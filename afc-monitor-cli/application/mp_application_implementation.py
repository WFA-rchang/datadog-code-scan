from typing import List
from typing import Tuple

from domain.entity.nra_domain import NRADomain
from domain.entity.device_domain import DeviceDomain
from application.mp_application import MPApplication
from domain.repository.nra_repository import NRARepository
from domain.repository.device_repository import DeviceRepository
from domain.repository.contract_repository import ContractRepository
from domain.repository.query_call_repository import QueryCallRepository
from domain.value_object.company_contracts_usages_value_object import CompanyContractsUsagesValueObject
from domain.value_object.company_query_call_usages_value_object import CompanyQueryCallUsagesValueObject


class MPApplicationImplementation(MPApplication):
    def __init__(self, nra_repository: NRARepository, contract_repository: ContractRepository,
                 device_repository: DeviceRepository, query_call_repository: QueryCallRepository):
        self.nra_repository = nra_repository
        self.contract_repository = contract_repository
        self.device_repository = device_repository
        self.query_call_repository = query_call_repository

    def get_nras(self) -> Tuple[Exception, List[NRADomain]]:
        return self.nra_repository.get_nras()

    def get_companies_contracts_usages(self) -> Tuple[Exception, List[CompanyContractsUsagesValueObject]]:
        return self.contract_repository.get_companies_contracts_usages()

    def get_registered_devices_in_period(self, period: str = '1d') -> Tuple[Exception, List[DeviceDomain]]:
        return self.device_repository.get_registered_devices_in_period(period)

    def get_query_call_usages_in_period(self, period: str = '1d') -> Tuple[Exception, List[CompanyQueryCallUsagesValueObject]]:
        return self.query_call_repository.get_query_call_usages_in_period(period)
