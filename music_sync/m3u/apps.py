import logging
import os

from marshmallow import fields

from music_sync.core.apps import App
from music_sync.core.download import Downloader
from music_sync.core.schema import (
    ContextAware,
    MetadataActionsSchema,
    PathField,
)
from music_sync.core.utils import is_valid_url

logger = logging.getLogger(__name__)


class M3UApp(App):
    name = "m3u"
    verbose_name = "M3U Playlists"

    class ConfigSchema(App.ConfigSchema):
        dir = ContextAware(PathField, required=True, context_key="base_path")
        download_archive = ContextAware(PathField)
        download_folder = ContextAware(
            PathField, required=True, context_read_key="base_path"
        )
        metadata_actions = ContextAware(
            fields.Nested(MetadataActionsSchema),
            dump_default=MetadataActionsSchema().dump({}),
        )
        files = fields.List(PathField(required=True), dump_default=[])

    def sync(self):
        downloader = Downloader(
            download_folder=self.config.download_folder,
            download_archive=self.config.download_archive,
            metadata_actions=self.config.metadata_actions,
        )

        for file_path in self.config.files:
            if not os.path.isfile(file_path) or not os.access(file_path, os.R_OK):
                logger.warning(f"{file_path} does not exist or is not a readable file")
                continue

            urls = []

            with open(file_path) as file:
                for item in file:
                    item = item.strip()
                    if len(item) == 0:
                        continue
                    if item[0] == "#":
                        continue
                    if not is_valid_url(item):
                        logger.warning(f"{item} is not a valid url.")
                        continue
                    urls.append(item)

            logger.info(f"Downloading music from {file_path}")

            error_code = downloader.download(urls)
            if error_code:
                return error_code

        return 0
