# Music Sync

Sync your downloaded music with your online platforms.

## Features

- Download the likes of a SoundCloud user.
- Download a list of songs urls supported by
  [yt-dlp](https://github.com/yt-dlp/yt-dlp) (saved in a `m3u` file).

## Requirements

- [Python](https://www.python.org/) (version >= 3.10) as a programming language.
- [pipenv](https://pip.pypa.io) as a package and venv management tool. If you do
  not have pipenv installed refer to [pipenv install
  instruction](https://pipenv.pypa.io/en/latest/installation.html).
- [ffmpeg](https://www.ffmpeg.org) to process downloaded file (convert format /
  add metadata). On debian you can install it with `sudo apt install ffmpeg`.

## Installation

```sh
git clone https://github.com/Mathieu-COSYNS/music-sync
cd ./music-sync
pipenv install
# or pipenv install --dev
```

## Run

```sh
pipenv run musicsync
```

The first time you run the program a config file will be generated. By default
no syncing module are enabled.
You should edit this config file to enable some modules and tweak the program
behavior to your liking. The config file is located according to your xdg
preferences (`~/.config/music_sync/config.yml` by default).

## Test

```sh
pipenv run test
```
