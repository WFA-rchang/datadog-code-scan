from typing import List
from typing import Tuple

from domain.entity.nra_domain import NRADomain
from application.mp_application import MPApplication
from domain.repository.nra_repository import NRARepository


class MPApplicationImplementation(MPApplication):
    def __init__(self, nra_repository: NRARepository):
        self.nra_repository = nra_repository

    def get_nras(self) -> Tuple[Exception, List[NRADomain]]:
        return self.nra_repository.get_nras()
