from marshmallow import fields

from music_sync.core.apps import App
from music_sync.core.config import get_config_path
from music_sync.core.download import ArchiveParser
from music_sync.core.download import Downloader
from music_sync.core.schema import ContextAware, MetadataActionsSchema, PathField
from music_sync.soundcloud.api import list_liked_tracks


class SoundCloudApp(App):
    name = "soundcloud_likes"
    verbose_name = "SoundCloud Likes"

    class ConfigSchema(App.ConfigSchema):
        username = fields.String(required=True, dump_default='')

        dir = ContextAware(PathField, required=True,
                           context_key='base_path', dump_default='SoundCloud')
        download_archive = ContextAware(
            PathField, dump_default='.download_archive.txt')
        download_folder = ContextAware(
            PathField, required=True, context_read_key='base_path')
        metadata_actions = ContextAware(fields.Nested(
            MetadataActionsSchema), dump_default=MetadataActionsSchema().dump({}))

    def sync(self):

        if self.config.username == '':
            raise ValueError(
                f"You should configure an username for SoundCloud or disable SoundCloud sync in {get_config_path(writable=True)}")

        tracks = list_liked_tracks(self.config.username)

        if self.config.download_archive:
            try:
                archived_ids = [id for provider, id in ArchiveParser(
                self.config.download_archive).read_rows() if provider == 'soundcloud']
            except FileNotFoundError:
                archived_ids = []

        urls = [track['permalink_url']
                for track in tracks if f"{track['id']}" not in archived_ids]

        return Downloader(download_folder=self.config.download_folder,
                          download_archive=self.config.download_archive,
                          metadata_actions=self.config.metadata_actions).download(urls)
