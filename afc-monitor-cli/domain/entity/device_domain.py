from datetime import datetime

from domain.entity.nra_domain import NRADomain
from domain.entity.company_domain import CompanyDomain
from domain.entity.contract_domain import ContractDomain


class DeviceDomain():
    def __init__(self, id: int = None, serial_number: str = None, license_id: str = None,
                 company: CompanyDomain = None, nra: NRADomain = None, description: str = None,
                 contract: ContractDomain = None, created_at: datetime = None):
        self.id = id
        self.serial_number = serial_number
        self.license_id = license_id
        self.company = company
        self.nra = nra
        self.description = description
        self.contract = contract
        self.created_at = created_at
