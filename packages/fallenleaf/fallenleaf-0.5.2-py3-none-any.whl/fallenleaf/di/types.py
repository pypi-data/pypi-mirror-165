from __future__ import annotations
from abc import ABC, abstractmethod


class IProvider(ABC):
    @abstractmethod
    def provide(self):
        pass

    @abstractmethod
    def bind_to_container(self, container: IContainer):
        pass

    @property
    @abstractmethod
    def blueprint(self):
        pass

    @property
    @abstractmethod
    def builder(self):
        pass


class IContainer(ABC):
    @abstractmethod
    def make(self, blueprint: type):
        pass

    @abstractmethod
    def bind(self, provider: IProvider):
        pass