from typing import List, Tuple
from application.scheduler_status_application import SchedulerStatusApplication
from domain.value_object.scheduler_status_value_object import SchedulerStatusValueObject



class SchedulerStatusApplicationImplementation(SchedulerStatusApplication):
  def __init__(self, scheduler_status_repository, default_env):
    self.scheduler_status_repository = scheduler_status_repository
    self.default_env = default_env

  def get_scheduler_status(self, scheduler_names: List[str], env: str) -> Tuple[Exception, List[SchedulerStatusValueObject]]:
    if env is None:
      env = self.default_env
    return self.scheduler_status_repository.get_scheduler_status(scheduler_names, env)