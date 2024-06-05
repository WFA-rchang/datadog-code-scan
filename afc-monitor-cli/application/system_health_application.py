from typing import List
from abc import ABC, abstractmethod


class SystemHealthApplication(ABC):
    @abstractmethod
    def get_system_health(self, system_names: List[str], env: str):
        pass
