from typing import List
from typing import Tuple
from abc import ABC, abstractmethod

from domain.value_object.scheduler_status_value_object import SchedulerStatusValueObject


class SchedulerStatusRepository(ABC):
    @abstractmethod
    def get_scheduler_status(self,  scheduler_names: List[str], env: str) -> Tuple[Exception, List[SchedulerStatusValueObject]]:
        pass
