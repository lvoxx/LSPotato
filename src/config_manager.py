import os
import yaml
from pathlib import Path
from typing import Dict, Any

class _ConfigManager:
    _instance = None
    
    def __init__(self):
        if _ConfigManager._instance is not None:
            raise RuntimeError("Use ConfigManager.instance() instead")
        
        self.config_path = os.path.join(Path(__file__).parent.parent, "application.yml")
        self._config = self._load_config()
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"Warning: Could not load config - {str(e)}")
            return {}
    
    def get_bl_info(self) -> Dict[str, Any]:
        """Get blender addon metadata from config"""
        app_config = self._config.get('application', {})
        version = app_config.get('version', [1, 0, 0])
        blender_version = app_config.get('blender', [4, 3, 0])
        
        return {
            "name": app_config.get('name', 'BPotato'),
            "author": app_config.get('author', 'Lvoxx'),
            "description": app_config.get('description', ''),
            "location": app_config.get('location', '3D View > Properties > BPotato'),
            "category": app_config.get('category', 'Tool'),
            "version": tuple(version),
            "blender": tuple(blender_version),
        }
    
    def get_graphviz_path(self) -> str:
        """Get Graphviz path from config"""
        default_path = os.path.join(
            Path(__file__).parent.parent,
            "dependencies",
            "Graphviz-13.1.2-win64",
            "bin"
        )
        
        rel_path = self._config.get("dependencies", {}).get("graphviz")
        if not rel_path:
            return default_path
            
        return os.path.abspath(os.path.join(Path(__file__).parent.parent, rel_path))

# Singleton access point
ConfigManager = _ConfigManager.instance()