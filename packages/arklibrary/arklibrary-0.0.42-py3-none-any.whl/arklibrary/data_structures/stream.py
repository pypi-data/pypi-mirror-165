import json
from arklibrary.data_structures.encoder import encode, decode
from collections import defaultdict
import pickle


class Stream:
    r"""
    A header is a 1 of the 3 parts which make up the Stream:
        Stream = [Size Stream][Header Stream][Data Stream]
                - Size Stream: length of the header stream.
                - Header Stream: extra data about the body, credentials, etc.
                - Data Stream: the raw data being sent.
        Ex.
                         Size       Header Stream                               Data Stream
            Stream   =   0036   |   {body_length: 19, body_type: 'json'}   |    {'data': 'my data'}
            Stream   =   0038   |   {body_length: 19, body_type: 'pickle'} |    \x8\a43\x92\x213\x1
            Stream   =   0035   |   {body_length: 19, body_type: 'str'}   |     this is my data str
    """
    SIZE = 4  # is 4 decimal digits long (e.g. 4 bytes)

    @classmethod
    def new(cls, stream: bytes) -> 'Stream':
        return pickle.loads(stream)

    def __init__(self, **kwargs):
        attrs = defaultdict(lambda: None)
        attrs.update(kwargs)
        self.from_address = attrs['from_address']
        self.to_address = attrs['to_address']
        self.authentication = attrs['authentication']
        self.expiration = attrs['expiration']
        self.body = attrs['body']
        self.function = attrs['function']
        self.type = attrs['type']

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def __getitem__(self, item):
        return self.__dict__[item]

    def encode(self) -> bytes:
        return pickle.dumps(self)

    def __getstate__(self):
        state = self.__dict__.copy()
        state['body'] = encode(self.body)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.body = decode(state['body'])

    def __eq__(self, other):
        return other.__dict__ == self.__dict__

    def __repr__(self):
        items = []
        for k, v in dict(self).items():
            items.append(f"\033[34m{k}\033[90m=\033[0m{repr(v)}\033[0m")
        args = ', '.join(items)
        return f'<\033[96mHeader\033[0m({args})>\033[0m'

