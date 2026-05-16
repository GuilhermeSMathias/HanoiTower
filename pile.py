class Pile:
    def __init__(self):
        self._items = []
        self._size = 0

    def push(self, item):
        self._items.append(item)
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError('Empty pile')
        self._size -= 1
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError('Empty pile')
        return self._items[-1]

    def is_empty(self):
        return self._size == 0

    def size(self):
        return self._size

    def __repr__(self):
        return f'Pile({self._items[::-1]})'

    @property
    def items(self):
        return self._items
