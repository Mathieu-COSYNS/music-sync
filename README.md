# Music Sync

Sync your downloaded music with your online platforms.

## Features

- Download the likes of a SoundCloud user
- Download a list of songs urls (saved in a `m3u` file) supported by [yl-dlp](https://github.com/yt-dlp/yt-dlp)

## Requirements

[Python](https://www.python.org/) (version >= 3.10) and [pip](https://pip.pypa.io)

## Installation

```sh
git clone https://github.com/Mathieu-COSYNS/music-sync
cd ./music-sync
pip install -r requirements.txt
```

## Run

```sh
python3 cli.py
```

The first time you run the program a config file will be generated. By default no syncing module are enabled.
You should edit this config file to enable some modules and tweak the program behavior to your liking. The config file is located according to your xdg preferences (`~/.config/music_sync/config.yml` by default).

## Test

```sh
python3 -m unittest discover
```
