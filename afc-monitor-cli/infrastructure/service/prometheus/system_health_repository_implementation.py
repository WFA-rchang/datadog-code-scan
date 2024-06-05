import logging
from typing import List, Tuple
from prometheus_api_client import PrometheusConnect
from concurrent.futures import ThreadPoolExecutor, as_completed

from domain.value_object.system_health_value_object import SystemHealthValueObject
from domain.repository.system_health_repository import SystemHealthRepository


class SystemHealthRepositoryImplementation(SystemHealthRepository):
    def __init__(self, prometheus_connect: PrometheusConnect):
        self.prometheus_connect = prometheus_connect

    def get_system_health(self, system_names, env) -> Tuple[Exception, List[SystemHealthValueObject]]:

        # define params for prometheus api
        metric_name = "kube_deployment_status_replicas_ready"

        deployments = {
            'als-viewer': {
                'name': 'als-viewer-wifi-afc-als-viewer',
                'namespace': 'afc-als-viewer',
            },
            'msghnd': {
                'name': 'afc-msghnd',
                'namespace': 'open-afc',
            },
            'cp': {
                'name': 'cp-wifi-afc-cp',
                'namespace': 'afc-cp',
            },
            'mp-backend': {
                'name': 'mp-backend-wifi-afc-mp-backend',
                'namespace': 'afc-mp',
            },
            'mp-frontend': {
                'name': 'mp-frontend-wifi-afc-mp-frontend',
                'namespace': 'afc-mp',
            },
            'mp-helper': {
                'name': 'mp-helper-wifi-afc-mp-helper',
                'namespace': 'afc-mp',
            },
            'mp-management-nginx': {
                'name': 'mp-management-nginx-wifi-afc-mp-management-nginx',
                'namespace': 'afc-cp',
            },
        }

        metrics_tag_name_map = {
            'mp-backend-wifi-afc-mp-backend': 'mp-backend',
            'mp-frontend-wifi-afc-mp-frontend': 'mp-frontend',
            'mp-helper-wifi-afc-mp-helper': 'mp-helper',
            'mp-management-nginx-wifi-afc-mp-management-nginx': 'mp-management-nginx',
            'cp-wifi-afc-cp': 'cp',
            'als-viewer-wifi-afc-als-viewer': 'als-viewer',
            'afc-msghnd': 'msghnd'
        }

        labels = []

        if len(system_names) == 0:
            system_names = deployments.keys()

        for system in system_names:
            if system in deployments:
                cluster = f"afc-{env}"
                labels.append(
                    {
                        'deployment': deployments[system]['name'],
                        'cluster': cluster,
                        'namespace': f"{deployments[system]['namespace']}"
                    }
                )

        # fetch metrics from prometheus api
        futures_list = []
        try:
            with ThreadPoolExecutor() as executor:
                for label in labels:
                    future = executor.submit(self.prometheus_connect.get_current_metric_value, metric_name=metric_name, label_config=label)
                    futures_list.append(future)
            prometheus_metrics_list = []
            for future in as_completed(futures_list):
                prometheus_metrics_list.extend(future.result())
        except Exception as e:
            logging.error(f"Error while fetching metrics: {e}")
            return e, []

        # make metrics list and do sorting and grouping
        metrics_list = []
        for metrics_object in prometheus_metrics_list:
            status = ''
            current_replicas = metrics_object['value'][1]
            if current_replicas != '0':
                status = 'OK'
            else:
                status = 'Failed'
            metrics_list.append(
                SystemHealthValueObject(
                    name=metrics_tag_name_map[metrics_object['metric']['deployment']],
                    status=status
                )
            )
        return None, metrics_list
