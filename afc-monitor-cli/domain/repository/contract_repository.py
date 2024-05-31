from typing import Tuple, List
from abc import ABC, abstractmethod

from domain.value_object.company_contracts_usages_value_object import CompanyContractsUsagesValueObject


class ContractRepository(ABC):
    @abstractmethod
    def get_companies_contracts_usages() -> Tuple[Exception, List[CompanyContractsUsagesValueObject]]:
        pass
