import importlib.util
from pathlib import Path
import os
import bpy  # type: ignore

# ---------------------------------------------------------------------------
# Thư mục compiled nằm cùng cấp với file này: src/nodes/compiled/
# ---------------------------------------------------------------------------
_NODES_DIR   = Path(os.path.dirname(os.path.abspath(__file__)))
_COMPILED_DIR = _NODES_DIR / "compiled"

# Base types dùng để kiểm tra class hợp lệ
_BASE_TYPES = (
    bpy.types.ShaderNodeCustomGroup,
    bpy.types.GeometryNodeCustomGroup,
)

# ---------------------------------------------------------------------------
# Cấu trúc thư mục LSCherry (từ scene hierarchy trong Blender)
# Map: tên subfolder compiled → folder path tương đối trong compiled/
#
# cherry/                     → compiled/cherry/
# ├── combiner                → compiled/cherry/combiner/
# ├── core                    → compiled/cherry/core/
# ├── external/               → compiled/cherry/external/
# │   └── michos/             → compiled/cherry/external/michos/
# │       ├── honkai-impact-3 → compiled/cherry/external/michos/honkai_impact_3/
# │       ├── genshin-impact  → compiled/cherry/external/michos/genshin_impact/
# │       └── honkai-star-rail→ compiled/cherry/external/michos/honkai_star_rail/
# ├── festivities             → compiled/cherry/festivities/
# ├── GloTAni                 → compiled/cherry/glotani/
# ├── AVR                     → compiled/cherry/avr/
# ├── XTR                     → compiled/cherry/xtr/
# ├── MMD                     → compiled/cherry/mmd/
# ├── MICA                    → compiled/cherry/mica/
# ├── post-production         → compiled/cherry/post_production/
# ├── utils/                  → compiled/cherry/utils/
# │   ├── bnodes              → compiled/cherry/utils/bnodes/
# │   ├── procedural          → compiled/cherry/utils/procedural/
# │   ├── ramp-style          → compiled/cherry/utils/ramp_style/
# │   ├── separator           → compiled/cherry/utils/separator/
# │   └── normal              → compiled/cherry/utils/normal/
# ├── global                  → compiled/cherry/global/
# ├── dev                     → compiled/cherry/dev/
# ├── plugin                  → compiled/cherry/plugin/
# └── vfx                     → compiled/cherry/vfx/
# ---------------------------------------------------------------------------

# Tất cả subpath dưới compiled/ cần scan (thứ tự không quan trọng)
_ALL_SUBPATHS: list[str] = [
    # Root cherry — node group chính không thuộc subfolder nào
    "cherry",
    # combiner
    "cherry/combiner",
    # core
    "cherry/core",
    # external → michos
    "cherry/external/michos/honkai_impact_3",
    "cherry/external/michos/genshin_impact",
    "cherry/external/michos/honkai_star_rail",
    # festivities, standalone characters
    "cherry/festivities",
    "cherry/glotani",
    "cherry/avr",
    "cherry/xtr",
    "cherry/mmd",
    "cherry/mica",
    # post-production
    "cherry/post_production",
    # utils subgroups
    "cherry/utils/bnodes",
    "cherry/utils/procedural",
    "cherry/utils/ramp_style",
    "cherry/utils/separator",
    "cherry/utils/normal",
    # global, dev, plugin, vfx
    "cherry/global",
    "cherry/dev",
    "cherry/plugin",
    "cherry/vfx",
]


class NodeLib:
    """
    Scan toàn bộ src/nodes/compiled/ theo cấu trúc LSCherry thực tế
    và trả về list class node đã compile, sẵn sàng để register.
    """

    @staticmethod
    def get_node_classes() -> list:
        """Trả về list tất cả compiled node class. Safe — không raise."""
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
        if not _COMPILED_DIR.is_dir():
            print(f"[LSPotato] NodeLib: compiled dir not found: {_COMPILED_DIR}")
            return []

        seen: set[str] = set()   # dedup by class __name__
        classes: list = []

        for subpath in _ALL_SUBPATHS:
            folder = _COMPILED_DIR / subpath
            if not folder.is_dir():
                continue
            for cls in NodeLib._scan_folder(folder):
                if cls.__name__ not in seen:
                    seen.add(cls.__name__)
                    classes.append(cls)

        # Fallback: scan root compiled/ (cho node không phân loại)
        for cls in NodeLib._scan_folder(_COMPILED_DIR, recursive=False):
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
