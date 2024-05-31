from typing import List
from typing import Tuple

from domain.entity.nra_domain import NRADomain
from application.mp_application import MPApplication
from domain.repository.nra_repository import NRARepository
from domain.repository.device_repository import DeviceRepository
from domain.repository.contract_repository import ContractRepository
from domain.value_object.company_contracts_usages_value_object import CompanyContractsUsagesValueObject


class MPApplicationImplementation(MPApplication):
    def __init__(self, nra_repository: NRARepository, contract_repository: ContractRepository,
                 device_repository: DeviceRepository):
        self.nra_repository = nra_repository
        self.contract_repository = contract_repository
        self.device_repository = device_repository

    def get_nras(self) -> Tuple[Exception, List[NRADomain]]:
        return self.nra_repository.get_nras()

    def get_companies_contracts_usages(self) -> Tuple[Exception, List[CompanyContractsUsagesValueObject]]:
        return self.contract_repository.get_companies_contracts_usages()

    def get_registered_devices_in_period(self, period: str = '1d'):
        return self.device_repository.get_registered_devices_in_period(period)
