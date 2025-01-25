import logging

from marshmallow import Schema

from music_sync.core.apps import AppRegistry
from music_sync.core.config import get_config, get_config_path
from music_sync.core.logging import setup_logging
from music_sync.core.schema import ContextAware, PathField
from music_sync.m3u.apps import M3UApp
from music_sync.soundcloud.apps import SoundCloudApp

logger = logging.getLogger(__name__)

APPS = [
    SoundCloudApp,
    M3UApp,
]


class MusicSyncConfigSchema(Schema):
    base_dir = ContextAware(
        PathField, required=True, dump_default="~/Music", context_key="base_path"
    )
    download_archive = ContextAware(PathField, dump_default=".download_archive.txt")


class MusicSync:
    def __init__(self, log_level=logging.WARNING) -> None:
        setup_logging(log_level)

    def sync(self):
        registry = AppRegistry(MusicSyncConfigSchema)
        registry.register(APPS)
        config_schema = registry.get_config_schema()

        try:
            config = config_schema().load(get_config(default=config_schema().dump({})))
        except Exception:
            logger.exception("Impossible to load the configuration file.")
            return

        no_module_enabled = True

        for app in registry.initialize(config):
            if app.is_enabled:
                no_module_enabled = False
                try:
                    logging.getLogger(__name__).info(f"Syncing {app}")
                    error_code = app.sync()
                    if error_code:
                        logging.getLogger(__name__).error(
                            f"Some {app} files failed to download"
                        )
                    else:
                        logging.getLogger(__name__).info(f"{app} synced")
                except Exception as error:
                    logger.exception(f"{app} sync failed: {error}")
            else:
                logger.debug(f"{app} is disabled")

        if no_module_enabled:
            logger.warning(
                "No module are enabled. Enable at least one module in the "
                + f"configuration file located at {get_config_path()}"
            )
        else:
            logger.info("Syncing finished")
