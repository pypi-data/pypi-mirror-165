import requests
from http.client import HTTPException
from pydwanimes.domain import Player
from bs4 import BeautifulSoup


class YourUpload(Player):
    base_url = "https://www.yourupload.com"

    @property
    def embed_url(self):
        return f"{self.base_url}/embed"

    @property
    def watch_url(self):
        return f"{self.base_url}/watch"

    def get_watch_page(self, multimedia_id: str) -> str:
        url = self.watch_url + f"/{multimedia_id}"
        res = requests.get(url)

        if res.status_code == 404:
            raise HTTPException({
                "code": res.status_code,
                "message": "Cannot found video"
            })
        html = res.text

        soup = BeautifulSoup(html, "lxml")
        dw_url = soup.find("a", {
            "class": "btn btn-success"
        })["href"]

        return self.base_url + dw_url

    def get_download_url(self, multimedia_id: str) -> str:
        url = self.get_watch_page(multimedia_id)

        print("Getting download page")
        res = requests.get(url)

        if res.status_code == 404:
            raise HTTPException({
                "code": res.status_code,
                "message": "Cannot found video"
            })

        html = res.text
        soup = BeautifulSoup(html, "lxml")
        dw_url = soup.find("a", {
            "class": "btn btn-success"
        })["data-url"]
        print("Download url getted !!")
        return self.base_url + dw_url

    def download(self, video_id: str, filename: str) -> None:
        video_dir = self.compose_video_dir(filename)
        print("Fetching download url ...")
        url = self.get_download_url(video_id)
        print("Download url fetched !!")

        print("Downloading video ...")
        print(f"Download video url -> {url}")
        res = requests.get(url, stream=True, headers={
            "Referer": "https://www.yourupload.com/"
        })

        if res.status_code == 404:
            raise HTTPException({
                "code": res.status_code,
                "message": "Cannot found video"
            })
        self.process_file(res, video_dir)
        print(f"Downloaded {filename} !!")
