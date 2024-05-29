from abc import ABC, abstractmethod


class MPApplication(ABC):
    @abstractmethod
    def get_nras():
        pass
