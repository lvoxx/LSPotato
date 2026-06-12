import importlib.util
import sys
from pathlib import Path
import os
import bpy  # type: ignore
from ..utils.logger import get_logger


logger = get_logger("NodeImpl")

# ---------------------------------------------------------------------------
# The shader directory sits at the same level as this file: src/nodes/shader/
# ---------------------------------------------------------------------------
_NODES_DIR   = Path(os.path.dirname(os.path.abspath(__file__)))
_shader_DIR = _NODES_DIR / "shader"

# Base types used to validate candidate classes.
# Shader only for now — geometry node support is deferred, so GeometryNode
# subclasses are intentionally NOT scanned, registered, or added to the menu.
_BASE_TYPES = (
    bpy.types.ShaderNodeCustomGroup,
)

# ---------------------------------------------------------------------------
# LSCherry directory structure (mirrors the scene hierarchy in Blender)
# Map: shader subfolder name → relative folder path inside shader/
#
# lscherry/                     → shader/lscherry/
# ├── combiner                → shader/lscherry/combiner/
# ├── core                    → shader/lscherry/core/
# ├── external/               → shader/lscherry/external/
# │   └── michos/             → shader/lscherry/external/michos/
# │       ├── honkai-impact-3 → shader/lscherry/external/michos/honkai_impact_3/
# │       ├── genshin-impact  → shader/lscherry/external/michos/genshin_impact/
# │       └── honkai-star-rail→ shader/lscherry/external/michos/honkai_star_rail/
# ├── festivities             → shader/lscherry/festivities/
# ├── GloTAni                 → shader/lscherry/glotani/
# ├── AVR                     → shader/lscherry/avr/
# ├── XTR                     → shader/lscherry/xtr/
# ├── MMD                     → shader/lscherry/mmd/
# ├── MICA                    → shader/lscherry/mica/
# ├── post-production         → shader/lscherry/post_production/
# ├── utils/                  → shader/lscherry/utils/
# │   ├── bnodes              → shader/lscherry/utils/bnodes/
# │   ├── procedural          → shader/lscherry/utils/procedural/
# │   ├── ramp-style          → shader/lscherry/utils/ramp_style/
# │   ├── separator           → shader/lscherry/utils/separator/
# │   └── normal              → shader/lscherry/utils/normal/
# ├── global                  → shader/lscherry/global/
# ├── dev                     → shader/lscherry/dev/
# ├── plugin                  → shader/lscherry/plugin/
# ├── vfx                     → shader/lscherry/vfx/
# └── <material>/             → material-based subfolders (auto-created by compile)
# ---------------------------------------------------------------------------


class NodeLib:
    """
    Scans the entire src/nodes/shader/ tree following the actual LSCherry layout
    and returns the list of compiled node classes, ready to register.
    """

    @staticmethod
    def get_node_classes() -> list:
        """Returns the list of all shader node classes. Safe — never raises."""
        try:
            return NodeLib._scan_all()
        except Exception as e:
            logger.error(f"NodeLib.get_node_classes error: {e}")
            return []

    @staticmethod
    def get_class_names() -> list[str]:
        return [cls.__name__ for cls in NodeLib.get_node_classes()]

    # ------------------------------------------------------------------ internal

    @staticmethod
    def _scan_all() -> list:
        if not _shader_DIR.is_dir():
            logger.warning(f"NodeLib: shader dir not found: {_shader_DIR}")
            return []

        seen: set[str] = set()
        classes: list = []

        SKIP_STEMS = {"__init__", "node", "utils", "node_impl", "node_info"}

        for py_file in sorted(_shader_DIR.rglob("*.py")):
            if py_file.stem in SKIP_STEMS:
                continue
            for cls in NodeLib._load_file(py_file):
                if cls.__name__ not in seen:
                    seen.add(cls.__name__)
                    classes.append(cls)

        return classes

    @staticmethod
    def _load_file(py_file: Path) -> list:
        # Derive the dotted module name from __package__ so the namespace matches
        # what Blender actually uses: "LSPotato.nodes" in dev, but
        # "bl_ext.user_default.LSPotato.nodes" inside the extension sandbox.
        # Using the filesystem root instead would produce bare "LSPotato.*" names
        # that Blender's extension policy checker rejects as top-level violations.
        try:
            rel          = py_file.relative_to(_shader_DIR)
            parts        = list(rel.with_suffix("").parts)
            base_pkg     = (__package__ or "") + ".shader"
            module_name  = base_pkg + "." + ".".join(parts)
            package_name = base_pkg + ("." + ".".join(parts[:-1]) if len(parts) > 1 else "")
        except ValueError:
            module_name  = py_file.stem
            package_name = ""

        # NOTE: we intentionally do NOT leave the leaf module in sys.modules.
        # Blender's extension policy audit scans sys.modules after register()
        # and flags every module whose file lives inside the extension dir.
        # We only need the module long enough to read its node classes, so we
        # register it for the duration of exec (so any self-reference resolves)
        # and pop it again afterwards. __package__ is still set correctly so the
        # relative imports inside compiled files (`from ...node import ...`)
        # resolve against the real, Blender-owned parent package.
        inserted = False
        try:
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            mod  = importlib.util.module_from_spec(spec)
            mod.__package__ = package_name
            if module_name not in sys.modules:
                sys.modules[module_name] = mod
                inserted = True
            spec.loader.exec_module(mod)
        except Exception as e:
            logger.error(f"NodeLib: cannot load '{py_file.name}': {e}")
            return []
        finally:
            if inserted:
                sys.modules.pop(module_name, None)

        result = []
        for attr in vars(mod).values():
            if (
                isinstance(attr, type)
                and attr not in _BASE_TYPES
                and issubclass(attr, _BASE_TYPES)
                and "bl_label" in attr.__dict__
                and "bl_idname" in attr.__dict__
            ):
                result.append(attr)
        return result
