from typing import List
from typing import Tuple

from application.afc_service_status_application import AFCServiceStatusApplication
from domain.repository.service_end_to_end_status_repository import ServiceEndToEndStatusRepository
from domain.value_object.service_end_to_end_status_value_object import ServiceEndToEndStatusValueObject
from domain.value_object.service_end_to_end_status_value_object import ServiceEndToEndDapPapStatusValueObject


class AFCServiceStatusApplicationImplementation(AFCServiceStatusApplication):
    def __init__(self, service_end_to_end_status_repository: ServiceEndToEndStatusRepository):
        self.service_end_to_end_status_repository = service_end_to_end_status_repository

    def get_end_to_end_status(self) -> Tuple[Exception, ServiceEndToEndStatusValueObject]:
        return self.service_end_to_end_status_repository.get_end_to_end_status()
    
    def get_end_to_end_dap_and_pap_status(self) -> Tuple[Exception, ServiceEndToEndDapPapStatusValueObject]:
        return self.service_end_to_end_status_repository.get_end_to_end_dap_and_pap_status()
