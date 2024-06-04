from typing import List
from typing import Tuple
from abc import ABC, abstractmethod

from domain.value_object.system_health_value_object import SystemHealthValueObject


class SystemHealthRepository(ABC):
    @abstractmethod
    def get_system_health(self, system_names: List[str], env: str) -> Tuple[Exception, List[SystemHealthValueObject]]:
        pass
