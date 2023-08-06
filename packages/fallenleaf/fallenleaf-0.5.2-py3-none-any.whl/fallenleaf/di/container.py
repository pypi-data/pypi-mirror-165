from typing import List
from fallenleaf.di.types import IContainer, IProvider
from fallenleaf.di.provider import Singleton, Factory

class Container(IContainer):
    bindings: List[IProvider]

    def __init__(self):
        self.bindings = []

    def bind(self, provider: IProvider):
        self.bindings.append(provider)
        provider.bind_to_container(self)

    def make(self, blueprint: type):
        for binding in self.bindings:
            if binding.blueprint == blueprint:
                return binding.provide()
        return None

    # decorators
    def bind_singleton(self, blueprint: type):
        self.bind(Singleton(blueprint))
        return blueprint

    def bind_factory(self, blueprint: type):
        self.bind(Factory(blueprint))
        return blueprint