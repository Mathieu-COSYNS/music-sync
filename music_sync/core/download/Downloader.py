import os

from yt_dlp import YoutubeDL

from .MetadataActions import MetadataActions


class Downloader():

    def __init__(self,
                 download_folder: str | None = None,
                 download_archive: str | None = None,
                 metadata_actions: MetadataActions | None = None) -> None:

        outtmpl = '%(artist|)s%(artist& - |)s%(uploader|)s%(uploader& - |)s%(title)s [%(id)s].%(ext)s'

        if download_folder is not None:
            outtmpl = os.path.join(download_folder, outtmpl)

        postprocessors = []

        if metadata_actions:
            postprocessors.append({
                'key': 'MetadataParser',
                'actions': metadata_actions.actions,
                'when': 'pre_process'
            })

        postprocessors.extend([
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            },
            {
                'key': 'FFmpegMetadata',
                'add_metadata': True
            },
            {
                'key': 'EmbedThumbnail',
                'already_have_thumbnail': False
            }
        ])

        self._ydl_opts = {
            'format': 'bestaudio/best',
            'windowsfilenames': True,
            'writethumbnail': True,
            'outtmpl': {
                'default': outtmpl,
                'pl_thumbnail': ''
            },
            'download_archive': download_archive,
            'postprocessors': postprocessors,
        }

    def download(self, urls: list[str]):
        with YoutubeDL(self._ydl_opts) as ydl:
            error_code = ydl.download(urls)

        return error_code
