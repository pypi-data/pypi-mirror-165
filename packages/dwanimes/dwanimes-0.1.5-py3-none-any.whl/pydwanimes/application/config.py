import json
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any

CONFIG_FILE_NAME = "config.json"
CONFIG_FILE_DIR = Path().home().joinpath(".config/dwanimes/")
CONFIG_FILE_PATH = CONFIG_FILE_DIR.joinpath(CONFIG_FILE_NAME).resolve()

DEFAULT = {
    "directory": "static/animes"
}


class Config:
    def __init__(self):
        CONFIG_FILE_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE_PATH.touch(exist_ok=True)

        for k in DEFAULT:
            setattr(self, k, DEFAULT[k])
        data = self.read()
        if not data:
            return
        for k in data:
            setattr(self, k, data[k])

    def read(self) -> Any:
        """ Read config file and return data """
        with open(str(CONFIG_FILE_PATH)) as f:
            try:
                data = json.load(f)
                return data
            except JSONDecodeError:
                return None

    def __getitem__(self, k) -> Any:
        return getattr(self, k, None)

    def get(self, key: Any) -> Any:
        return getattr(self, key, None)

    def update(self, key: Any, value: Any) -> None:
        setattr(self, key, value)


config = Config()
