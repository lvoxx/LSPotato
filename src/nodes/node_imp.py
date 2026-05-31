import importlib
from pathlib import Path
import os
from typing import List, Tuple, Type

class NodeLib:
    BASE_DIR = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "nodes"))
        
    @staticmethod
    def get_node_sets() -> Tuple[List[Type], List[Type]]:
        """Safely retrieve node definitions"""
        try:
            return NodeLib()()
        except Exception as e:
            print(f"Error loading node definitions: {e}")
            return [], []

    @staticmethod
    def import_classes_from_folder(folder_path):

        folder_name = folder_path.name
        prefix = "GeometryNode" if folder_name == "geometry" else "ShaderNode"
        imported_classes = []

        # Pre-fetch all .py files
        py_files = [
            f
            for f in folder_path.iterdir()
            if f.suffix == ".py" and f.stem not in {"__init__", "utils"}
        ]

        for py_file in py_files:
            module_name = f".nodes.{folder_name}.{py_file.stem}"

            try:
                module = importlib.import_module(module_name, package=__package__)
            except ImportError as e:
                continue

            for attr_name, attr in module.__dict__.items():
                if (
                    isinstance(attr, type)
                    and attr_name.startswith(prefix)
                    and attr_name != prefix
                ):
                    imported_classes.append(attr)
                    break
        return imported_classes

    @classmethod
    def __call__(cls):

        shader_folder = cls.BASE_DIR / "shader"
        shader_classes = cls.import_classes_from_folder(shader_folder)

        return shader_classes