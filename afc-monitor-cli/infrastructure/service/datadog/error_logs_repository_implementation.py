from typing import Optional
from typing import Tuple, List
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.model.logs_compute import LogsCompute
from datadog_api_client.v2.model.logs_group_by import LogsGroupBy
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_group_by_total import LogsGroupByTotal
from datadog_api_client.v2.model.logs_aggregate_request import LogsAggregateRequest
from datadog_api_client.v2.model.logs_aggregation_function import LogsAggregationFunction

from domain.repository.error_logs_repository import ErrorLogsRepository
from domain.value_object.error_logs_value_object import ErrorLogsValueObject
from domain.value_object.error_logs_value_object import ErrorLogsOverallValueObject
from domain.value_object.error_logs_value_object import ErrorLogsPatternCountValueObject
from domain.value_object.error_logs_value_object import ErrorLogsServiceCountValueObject


class ErrorLogsRepositoryImplementation(ErrorLogsRepository):
    def __init__(self, datadog_site: str, datadog_api_key: str, datadog_app_key: str, env_tag: str):
        self.datadog_site = datadog_site
        self.datadog_api_key = datadog_api_key
        self.datadog_app_key = datadog_app_key
        self.env_tag = env_tag

    def get_error_logs(self) -> Tuple[Optional[Exception], ErrorLogsValueObject]:
        configuration = Configuration(
            api_key={
                "apiKeyAuth": self.datadog_api_key,
                "appKeyAuth": self.datadog_app_key
            },
            server_variables={
                "site": self.datadog_site
            }
        )

        body = LogsAggregateRequest(
            filter=LogsQueryFilter(
                query=f"env:{self.env_tag} status:error ",
                indexes=["*"],
                _from="now-86400s",
                to="now"
            ),
            compute=[LogsCompute(
                aggregation=LogsAggregationFunction.COUNT
            )],
            group_by=[
                LogsGroupBy(
                    facet="service",
                    total=LogsGroupByTotal(
                        compute=LogsCompute(
                            aggregation=LogsAggregationFunction.COUNT
                        )
                    ),
                    limit=20
                ),
                LogsGroupBy(
                    facet="message",
                    total=LogsGroupByTotal(
                        compute=LogsCompute(
                            aggregation=LogsAggregationFunction.COUNT
                        )
                    ),
                    limit=500
                )]
        )

        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            try:
                response = api_instance.aggregate_logs(body=body)
                # Convert the data to a list for processing
                buckets = list(response.data.buckets)

                total_logs_count = 0
                '''
                {
                  "OpenAFC": {
                    "ERROR:...": 11
                  }
                }
                '''
                pattern_count_dict = {}
                '''
                {
                  "OpenAFC": 11
                }
                '''
                service_count_dict = {}

                # Iterate through each bucket and collect message patterns and counts
                for bucket in buckets:
                    message = bucket.by.get('message', 'N/A')
                    service = bucket.by.get('service', 'Unknown Service')
                    count = bucket.computes.get('c0', 0)  # Get the count value

                    # Skip empty messages
                    if not message:
                        continue
                    # Extract total count and rename it to TOTAL
                    if message == '__TOTAL__':
                        if service == '__TOTAL__':
                            service = "TOTAL"
                        service_count_dict[service] = count
                        continue

                    if service not in pattern_count_dict:
                        pattern_count_dict[service] = {}
                    pattern_count_dict[service][message] = count

                # Initialize a dictionary to store sorted patterns per service.
                sorted_services = dict(sorted(service_count_dict.items(), key=lambda service_count: service_count[1], reverse=True))
                sorted_services_patterns = {}
                for service, pattern in pattern_count_dict.items():
                    sorted_patterns = dict(sorted(pattern.items(), key=lambda pattern_count: pattern_count[1], reverse=True))
                    sorted_services_patterns[service] = sorted_patterns

                # Initialize a list to hold pattern count value objects.
                error_logs_pattern_count_value_object_list = []
                for service, patterns in sorted_services_patterns.items():
                    for message, count in patterns.items():
                        error_logs_pattern_count_value_object = ErrorLogsPatternCountValueObject(
                            pattern=message,
                            service=service,
                            count=count
                        )
                        error_logs_pattern_count_value_object_list.append(error_logs_pattern_count_value_object)
                        
                # Initialize a list to hold service count value objects.
                error_logs_service_count_value_object_list = []
                for service, count in sorted_services.items():
                    error_logs_service_count_value_object = ErrorLogsServiceCountValueObject(
                        service=service,
                        count=count
                    )
                    error_logs_service_count_value_object_list.append(error_logs_service_count_value_object)
                
                # Create the final error logs value object containing all data about error logs.
                error_logs = ErrorLogsValueObject(
                    error_logs_overall=ErrorLogsOverallValueObject(
                        total_pattern_count=len(pattern_count_dict),
                        total_logs_count=total_logs_count
                    ),
                    error_logs_pattern_counts=error_logs_pattern_count_value_object_list,
                    error_logs_service_counts=error_logs_service_count_value_object_list
                )
                return None, error_logs
            except Exception as e:
                return e, []
