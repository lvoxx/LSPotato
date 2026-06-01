import importlib.util
from pathlib import Path
import os
import bpy  # type: ignore

# ---------------------------------------------------------------------------
# Thư mục shader nằm cùng cấp với file này: src/nodes/shader/
# ---------------------------------------------------------------------------
_NODES_DIR   = Path(os.path.dirname(os.path.abspath(__file__)))
_shader_DIR = _NODES_DIR / "shader"

# Base types dùng để kiểm tra class hợp lệ
_BASE_TYPES = (
    bpy.types.ShaderNodeCustomGroup,
    bpy.types.GeometryNodeCustomGroup,
)

# ---------------------------------------------------------------------------
# Cấu trúc thư mục LSCherry (từ scene hierarchy trong Blender)
# Map: tên subfolder shader → folder path tương đối trong shader/
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
# └── vfx                     → shader/lscherry/vfx/
# ---------------------------------------------------------------------------

# Tất cả subpath dưới shader/ cần scan (thứ tự không quan trọng)
_ALL_SUBPATHS: list[str] = [
    # Root lscherry — node group chính không thuộc subfolder nào
    "lscherry",
    # combiner
    "lscherry/combiner",
    # core
    "lscherry/core",
    # external → michos
    "lscherry/external/michos/honkai_impact_3",
    "lscherry/external/michos/genshin_impact",
    "lscherry/external/michos/honkai_star_rail",
    # festivities, standalone characters
    "lscherry/festivities",
    "lscherry/glotani",
    "lscherry/avr",
    "lscherry/xtr",
    "lscherry/mmd",
    "lscherry/mica",
    # post-production
    "lscherry/post_production",
    # utils subgroups
    "lscherry/utils/bnodes",
    "lscherry/utils/procedural",
    "lscherry/utils/ramp_style",
    "lscherry/utils/separator",
    "lscherry/utils/normal",
    # global, dev, plugin, vfx
    "lscherry/global",
    "lscherry/dev",
    "lscherry/plugin",
    "lscherry/vfx",
]


class NodeLib:
    """
    Scan toàn bộ src/nodes/shader/ theo cấu trúc LSCherry thực tế
    và trả về list class node đã compile, sẵn sàng để register.
    """

    @staticmethod
    def get_node_classes() -> list:
        """Trả về list tất cả shader node class. Safe — không raise."""
        try:
            return NodeLib._scan_all()
        except Exception as e:
            print(f"[LSPotato] NodeLib.get_node_classes error: {e}")
            return []

    @staticmethod
    def get_class_names() -> list[str]:
        return [cls.__name__ for cls in NodeLib.get_node_classes()]

    # ------------------------------------------------------------------ internal

    @staticmethod
    def _scan_all() -> list:
        if not _shader_DIR.is_dir():
            print(f"[LSPotato] NodeLib: shader dir not found: {_shader_DIR}")
            return []

        seen: set[str] = set()   # dedup by class __name__
        classes: list = []

        for subpath in _ALL_SUBPATHS:
            folder = _shader_DIR / subpath
            if not folder.is_dir():
                continue
            for cls in NodeLib._scan_folder(folder):
                if cls.__name__ not in seen:
                    seen.add(cls.__name__)
                    classes.append(cls)

        # Fallback: scan root shader/ (cho node không phân loại)
        for cls in NodeLib._scan_folder(_shader_DIR, recursive=False):
            if cls.__name__ not in seen:
                seen.add(cls.__name__)
                classes.append(cls)

        return classes

    @staticmethod
    def _scan_folder(folder: Path, recursive: bool = False) -> list:
        classes: list = []
        try:
            py_files = [
                f for f in folder.iterdir()
                if f.is_file()
                and f.suffix == ".py"
                and f.stem not in {"__init__", "node", "utils", "node_impl", "node_info"}
            ]
        except OSError:
            return []

        for py_file in py_files:
            classes.extend(NodeLib._load_file(py_file))

        return classes

    @staticmethod
    def _load_file(py_file: Path) -> list:
        try:
            spec = importlib.util.spec_from_file_location(py_file.stem, py_file)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"[LSPotato] NodeLib: cannot load '{py_file.name}': {e}")
            return []

        result = []
        for attr in vars(mod).values():
            if (
                isinstance(attr, type)
                and attr not in _BASE_TYPES
                and issubclass(attr, _BASE_TYPES)
            ):
                result.append(attr)
        return result
