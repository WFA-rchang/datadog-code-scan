from typing import (
    List,
    Tuple,
)

from sqlalchemy import (
    and_,
    case,
    func,
    text,
    select,
)
from sqlalchemy.orm import (
    Session,
    aliased,
)
from sqlalchemy.engine import Engine
from domain.repository.query_call_repository import QueryCallRepository
from infrastructure.persistence.postgres.dao.device_dao import DeviceDAO
from infrastructure.persistence.postgres.dao.company_dao import CompanyDAO
from infrastructure.persistence.postgres.dao.query_call_dao import QueryCallDAO
from domain.value_object.company_query_call_usages_value_object import CompanyQueryCallUsagesValueObject


class QueryCallRepositoryImplementation(QueryCallRepository):
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_query_call_usages_in_period(self, period: str) -> Tuple[Exception, List[CompanyQueryCallUsagesValueObject]]:
        query_call_usages_list = []
        try:
            with Session(self.engine) as session:
                mqc = aliased(QueryCallDAO, name='mqc')
                md = aliased(DeviceDAO, name='md')
                mc = aliased(CompanyDAO, name='mc')

                statement = (
                    select(
                        mc.name.label('company_name'),
                        func.count(case((mqc.type == '1', 1), else_=0)).label('normal_usages'),
                        func.count(case((mqc.type == '2', 1), else_=0)).label('channel_evaluation_usages'),
                        func.count().label('total_usages')
                    )
                    .select_from(mqc)
                    .join(md, mqc.device_id == md.id)
                    .join(mc, mc.id == md.company_id)
                    .where(
                        and_(
                            mqc.query_date >= text(f"current_date - INTERVAL '{period}'"),
                            md.created_at < func.current_date(),
                        )
                    )
                    .group_by(mc.name)
                    .order_by(mc.name)
                )

                result = session.execute(statement).all()

                for row in result:
                    company_query_call_usages_value_object = CompanyQueryCallUsagesValueObject(
                        company_name=row.company_name,
                        normal_usages=row.normal_usages,
                        channel_evaluation_usages=row.channel_evaluation_usages,
                        total_usages=row.total_usages,
                    )
                    query_call_usages_list.append(company_query_call_usages_value_object)
                return None, query_call_usages_list
        except Exception as e:
            return e, []
