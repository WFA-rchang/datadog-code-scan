from typing import Tuple, List
from abc import ABC, abstractmethod

from domain.entity.device_domain import DeviceDomain


class DeviceRepository(ABC):
    @abstractmethod
    def get_registered_devices_in_period(period: str) -> Tuple[Exception, List[DeviceDomain]]:
        pass
