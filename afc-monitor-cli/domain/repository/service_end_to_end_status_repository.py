from typing import Tuple, List
from abc import ABC, abstractmethod

from domain.value_object.service_end_to_end_status_value_object import ServiceEndToEndStatusValueObject


class ServiceEndToEndStatusRepository(ABC):
    @abstractmethod
    def get_end_to_end_status(self) -> Tuple[Exception, ServiceEndToEndStatusValueObject]:
        pass
