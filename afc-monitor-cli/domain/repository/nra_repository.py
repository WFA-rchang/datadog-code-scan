from typing import Tuple, List
from abc import ABC, abstractmethod

from domain.entity.nra_domain import NRADomain


class NRARepository(ABC):
    @abstractmethod
    def get_nras(self) -> Tuple[Exception, List[NRADomain]]:
        pass
