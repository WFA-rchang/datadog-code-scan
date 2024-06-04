from typing import Tuple, List

from application.system_health import SystemHealthApplication
from domain.entity.system_health_domain import SystemHealthDomain


class SystemHealthApplicationImplementation(SystemHealthApplication):
    def __init__(self, system_health_repository):
        self.system_health_repository = system_health_repository

    def get_system_health(self, system_names: List[str], env: str) -> Tuple[Exception, List[SystemHealthDomain]]:
        return self.system_health_repository.get_system_health(system_names, env)
