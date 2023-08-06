import inspect
from abc import ABC
from fallenleaf.di.types import IContainer, IProvider
from fallenleaf.di.exceptions import BindingError, BuildingError


class Provider(IProvider, ABC):
    __container = None

    def __init__(self, blueprint: type, builder: callable = None):
        self.__builder = builder
        if not builder:
            self.__builder = blueprint
        self.__blueprint = blueprint

    def bind_to_container(self, container: IContainer):
        if self.__container:
            raise BindingError("Double binding")
        self.__container = container

    def build(self):
        signature = inspect.signature(self.builder)
        kw_dependencies = {}
        for key, parameter in signature.parameters.items():
            if key == "container":
                kw_dependencies[key] = self.__container
                continue
            if key == "blueprint":
                kw_dependencies[key] = self.__blueprint
                continue
            kw_dependencies[key] = None
            annotated_types = [parameter.annotation] if isinstance(parameter.annotation, type) else parameter.annotation.__args__
            deps = [self.__container.make(type_) for type_ in annotated_types]
            for dep in deps:
                if dep:
                    kw_dependencies[key] = dep
                    break
        if self.builder == self.blueprint:
            return self.blueprint(**kw_dependencies)
        # kw_dependencies["container"] = self.__container
        # kw_dependencies["blueprint"] = self.__blueprint
        return self.builder(**kw_dependencies)

    @property
    def builder(self):
        return self.__builder

    @property
    def blueprint(self):
        return self.__blueprint

    @property
    def container(self):
        return self.__container

    def __call__(self):
        return self.provide()


class Singleton(Provider):
    __instance = None

    def provide(self):
        if not self.__instance:
            self.__instance = self.build()
        return self.__instance


class Factory(Provider):
    def provide(self):
        return self.build()
