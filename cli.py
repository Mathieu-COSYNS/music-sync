import argparse
import itertools

from music_sync import LOG_LEVELS, MusicSync


def main():
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description="Sync your downloaded music with your online platforms",
    )

    parser.add_argument(
        "--log",
        choices=list(itertools.chain(*LOG_LEVELS.items())),
        help="log level",
        default="INFO",
        type=str.upper,
    )

    args = parser.parse_args()

    music_sync = MusicSync(log_level=args.log)
    music_sync.sync()


if __name__ == "__main__":
    main()
