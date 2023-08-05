![PyPI](https://img.shields.io/pypi/v/dwanimes?color=blue&label=Version&logo=python&style=for-the-badge)

# Download animes

Download any anime from the web with only one command in your PC.

## Instalation

Execute command:

```bash
pip install dwanimes
```

## To use CLI

```bash
dw-animes --help
dw-animes --name spy-x-family --chapter 1
```

## To use library

```py
import pydwanimes

# Directory to save animes
directory = "/home/my-user/Videos"

# Compose optional loading class
loading = pydwanimes.loading.tqdm_loading.TqdmLoading()

# Compose site class
config = {
    "directory": directory,
    "loading": loading,
}
site = pydwanimes.sites.anime_fenix.AnimeFenix(config)

# Download anime chapter
site.download_multimedia("spy-x-family", 1)
```
