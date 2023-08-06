class ConfigurableMeta(type):
    def __new__(cls, name: str, bases: list, attrs: dict, **kw):
        super_new = super().__new__
        config_class = attrs.pop("Config", None)
        attrs["_config"] = None
        if config_class:
            attrs["_config"] = config_class()
        return super_new(cls, name, bases, attrs, **kw)


class Configurable(metaclass=ConfigurableMeta):
    def __setitem__(self, key: str, value: any):
        setattr(self._config, key, value)

    def __getitem__(self, key: str):
        return getattr(self._config, key)
