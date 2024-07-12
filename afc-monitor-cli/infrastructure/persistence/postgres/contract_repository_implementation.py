import logging
from typing import (
    List,
    Tuple,
)

from sqlalchemy import select
from sqlalchemy.orm import (
    Session,
    aliased,
)
from sqlalchemy.engine import Engine
from domain.repository.contract_repository import ContractRepository
from infrastructure.persistence.postgres.dao.company_dao import CompanyDAO
from infrastructure.persistence.postgres.dao.contract_dao import ContractDAO
from domain.value_object.company_contracts_usages_value_object import (
    MonthlyBucketUsageValueObject,
    ContractGroupUsagesValueObject,
    CompanyContractsUsagesValueObject,
)
from infrastructure.persistence.postgres.dao.contract_group_dao import ContractGroupDAO

logger = logging.getLogger(__name__)


class ContractRepositoryImplementation(ContractRepository):
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_companies_contracts_usages(self) -> Tuple[Exception, List[CompanyContractsUsagesValueObject]]:
        company_contracts_usages_list = []
        try:
            with Session(self.engine) as session:
                mc = aliased(ContractDAO, name='mc')
                mcg = aliased(ContractGroupDAO, name='mcg')
                mco = aliased(CompanyDAO, name='mco')

                statement = (
                    select(mco.name.label("company_name"), mc.contract_group_id, mc.monthly_bucket, mc.licensed_count)
                    .join(mcg, mc.contract_group_id == mcg.id)
                    .join(mco, mcg.company_id == mco.id)
                    .order_by(mco.name, mc.contract_group_id, mc.monthly_bucket.asc())
                )

                result = session.execute(statement).all()

                # Create model objects
                companies = {}
                for row in result:
                    company_name, contract_group_id, monthly_bucket, licensed_count = row
                    if company_name not in companies:
                        companies[company_name] = {}
                    if contract_group_id not in companies[company_name]:
                        companies[company_name][contract_group_id] = []
                    monthly_bucket = MonthlyBucketUsageValueObject(monthly_bucket, licensed_count)
                    companies[company_name][contract_group_id].append(monthly_bucket)

                for company_name, contract_groups in companies.items():
                    contract_group_usages = []
                    for contract_group_id, monthly_buckets in contract_groups.items():
                        contract_group_usage = ContractGroupUsagesValueObject(contract_group_id, monthly_buckets)
                        contract_group_usages.append(contract_group_usage)
                    company_contract_usage = CompanyContractsUsagesValueObject(company_name, contract_group_usages)
                    company_contracts_usages_list.append(company_contract_usage)
                return None, company_contracts_usages_list
        except Exception as e:
            return e, []
