from platformdirs import PlatformDirs
from importlib import resources
import sys
import json

class Settings:
    def __init__(self):
        self._dirs = PlatformDirs("deskdrink", "elmaron", ensure_exists=True)
        self._user_config = self._dirs.user_config_path / "settings.json"
        self._default = None
        self._user = None
        self.load()
    
    def load(self):
        with resources.open_text("deskdrink", "data", "settings.json", encoding="utf-8") as file:
            self._default = json.load(file)
        
        if not self._user_config.exists():
            with open(self._user_config, "w") as f:
                self._user = {}
                for k in self._default.keys():
                    self._user[k] = None
                f.write(json.dumps(self._user))
        
        else:
            with open(self._user_config, "r") as f:
                self._user = json.load(f)
    
    def save(self):
        with open(self._user_config, "w") as f:
            f.write(json.dumps(self._user))