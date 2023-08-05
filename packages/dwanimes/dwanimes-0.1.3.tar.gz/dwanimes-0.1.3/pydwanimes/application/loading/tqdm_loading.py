from pydwanimes.domain import Loading
from tqdm import tqdm


class TqdmLoading(Loading):
    def start(self, total_size: int):
        self.progress_bar = tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            desc="Downloading",
            ascii=True
        )

    def update(self, size: int):
        self.progress_bar.update(size)

    def end(self):
        if not self.progress_bar:
            return
        self.progress_bar.close()
