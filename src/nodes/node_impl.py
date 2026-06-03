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

# Base types used to validate candidate classes
_BASE_TYPES = (
    bpy.types.ShaderNodeCustomGroup,
    bpy.types.GeometryNodeCustomGroup,
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
        # Compute the full dotted module name (e.g. "src.nodes.shader.lscherry.make_toon")
        # so that relative imports inside compiled files resolve correctly.
        # _NODES_DIR = src/nodes/, so addon_root = the LSPotato package directory.
        addon_root = _NODES_DIR.parent.parent
        try:
            rel          = py_file.relative_to(addon_root)
            parts        = list(rel.with_suffix("").parts)
            module_name  = ".".join(parts)
            package_name = ".".join(parts[:-1])
        except ValueError:
            module_name  = py_file.stem
            package_name = ""

        try:
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            mod  = importlib.util.module_from_spec(spec)
            mod.__package__ = package_name
            sys.modules.setdefault(module_name, mod)
            spec.loader.exec_module(mod)
        except Exception as e:
            logger.error(f"NodeLib: cannot load '{py_file.name}': {e}")
            return []

        result = []
        for attr in vars(mod).values():
            if (
                isinstance(attr, type)
                and attr not in _BASE_TYPES
                and issubclass(attr, _BASE_TYPES)
                and "bl_label" in attr.__dict__
            ):
                result.append(attr)
        return result
