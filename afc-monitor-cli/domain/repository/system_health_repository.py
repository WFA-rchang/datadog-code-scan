from typing import List
from typing import Tuple
from abc import ABC, abstractmethod

from domain.entity.system_health_domain import SystemHealthDomain


class SystemHealthRepository(ABC):
    @abstractmethod
    def get_system_health(self, system_names: List[str], env: str) -> Tuple[Exception, List[SystemHealthDomain]]:
        pass
