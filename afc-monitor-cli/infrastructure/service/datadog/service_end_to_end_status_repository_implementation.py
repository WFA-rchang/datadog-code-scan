from typing import Tuple, List
from typing import Optional
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.monitors_api import MonitorsApi

from domain.repository.service_end_to_end_status_repository import ServiceEndToEndStatusRepository
from domain.value_object.service_end_to_end_status_value_object import ServiceEndToEndStatusValueObject
from domain.value_object.service_end_to_end_status_value_object import ServiceEndToEndRegionStatusValueObject
from domain.value_object.service_end_to_end_status_value_object import ServiceEndToEndDapPapStatusValueObject
from domain.value_object.service_end_to_end_status_value_object import ServiceEndToEndDapPapRegionStatusValueObject



class ServiceEndToEndStatusRepositoryImplementation(ServiceEndToEndStatusRepository):
    def __init__(self, datadog_site: str, datadog_api_key: str, datadog_app_key: str, datadog_monitor_mtls_env_tag: str, datadog_monitor_dap_pap_env_tag: str, env_tag:str):
        self.datadog_site = datadog_site
        self.datadog_api_key = datadog_api_key
        self.datadog_app_key = datadog_app_key
        self.datadog_monitor_mtls_env_tag = datadog_monitor_mtls_env_tag
        self.datadog_monitor_dap_pap_env_tag = datadog_monitor_dap_pap_env_tag
        self.env_tag = env_tag

    def get_end_to_end_status(self) -> Tuple[Optional[Exception], ServiceEndToEndStatusValueObject]:
        # Datadog Search Monitor API
        configuration = Configuration(
            api_key={
                "apiKeyAuth": self.datadog_api_key,
                "appKeyAuth": self.datadog_app_key
            },
            server_variables={
                "site": self.datadog_site
            }
        )

        try:
            with ApiClient(configuration) as api_client:
                api_instance = MonitorsApi(api_client)
                mtls_response = api_instance.search_monitor_groups(query=self.datadog_monitor_mtls_env_tag)

                # Create a list to store all status information
                end_to_end_status_value_object = ServiceEndToEndStatusValueObject()
                total_group_info = None

                # Extract 'group' and 'status' from groups
                mtls_response ['groups'].sort(key=lambda x: x["group"])
                for group_info in mtls_response ['groups']:
                    region = group_info.get('group')
                    status = group_info.get('status')
                    
                    if region == 'total':
                        total_group_info = ServiceEndToEndRegionStatusValueObject(region=region, status=status)
                        end_to_end_status_value_object.regions_status.insert(0, total_group_info)
                    else:
                        region_status_value_object = ServiceEndToEndRegionStatusValueObject(region=region, status=status)
                        end_to_end_status_value_object.regions_status.append(region_status_value_object)
            return None, end_to_end_status_value_object

        except Exception as e:
            return e, None
        
    
    def get_end_to_end_dap_and_pap_status(self) -> Tuple[Optional[Exception], ServiceEndToEndDapPapStatusValueObject]:
        # Datadog Search Monitor API
        configuration = Configuration(
            api_key={
                "apiKeyAuth": self.datadog_api_key,
                "appKeyAuth": self.datadog_app_key
            },
            server_variables={
                "site": self.datadog_site
            }
        )
        
        try:
            with ApiClient(configuration) as api_client:
                api_instance = MonitorsApi(api_client)
                query = f"{self.datadog_monitor_dap_pap_env_tag} AND env:{self.env_tag}"
                dap_and_pap_response = api_instance.search_monitor_groups(query=query)
                
                # Create a list to store all status information
                dap_and_pap_status_value_object = ServiceEndToEndDapPapStatusValueObject()

                # Extract 'monitor_name', 'total' and 'status' from groups
                for group_info in dap_and_pap_response ['groups']:
                    monitor_name = group_info.get('monitor_name')
                    region = group_info.get('group')
                    status = group_info.get('status')

                    dap_and_pap_status_info = ServiceEndToEndDapPapRegionStatusValueObject(monitor_name=monitor_name, region=region, status=status)
                    dap_and_pap_status_value_object.regions_status.append(dap_and_pap_status_info)
            return None, dap_and_pap_status_value_object

        except Exception as e:
            return e, None