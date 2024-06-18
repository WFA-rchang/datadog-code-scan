from typing import List
from typing import Tuple
from abc import ABC, abstractmethod

from domain.value_object.error_logs_value_object import ErrorLogsValueObject


class ErrorLogsApplication(ABC):
    @abstractmethod
    def get_error_logs() -> Tuple[Exception, ErrorLogsValueObject]:
        pass
