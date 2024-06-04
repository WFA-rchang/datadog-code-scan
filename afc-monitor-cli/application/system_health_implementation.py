from typing import Tuple, List

from application.system_health import SystemHealthApplication
from domain.value_object.system_health_value_object import SystemHealthValueObject


class SystemHealthApplicationImplementation(SystemHealthApplication):
    def __init__(self, system_health_repository, default_env):
        self.system_health_repository = system_health_repository
        self.default_env = default_env

    def get_system_health(self, system_names: List[str], env: str) -> Tuple[Exception, List[SystemHealthValueObject]]:
        if env is None:
            env = self.default_env
        return self.system_health_repository.get_system_health(system_names, env)
