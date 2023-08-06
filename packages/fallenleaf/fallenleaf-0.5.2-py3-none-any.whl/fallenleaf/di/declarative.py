from typing import List
from fallenleaf.di.types import IContainer, IProvider
from fallenleaf.di.provider import Singleton, Factory


class Provide:
    def __init__(self, blueprint: type, provider_type: IProvider = Singleton, builder: callable = None):
        cls = type(self)
        self.blueprint = blueprint
        self.provider_type = provider_type
        self.builder = builder if builder else blueprint

    def as_provider(self):
        return self.provider_type(self.blueprint, self.builder)


class DeclarativeContainer(IContainer):
    bindings: List[IProvider]

    def __init__(self):
        self.bindings = []
        for key in dir(self):
            if key.startswith("_"):
                continue
            value = getattr(self, key)
            if not isinstance(value, Provide):
                continue
            self.bind(value.as_provider())

    def bind(self, provider: IProvider):
        self.bindings.append(provider)
        provider.bind_to_container(self)

    def make(self, blueprint: type):
        for binding in self.bindings:
            if binding.blueprint == blueprint:
                return binding.provide()
        return None