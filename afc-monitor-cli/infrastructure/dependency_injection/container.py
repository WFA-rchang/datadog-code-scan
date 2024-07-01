import logging
from dotenv import load_dotenv
from prometheus_api_client import PrometheusConnect
from dependency_injector import containers, providers

from application.mp_application_implementation import MPApplicationImplementation
from application.system_health_application_implementation import SystemHealthApplicationImplementation
from application.scheduler_status_application_implementation import SchedulerStatusApplicationImplementation
from application.afc_service_status_application_implementation import AFCServiceStatusApplicationImplementation
from application.error_logs_application_implementation import ErrorLogsApplicationImplementation
from infrastructure.persistence.postgres.database.engine import PostgresEngineFactory
from infrastructure.persistence.postgres.nra_repository_implementation import NRARepositoryImplementation
from infrastructure.persistence.postgres.device_repository_implementation import DeviceRepositoryImplementation
from infrastructure.persistence.postgres.contract_repository_implementation import ContractRepositoryImplementation
from infrastructure.persistence.postgres.query_call_repository_implementation import QueryCallRepositoryImplementation
from infrastructure.service.prometheus.system_health_repository_implementation import SystemHealthRepositoryImplementation
from infrastructure.service.prometheus.scheduler_status_repository_implementation import SchedulerStatusRepositoryImplementation    
from infrastructure.service.datadog.service_end_to_end_status_repository_implementation import ServiceEndToEndStatusRepositoryImplementation
from infrastructure.service.datadog.error_logs_repository_implementation import ErrorLogsRepositoryImplementation


class Container(containers.DeclarativeContainer):
    # Load .env.local if it exists for environment variables
    load_dotenv('.env.local')

    # Wiring Config
    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=[
            "interface.click.command.proactive_monitor_command",
            "interface.click.command.system_health_command",
            "interface.click.command.scheduler_status_command"
        ],
    )

    # Configuration Provider
    config = providers.Configuration()
    config.db_host.from_env("DB_HOST", required=True)
    config.db_port.from_env("DB_PORT", default="5432")
    config.db_username.from_env("DB_USERNAME", required=True)
    config.db_password.from_env("DB_PASSWORD", required=True)
    config.db_name.from_env("DB_NAME", required=True)
    config.log_level.from_env("LOG_LEVEL", default="INFO")
    config.datadog_site.from_env("DATADOG_SITE", required=True)
    config.datadog_api_key.from_env("DATADOG_API_KEY", required=True)
    config.datadog_app_key.from_env("DATADOG_APP_KEY", required=True)
    config.datadog_monitor_mtls_env_tag.from_env("DATADOG_MONITOR_MTLS_ENV_TAG", required=True)
    config.datadog_monitor_dap_pap_env_tag.from_env("DATADOG_MONITOR_DAP_PAP_ENV_TAG", required=True)
    config.prometheus_host.from_env("PROMETHEUS_HOST", required=True)
    config.prometheus_monitoring_env.from_env("PROMETHEUS_MONITORING_ENV", default="production")
    config.env_tag.from_env("ENV_TAG", required=True)

    # Initialize logging
    logging.basicConfig(level=logging.getLevelName(config.log_level()))

    # SQLAlchemy Engine
    postgres_engine = providers.Singleton(
        PostgresEngineFactory.create_postgres_engine,
        db_host=config.db_host,
        db_port=config.db_port,
        db_username=config.db_username,
        db_password=config.db_password,
        db_name=config.db_name
    )

    # Prometheus Connection
    prometheus_connect = providers.Singleton(
        PrometheusConnect,
        url=config.prometheus_host,
        disable_ssl=True
    )

    # Repositories
    nra_repository = providers.Factory(
        NRARepositoryImplementation,
        engine=postgres_engine
    )

    system_health_repository = providers.Factory(
        SystemHealthRepositoryImplementation,
        prometheus_connect=prometheus_connect
    )

    scheduler_status_repository = providers.Factory(
        SchedulerStatusRepositoryImplementation,
        prometheus_connect=prometheus_connect
    )

    contract_repository = providers.Factory(
        ContractRepositoryImplementation,
        engine=postgres_engine
    )

    device_repository = providers.Factory(
        DeviceRepositoryImplementation,
        engine=postgres_engine
    )

    query_call_repository = providers.Factory(
        QueryCallRepositoryImplementation,
        engine=postgres_engine
    )

    service_end_to_end_status_repository = providers.Factory(
        ServiceEndToEndStatusRepositoryImplementation,
        datadog_site=config.datadog_site,
        datadog_api_key=config.datadog_api_key,
        datadog_app_key=config.datadog_app_key,
        datadog_monitor_mtls_env_tag=config.datadog_monitor_mtls_env_tag,
        datadog_monitor_dap_pap_env_tag=config.datadog_monitor_dap_pap_env_tag
    )

    error_logs_repository = providers.Factory(
        ErrorLogsRepositoryImplementation,
        datadog_site=config.datadog_site,
        datadog_api_key=config.datadog_api_key,
        datadog_app_key=config.datadog_app_key,
        env_tag=config.env_tag
    )

    # Applications
    mp_application = providers.Factory(
        MPApplicationImplementation,
        nra_repository=nra_repository,
        contract_repository=contract_repository,
        device_repository=device_repository,
        query_call_repository=query_call_repository
    )

    afc_service_status_application = providers.Factory(
        AFCServiceStatusApplicationImplementation,
        service_end_to_end_status_repository=service_end_to_end_status_repository
    )

    system_health_application = providers.Factory(
        SystemHealthApplicationImplementation,
        system_health_repository=system_health_repository,
        default_env=config.prometheus_monitoring_env
    )

    scheduler_status_application = providers.Factory(
        SchedulerStatusApplicationImplementation,
        scheduler_status_repository=scheduler_status_repository,
        default_env=config.prometheus_monitoring_env
    )

    error_logs_application = providers.Factory(
        ErrorLogsApplicationImplementation,
        error_logs_repository=error_logs_repository
    )
