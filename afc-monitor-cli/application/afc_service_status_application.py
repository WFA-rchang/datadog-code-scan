from typing import List
from typing import Tuple
from abc import ABC, abstractmethod

from domain.value_object.service_end_to_end_status_value_object import ServiceEndToEndStatusValueObject


class AFCServiceStatusApplication(ABC):
    @abstractmethod
    def get_end_to_end_status() -> Tuple[Exception, ServiceEndToEndStatusValueObject]:
        pass
