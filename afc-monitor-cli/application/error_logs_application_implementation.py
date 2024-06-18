from typing import List
from typing import Tuple

from application.error_logs_application import ErrorLogsApplication
from domain.repository.error_logs_repository import ErrorLogsRepository
from domain.value_object.error_logs_value_object import ErrorLogsValueObject


class ErrorLogsApplicationImplementation(ErrorLogsApplication):
    def __init__(self, error_logs_repository: ErrorLogsRepository):
        self.error_logs_repository = error_logs_repository

    def get_error_logs(self) -> Tuple[Exception, ErrorLogsValueObject]:
        return self.error_logs_repository.get_error_logs()
