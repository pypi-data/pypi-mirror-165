from abc import abstractmethod
from pathlib import Path
import configparser
from collections import defaultdict


class Configuration:
    def __init__(self, path):
        self.path = path and Path(path) or None
        self.data = defaultdict(lambda: None)

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def __delitem__(self, key):
        pass

    @abstractmethod
    def __setitem__(self, key, value):
        pass

    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def keys(self):
        pass

    def exists(self):
        return self.path is not None and self.path.exists()


class Ini(Configuration):
    def __init__(self, path=None):
        super().__init__(path)
        if self.path and self.path.exists():
            config = configparser.ConfigParser()
            config.read(self.path)
            self.data = self.__to_dict(config)

    @classmethod
    def __to_dict(cls, data: dict, result=None):
        if result is None:
            result = {}
        for key, value in data.items():
            if isinstance(value, configparser.SectionProxy):
                result[key] = cls.__to_dict(dict(value))
            else:
                result[key] = value
        return result

    @classmethod
    def __to_array(cls, data: list):
        result = []
        for item in data:
            result.append(item)
        return list(data)

    def __getitem__(self, item):
        return self.data[item]

    def __contains__(self, item):
        return item in self.data

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        items = []
        for k, v in self.__dict__.items():
            if k and k[0] != "_":
                items.append(f"\033[34m{k}\033[90m=\033[0m{repr(v)}\033[0m")
        args = ', '.join(items)
        return f'<\033[96m{type(self).__name__}\033[0m({args})>\033[0m'
