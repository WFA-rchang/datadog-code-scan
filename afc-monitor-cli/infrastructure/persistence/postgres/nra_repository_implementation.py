from typing import List
from typing import Tuple
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from domain.entity.nra_domain import NRADomain
from domain.repository.nra_repository import NRARepository
from infrastructure.persistence.postgres.dao.nra_dao import NRADAO


class NRARepositoryImplementation(NRARepository):
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_nras(self) -> Tuple[Exception, List[NRADomain]]:
        nras_domain_list = []
        try:
            with Session(self.engine) as session:
                nras = session.query(NRADAO) \
                              .order_by(NRADAO.ruleset_id, NRADAO.certification_id) \
                              .all()
                
                for nra in nras:
                    nra_domain = NRADomain(id=nra.id, certification_id=nra.certification_id, 
                                           is_authed=nra.is_authed, ruleset_id=nra.ruleset_id, 
                                           deployment_type=nra.deployment_type)
                    nras_domain_list.append(nra_domain)
                return None, nras
        except Exception as e:
            return e, []
