import json

class Trie:
    @classmethod
    def setup(cls, words):
        root = Trie()
        for word in words:
            root.add_child(word)
        return root

    def __init__(self, value=None):
        self.value = value
        # use a hashmap to lookup child nodes in constant time
        # Example: {'a': Node('a'), 'o': Node(o)}
        self.children = {}

    def keys(self):
        return self.children.keys()

    def values(self):
        return self.children.values()

    def items(self):
        return self.children.items()

    def __contains__(self, item):
        return item in self.children

    def __getitem__(self, item):
        if item not in self:
            return None
        return self.children[item]

    def __setitem__(self, key, value):
        self.children[key] = value

    def add_child(self, word):
        if word == "":
            self["."] = None
            return None
        next_char, rest_of_string = word[:1], word[1:]
        # If the node already exists in the trie you are building,
        # query it and pass it to the next recursive call
        if next_char in self:
            self[next_char].add_child(rest_of_string)
            return

        # If the node does not exist, create a new one
        # and add it to its parent
        self[next_char] = Trie(next_char)
        # Move on to the next
        self[next_char].add_child(rest_of_string)

    def is_member(self, word):
        if word == "":
            return "." in self.children
        next_char, rest_of_string = word[:1], word[1:]
        if next_char == ".":
            for child in self.values():
                if child.is_member(rest_of_string):
                    return True
        else:
            if next_char in self:
                return self[next_char].is_member(rest_of_string)
        return False

    def is_like(self, word):
        if word == "":
            return True
        next_char, rest_of_string = word[:1], word[1:]
        if next_char == ".":
            for child in self.values():
                if child.is_like(rest_of_string):
                    return True
        else:
            if next_char in self:
                return self[next_char].is_like(rest_of_string)
        return False

    def get_like(self, word):
        if self.is_like(word):
            return self.get_like_helper(word, [], "", self)
        return []

    def get_like_helper(self, word, found: list, traced: str, root):
        next_char, rest_of_string = word[:1], word[1:]
        if word == "":
            if root.is_member(traced):
                found.append(traced)
            for child_char, child in self.items():
                if child_char != ".":
                    child.get_like_helper(word, found, f"{traced}{child_char}", root)
        elif self.is_member(traced) and traced != "":
            found.append(traced)
            return found
        elif next_char in self:
            self[next_char].get_like_helper(rest_of_string, found, f"{traced}{next_char}", root)
        return found

    def __str__(self):
        return json.dumps(children_dict(self), sort_keys=True, indent=2)

    def __repr__(self):
        items = []
        for k, v in self.__dict__.items():
            if k and k[0] != "_":
                items.append(f"\033[34m{k}\033[90m=\033[0m{repr(v)}\033[0m")
        args = ', '.join(items)
        return f'<\033[96m{type(self).__name__}\033[0m({args})>\033[0m'


def children_dict(child, content={}):
    if child is None:
        return None
    return {**content, **{k: children_dict(v) for k, v in child.items()}}


if __name__ == "__main__":
    words = ['one', 'two', 'three', 'only', 'onyx', 'ones']
    root = Trie.setup(words)

    word = 'on'
    print(root)
    print(f"is_member({'one'}, root) => ", root.is_member('one'))
    print(f"is_member({'onl'}, root) => ", root.is_member('onl'))
    print(f"is_like('{word}', root) => ", root.is_like(word))
    print(f"is_like(''), root) =>", root.is_like(''))
    print(f"get_like('{word}', root) => ", root.get_like(word))
