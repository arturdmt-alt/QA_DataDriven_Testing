import yaml
import os
from typing import Dict, Any


class ConfigReader:
    
    def __init__(self, config_file: str = "config/dev.yaml"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing YAML: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    def get_base_url(self) -> str:
        return self.get('sut.base_url')
    
    def get_timeout(self) -> int:
        return self.get('test_config.timeout', 30)
    
    def get_retry_attempts(self) -> int:
        return self.get('test_config.retry_attempts', 3)


config = ConfigReader()
