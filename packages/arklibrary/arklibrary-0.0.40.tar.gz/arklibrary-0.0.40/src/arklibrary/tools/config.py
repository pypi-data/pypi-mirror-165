from pathlib import Path
import json


class Config:
    __config = None

    @classmethod
    def get(cls):
        if cls.__config:
            return cls.__config
        path = Path.cwd() / Path("config.json")
        assert path.exists(), "Unable to find the config file."
        with open(path, 'r') as r:
            cls.__config = json.load(r)

    @classmethod
    def admin_password(cls):
        return cls.get()['admin_password']

    @classmethod
    def ark_lnk_path(cls):
        return cls.get()['ark_lnk_path']

    @classmethod
    def admin_player_id(cls):
        return cls.get()['admin_player_id']

    def __repr__(self):
        items = []
        for k, v in self.__dict__.items():
            if k and k[0] != "_":
                items.append(f"\033[34m{k}\033[90m=\033[0m{repr(v)}\033[0m")
        args = ', '.join(items)
        return f'<\033[96m{type(self).__name__}\033[0m({args})>\033[0m'