from typing import Optional
from typing import Tuple, List
from collections import defaultdict
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



class ErrorLogsRepositoryImplementation(ErrorLogsRepository):
    def __init__(self, datadog_site: str, datadog_api_key: str, datadog_app_key: str, datadog_error_logs_status: str, datadog_error_logs_env_tag: str, datadog_error_logs_index: str):
        self.datadog_site = datadog_site
        self.datadog_api_key = datadog_api_key
        self.datadog_app_key = datadog_app_key
        self.datadog_error_logs_status = datadog_error_logs_status
        self.datadog_error_logs_env_tag = datadog_error_logs_env_tag
        self.datadog_error_logs_index = datadog_error_logs_index

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
                query=f"{self.datadog_error_logs_status} AND {self.datadog_error_logs_env_tag}",
                indexes=[self.datadog_error_logs_index],
                _from="now-86400s",
                to="now"
            ),
            compute=[LogsCompute(
                aggregation=LogsAggregationFunction.COUNT
            )],
            group_by=[LogsGroupBy(
                facet="message",
                total=LogsGroupByTotal(
                    compute=LogsCompute(
                        aggregation=LogsAggregationFunction.COUNT
                    )
                ),
                limit=10000
            )]
        )

        with ApiClient(configuration) as api_client:
            api_instance = LogsApi(api_client)
            try:
                response = api_instance.aggregate_logs(body=body)

                # Convert the data to a list for processing
                buckets = list(response.data.buckets)

                total_logs_count = 0
                pattern_count_dict = defaultdict(int)

                # Iterate through each bucket and collect message patterns and counts
                for bucket in buckets:
                    message = bucket.by.get('message', 'N/A')
                    count = bucket.computes.get('c0', 0)  # Get the count value

                    # Extract total count
                    if message == '__TOTAL__':
                        total_logs_count = count
                        continue

                    pattern_count_dict[message] += count

                # Print sorted results and show logs for each cluster
                sorted_patterns = sorted(pattern_count_dict.items(), key=lambda x: x[1], reverse=True)

                error_logs_pattern_count_value_object_list = []
                for pattern, count in sorted_patterns:
                    error_logs_pattern_count_value_object = ErrorLogsPatternCountValueObject(
                        pattern=pattern, 
                        count=count
                    )
                    error_logs_pattern_count_value_object_list.append(error_logs_pattern_count_value_object)

                error_logs = ErrorLogsValueObject(
                    error_logs_overall=ErrorLogsOverallValueObject(
                        total_pattern_count=len(pattern_count_dict),
                        total_logs_count=total_logs_count
                    ),
                    error_logs_pattern_counts=error_logs_pattern_count_value_object_list
                )
                    
                return None, error_logs    

            except Exception as e:
                return e, []
    