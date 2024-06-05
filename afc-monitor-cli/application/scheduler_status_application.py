from typing import List
from abc import ABC, abstractmethod

class SchedulerStatusApplication(ABC):
  @abstractmethod
  def get_scheduler_status(self, scheduler_names: List[str], env: str):
    pass