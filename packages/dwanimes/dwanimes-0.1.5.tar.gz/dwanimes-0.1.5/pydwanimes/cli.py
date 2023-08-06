from argparse import ArgumentParser
import argparse
from pathlib import Path

import pydwanimes.application.sites.anime_fenix as anime_fenix
from pydwanimes.application.loading.tqdm_loading import TqdmLoading
from pydwanimes.application.config import config


def main():
    parser = ArgumentParser(description="Anime downloader",
                            formatter_class=argparse.HelpFormatter)
    parser.add_argument("-n", "--name", dest="name",
                        help="Anime name", required=True)
    parser.add_argument("-c", "--chapter", dest="chapter",
                        type=int, help="Chapter number", required=True)
    parser.add_argument("--directory", dest="directory",
                        type=str,
                        default=config.get("directory"),
                        help="Directory to save animes")
    args = parser.parse_args()

    anime_slug = args.name
    chapter = args.chapter
    path = Path(args.directory).joinpath(anime_slug)
    d = path.resolve()

    ld = TqdmLoading()

    s = anime_fenix.AnimeFenix({
        "directory": d,
        "loading": ld
    })
    s.download_multimedia(anime_slug, chapter)


if __name__ == '__main__':
    main()
