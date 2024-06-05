import logging
from typing import Tuple, List
from prometheus_api_client import PrometheusConnect
from concurrent.futures import ThreadPoolExecutor, as_completed
from domain.repository.scheduler_status_repository import SchedulerStatusRepository
from domain.value_object.scheduler_status_value_object import SchedulerStatusValueObject

class SchedulerStatusRepositoryImplementation(SchedulerStatusRepository):
    def __init__(self, prometheus_connect: PrometheusConnect):
        self.prometheus_connect = prometheus_connect

    def get_scheduler_status(self, scheduler_names, env) -> Tuple[Exception, List[SchedulerStatusValueObject]]:
        metric_name = "argo_workflows_scheduler_execution_result"
        schedulers = {
            'helper-auto-release-scheduler': {
                'time': '24h'
            },
            'helper-contract-scheduler': {
                'time': '24h'
            },
            'helper-nra-scheduler': {
                'time': '1h'
            },
            'helper-usage-scheduler': {
                'time': '24h'
            }
        }

        target_scheduler_names = []

        if len(scheduler_names) == 0:
            target_scheduler_names = schedulers.keys()
        else: 
            for scheduler_name in scheduler_names:
                if scheduler_name in schedulers:
                    target_scheduler_names.append(scheduler_name)

        # fetch metrics from prometheus
        futures_list = []
        try:
            with ThreadPoolExecutor() as executor:
                for scheduler_name in target_scheduler_names:
                    query = 'floor(increase({metric_name}{{cluster="afc-{env}", scheduler_name="{scheduler_name}", status="Succeeded"}}[{time}]))'.format(
                        metric_name=metric_name, 
                        scheduler_name=scheduler_name, 
                        time=schedulers[scheduler_name]['time'], 
                        env=env
                    )
                    future = executor.submit(self.prometheus_connect.custom_query, query=query)
                    futures_list.append(future)

            prometheus_metrics_list = []
            for future in as_completed(futures_list):
                if (len(prometheus_metrics_list) == 0):
                    prometheus_metrics_list = future.result()
                else:
                    prometheus_metrics_list += future.result()
        except Exception as e:
            logging.error(f"Error while fetching metrics: {e}")
            return e, []
        
        metrics_list = []
        for metrics_object in prometheus_metrics_list:
            status = ''
            execution_success_times = metrics_object['value'][1]
            if int(execution_success_times) >= 1 :
                status = 'OK'
            elif int(execution_success_times) == 0:
                status = 'Failed'
            else:
                status = 'Unknown'

            metrics_list.append(
                SchedulerStatusValueObject(
                    name=metrics_object['metric']['scheduler_name'],
                    status=status
                )
            )
        return None, metrics_list
    

    