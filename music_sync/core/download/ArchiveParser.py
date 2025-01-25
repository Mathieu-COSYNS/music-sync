import csv


class ArchiveParser:
    def __init__(self, download_archive: str) -> None:
        self._download_archive = download_archive

    def read_rows(self):
        with open(self._download_archive) as f:
            reader = csv.reader(f, delimiter=" ")
            yield from reader
