from typing import Tuple, List
from abc import ABC, abstractmethod

from domain.value_object.company_query_call_usages_value_object import CompanyQueryCallUsagesValueObject


class QueryCallRepository(ABC):
    @abstractmethod
    def get_query_call_usages_in_period(period: str) -> Tuple[Exception, List[CompanyQueryCallUsagesValueObject]]:
        pass
