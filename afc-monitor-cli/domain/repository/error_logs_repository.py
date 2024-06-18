from typing import Tuple
from abc import ABC, abstractmethod

from domain.value_object.error_logs_value_object import ErrorLogsValueObject

class ErrorLogsRepository(ABC):
    @abstractmethod
    def get_error_logs(self) -> Tuple[Exception, ErrorLogsValueObject]:
        pass
