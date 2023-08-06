import requests
from http.client import HTTPException
from pydwanimes.domain import Player


class Fembed(Player):
    base_url = "https://vanfem.com"

    def get_file_url(self, video_id: str):
        return self.base_url + "/f/" + video_id

    def get_headers(self):
        return {
            "Referer": self.base_url + "/"
        }

    def get_file_source(self, video_id: str):
        url = self.base_url + "/api/source/" + video_id
        res = requests.post(url, headers=self.get_headers())
        body = res.json()
        success = body["success"]

        if not success:
            raise HTTPException({
                "code": res.status_code,
                "success": success,
                "message": body["data"]
            })

        files = body["data"]

        for f in files:
            if not f["label"] == "720p":
                continue
            return f

    def download(self, video_id: str, filename: str) -> None:
        f = self.get_file_source(video_id)
        url = f["file"]
        res = requests.get(url, headers=self.get_headers(), stream=True)

        print(f"REQUEST VIDEO STATUS -> {res.status_code}")
        if res.status_code == 404:
            raise HTTPException({
                "code": res.status_code,
                "message": "Cannot found video"
            })

        video_dir = self.compose_video_dir(filename)
        self.process_file(res, video_dir)
