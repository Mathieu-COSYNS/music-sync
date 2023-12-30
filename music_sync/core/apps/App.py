import copy
import re
from collections import namedtuple
from abc import ABC, abstractmethod

from marshmallow import Schema, fields, post_load


class App(ABC):

    class ConfigSchema(Schema):
        enabled = fields.Boolean(required=True, dump_default=False)

        def __init__(self, *, context: dict | None = None, **kwargs):
            super().__init__(context=copy.deepcopy(context), **kwargs)

        @post_load
        def to_obj(self, data, **kwargs):
            name = self.__class__.__qualname__.replace(
                '.', '').replace('Schema', '')
            fields = self.__class__._declared_fields.keys()
            return namedtuple(name, fields, defaults=(None,) * len(fields))(**data)

    def __init__(self, config) -> None:
        assert re.match('^[a-z0-9_]+$', self.name) is not None, \
            f"{self.__class__.__name__} name is {self.name} but should only contains lower case a-z0-9 characters or underscore."
        if not hasattr(config, 'enabled'):
            raise ValueError(f"{config} does not have a enabled property")
        self._config = config

    @property
    @abstractmethod
    def name(self) -> str:
        assert False, "App {self.__class__.__name__} does not have a name attribute."

    @property
    def verbose_name(self):
        return self.name

    @property
    def config(self):
        return self._config

    @property
    def is_enabled(self):
        return bool(self.config.enabled)

    @abstractmethod
    def sync(self):
        return 0

    def __str__(self) -> str:
        return self.verbose_name
