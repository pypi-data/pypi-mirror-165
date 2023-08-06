import pydwanimes.domain.player as player
import pydwanimes.domain.site as site

from importlib import import_module

SITES = {
    "animefenix": "Animefenix",
}

PLAYERS = {
    "fireload": "Fireload",
    "your_upload": "YourUpload",
    "fembed": "Fembed"
}


def get_player_class(name: str, **config) -> player.Player:
    try:
        m = import_module(f"pydwanimes.application.players.{name}")
    except ImportError as e:
        raise e
    return getattr(m, PLAYERS[name])(**config)


def get_site_class(name: str) -> site:
    try:
        m = import_module(f"application.sites.{name}")
    except ImportError as e:
        raise e
    return getattr(m, SITES[name])
