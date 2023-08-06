from abc import ABC, abstractmethod
from http.client import HTTPException
import os
from requests import Response
from pathlib import Path

import pydwanimes.domain.loading as loading


class Player(ABC):
    def __init__(self, directory: str, extension: str = None, loading: loading.Loading = False) -> None:
        """
        Params:
        -
        -   dir         (str)      Directory where save files
        -   extension   (str)      Extension of file -> default : .mp4
        -   loading     (Loading)  Loading class to handle file process  -> default : TqdmLoading
        """
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        if not extension:
            self.extension = ".mp4"
        self.loading = loading
        self.directory = directory

    def compose_video_dir(self, filename: str) -> str:
        if not self.extension in filename:
            filename += self.extension
        return os.path.join(self.directory, filename)

    def process_file(self, res: Response, file_dir: str, chunk_size: int = None) -> None:
        """ Process and save video """
        if not chunk_size:
            chunk_size = 1024*1024

        if res.status_code >= 400:
            error_args = {"content": res.text, "status_code": res.status_code}
            raise HTTPException(error_args)

        with open(file_dir, "wb") as f:
            if self.loading:
                size = int(res.headers.get("content-length", 0))
                self.loading.start(size)

            for chunk in res.iter_content(chunk_size=chunk_size):
                if self.loading:
                    self.loading.update(len(chunk))
                if chunk:
                    f.write(chunk)

            if self.loading:
                self.loading.end()

    @abstractmethod
    def download(self, video_id: str, filename: str) -> None:
        pass
