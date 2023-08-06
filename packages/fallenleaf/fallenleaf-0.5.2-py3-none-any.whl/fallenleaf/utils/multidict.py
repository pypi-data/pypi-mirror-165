class MultiDict(dict):
    _default_index = 0

    def __init__(self, **data):
        res = []
        for key, value in data.items():
            res.append([key, [value]])
        super().__init__(res)

    def set(self, key: any, index:int, value: any):
        if key not in self:
            super().__setitem__(key, [])
        values = super().__getitem__(key)
        if index >= len(values):
            self.add(key, value)
        values[index] = value
        super().__setitem__(key, values)

    def get(self, key: any, index: int):
        if key not in self:
            return None
        values = super().__getitem__(key)
        if index >= len(values):
            return None
        return values[index]

    def __getitem__(self, key: any):
        return self.get(key, self._default_index)

    def __setitem__(self, key:any, value:any):
        self.set(key, self._default_index, value)

    def __str__(self):
        cls = type(self)
        res = f"<{cls.__name__}("
        for key, values in self.items():
            for value in values:
                res += f"{key} : {value}, " if not isinstance(value, str) else f"{key} : \"{value}\", "
        return res + ")>"

    def add(self, key: any, value: any):
        if key not in self:
            raise KeyError(key)
        values = super().__getitem__(key)
        values.append(value)
        super().__setitem__(key, values)
        return self

    def popitem(self, key: any, index: int):
        values = super().__getitem__(key)
        if index >= len(values):
            raise IndexError(index)
        value = values.pop(index)
        super().__setitem__(key, values)
        return value