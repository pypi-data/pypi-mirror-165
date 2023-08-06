from http.client import HTTPException
from typing import Generator, List, Tuple
from pydwanimes.domain import Site
from urllib import parse
import requests

from bs4 import BeautifulSoup


class AnimeFenix(Site):

    base_url = "https://www.animefenix.com"

    dictionary = {
        "your_upload": "YourUpload",
        "fireload": "Fireload",
        "fembed": "Fembed"
    }

    def get_tab_id(self, html: str, player_name: str) -> int:
        """ 
        Get tab id from attribute id='vid#ID' 

        Only supports : 
            -   YourUpload
            -   Fireload
        """
        soup = BeautifulSoup(html, "lxml")
        tab_id = soup.find("div", {
            "class": "tabs"
        }).find("ul").find("a", {
            "title": player_name
        })["href"].replace("#vid", "")

        return int(tab_id)

    def get_tab_url(self, html, i):
        """ 
            Get tab url only supports : 
            -   YourUpload
            -   Fireload
        """
        soup = BeautifulSoup(html, "lxml")
        s = soup.find("div", {
            "class": "player-container"
        }).find("script").string
        tabs = [tab.strip() for tab in s.strip().split("\n")]
        tabs.pop(0)
        tabs = [tab.split('"')[1] for tab in tabs]

        frames = []
        for tab in tabs:
            if not tab:
                continue
            f_soup = BeautifulSoup(tab, "lxml")
            f = f_soup.find("iframe")["src"]
            frames.append(f)

        return frames[i - 1]

    def get_embed_url(self, anime_slug: str, chapter: int) -> Generator[str, None, None]:
        """ 
        Get embed url

        Parameters
        ----------
        anime_slug  (str)   example: overlord
        chapter     (int)   example: 1
        """

        url = self.base_url + f"/ver/{anime_slug}-{chapter}"
        res = requests.get(url)
        html = res.text

        # * Get player by get_multimedia_players method
        players = self.get_multimedia_players(anime_slug, chapter)
        for player_name in players:
            player = self.import_player(player_name)

            self.player = player
            self.player_name = player_name

            tab_id = self.get_tab_id(html, self.dictionary[player_name])
            tab_url = self.get_tab_url(html, tab_id)
            yield tab_url

    def get_code_of_embed(self, embed_url: str) -> str:
        parsed_url = parse.urlsplit(embed_url)
        qs = dict(parse.parse_qs(parsed_url.query))
        return qs["code"][0]

    def search(self, slug: str) -> str:
        url = self.base_url + f"/animes?q={slug}"
        res = requests.get(url)
        html = res.text
        soup = BeautifulSoup(html, "lxml")
        articles = soup.find_all("article", {
            "class": "serie-card"
        })

        anime_url: str = articles[0].find("figure").find("a")["href"]
        formatted_url = anime_url.replace(self.base_url + "/", "")

        return formatted_url

    def get_multimedia_players(self, slug: str, chapter: int) -> List[str]:
        url = self.base_url + f"/ver/{slug}-{chapter}"
        res = requests.get(url)
        html = res.text
        print(res.status_code)

        if res.status_code >= 400:
            raise HTTPException(res.text)

        soup = BeautifulSoup(html, "lxml")
        dictionary = {
            "Fembed": "fembed",
            "YourUpload": "your_upload",
            "Fireload": "fireload"
        }

        tabs = soup.find("div", {
            "class": "tabs"
        }).find("ul").find_all("a")

        players = []
        for tab in tabs:
            p = dictionary.get(tab["title"], None)
            if not p:
                continue
            players.append(p)

        return players

    def get_multimedia_url(self, slug, chapter) -> Generator[Tuple[str, str], None, None]:
        for embed in self.get_embed_url(slug, chapter):
            print(f"EMBED URL -> {embed}")
            url = self.get_code_of_embed(embed)
            print(f"{self.player.__class__.__name__.upper()} VIDEO ID {url}")
            yield (url, self.player_name)
