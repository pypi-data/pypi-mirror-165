from abc import ABC, abstractmethod


class Loading(ABC):
    @abstractmethod
    def start(self, total_size: int):
        pass

    @abstractmethod
    def update(self, size: int):
        pass

    @abstractmethod
    def end(self):
        pass
