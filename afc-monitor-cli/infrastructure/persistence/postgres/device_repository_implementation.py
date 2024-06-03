import logging
from typing import List
from typing import Tuple
from sqlalchemy import and_
from sqlalchemy import func
from sqlalchemy import text
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from domain.entity.nra_domain import NRADomain
from domain.entity.device_domain import DeviceDomain
from domain.entity.company_domain import CompanyDomain
from domain.entity.contract_domain import ContractDomain
from domain.repository.device_repository import DeviceRepository

from infrastructure.persistence.postgres.dao.nra_dao import NRADAO
from infrastructure.persistence.postgres.dao.device_dao import DeviceDAO
from infrastructure.persistence.postgres.dao.license_dao import LicenseDAO
from infrastructure.persistence.postgres.dao.company_dao import CompanyDAO
from infrastructure.persistence.postgres.dao.contract_dao import ContractDAO


logger = logging.getLogger(__name__)


class DeviceRepositoryImplementation(DeviceRepository):
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_registered_devices_in_period(self, period: str) -> Tuple[Exception, List[DeviceDomain]]:
        device_list = []
        try:
            with Session(self.engine) as session:
                md = aliased(DeviceDAO, name='md')
                mna = aliased(NRADAO, name='mna')
                mco = aliased(CompanyDAO, name='mco')
                ml = aliased(LicenseDAO, name='ml')
                mc = aliased(ContractDAO, name='mc')

                statement = select(
                    mco.name.label("company_name"),
                    mna.ruleset_id,
                    mna.certification_id,
                    md.serial_number,
                    md.license_id,
                    mc.contract_group_id,
                    mc.monthly_bucket
                ).join(
                    mna, md.auth_id == mna.id
                ).join(
                    mco, md.company_id == mco.id
                ).join(
                    ml, md.license_id == ml.id
                ).join(
                    mc, mc.id == ml.contract_id
                ).where(
                    and_(
                        md.created_at >= text(f"current_date - INTERVAL '{period}'"),
                        md.created_at < func.current_date()
                    )
                ).order_by(
                    mco.name,
                    mna.ruleset_id,
                    md.serial_number,
                    mc.contract_group_id,
                    mc.monthly_bucket
                )

                result = session.execute(statement).all()
                for row in result:
                    company = CompanyDomain(
                        name=row.company_name
                    )
                    nra = NRADomain(
                        ruleset_id=row.ruleset_id,
                        certification_id=row.certification_id
                    )
                    contract = ContractDomain(
                        contract_group_id=row.contract_group_id,
                        monthly_bucket=row.monthly_bucket
                    )
                    device = DeviceDomain(
                        serial_number=row.serial_number,
                        license_id=row.license_id,
                        company=company,
                        nra=nra,
                        contract=contract
                    )
                    device_list.append(device)
                return None, device_list
        except Exception as e:
            return e, []
