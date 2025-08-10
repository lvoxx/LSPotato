import os
import yaml
from pathlib import Path
from typing import Dict, Any

class _ConfigManager:
    _instance = None
    
    def __init__(self):
        if _ConfigManager._instance is not None:
            raise RuntimeError("Use ConfigManager.instance() instead")
        
        self.config_path = os.path.join(Path(__file__).parent.parent, "application.yaml")
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