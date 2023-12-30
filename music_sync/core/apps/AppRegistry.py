from collections.abc import Iterable
import logging

from marshmallow import fields

from music_sync.core.apps.App import App
from music_sync.core.utils import safe_issubclass


class AppRegistry():
    _apps = []

    def __init__(self, global_config_schema_class) -> None:
        self._global_config_schema_class = global_config_schema_class

    def register(self, apps: App | Iterable[App]):

        if not isinstance(apps, Iterable):
            apps = [apps]

        for app in apps:
            if not safe_issubclass(app, App):
                raise ValueError(f"{app} is not a subclass of App.")
            if app in self._apps:
                raise ValueError(f"{app} in already registered.")
            self._apps.append(app)

    def get_config_schema(self):
        apps_configs = {}
        for app in self._apps:
            apps_configs[app.name] = fields.Nested(
                app.ConfigSchema, required=True, dump_default=app.ConfigSchema().dump({}))
        return self._global_config_schema_class.from_dict(apps_configs)

    def initialize(self, config):
        apps_instances = []
        for app in self._apps:
            try:
                apps_instances.append(app(config.get(app.name)))
            except Exception as err:
                logging.getLogger(__name__).error(err)
        return apps_instances
