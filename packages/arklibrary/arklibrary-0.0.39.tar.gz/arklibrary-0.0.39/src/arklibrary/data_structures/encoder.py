import pickle
from arklibrary.admin import Admin, Bundle
from arklibrary.lib.configuration import Ini

required_types = [int, float, set, bool, type(None), str, dict, list, Admin, Bundle, Ini]


def assert_data_types(data):
    type_names = ', '.join([data_type.__name__ for data_type in required_types])
    message = f"\nEncoding must be of types: {type_names}\nBut was: {type(data).__name__}"
    assert any([isinstance(data, data_type) for data_type in required_types]), message


def encode(data) -> bytes:
    assert_data_types(data)
    return pickle.dumps(data)


def decode(stream):
    return pickle.loads(stream)

