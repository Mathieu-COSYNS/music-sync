# Music Sync

Sync your downloaded music with your online platforms.

## Features

- Download the likes of a SoundCloud user.
- Download a list of songs urls supported by
  [yt-dlp](https://github.com/yt-dlp/yt-dlp) (saved in a `m3u` file).

## Requirements

- [Python](https://www.python.org/) (version >= 3.10) as a programming language.
- [uv](https://docs.astral.sh/uv/) as a package and venv management tool. If you do
  not have uv installed refer to [uv install
  instruction](https://docs.astral.sh/uv/getting-started/installation/).
- [ffmpeg](https://www.ffmpeg.org) to process downloaded file (convert format /
  add metadata). On debian you can install it with `sudo apt install ffmpeg`.

## Installation

```sh
git clone https://github.com/Mathieu-COSYNS/music-sync
cd ./music-sync
uv venv
. .venv/bin/activate
uv sync
```

## Run

```sh
uv run cli.py
```

The first time you run the program a config file will be generated. By default
no syncing module are enabled.
You should edit this config file to enable some modules and tweak the program
behavior to your liking. The config file is located according to your xdg
preferences (`~/.config/music_sync/config.yml` by default).

## Test

```sh
uv run -m unittest discover
```
