import logging
from dotenv import load_dotenv
from prometheus_api_client import PrometheusConnect
from dependency_injector import containers, providers

from application.mp_application_implementation import MPApplicationImplementation
from infrastructure.persistence.postgres.database.engine import PostgresEngineFactory
from application.system_health_implementation import SystemHealthApplicationImplementation
from infrastructure.persistence.postgres.nra_repository_implementation import NRARepositoryImplementation
from application.afc_service_status_application_implementation import AFCServiceStatusApplicationImplementation
from infrastructure.persistence.postgres.device_repository_implementation import DeviceRepositoryImplementation
from infrastructure.persistence.postgres.contract_repository_implementation import ContractRepositoryImplementation
from infrastructure.persistence.postgres.query_call_repository_implementation import QueryCallRepositoryImplementation
from infrastructure.service.prometheus.system_health_repository_implementation import SystemHealthRepositoryImplementation
from infrastructure.service.datadog.service_end_to_end_status_repository_implementation import ServiceEndToEndStatusRepositoryImplementation


class Container(containers.DeclarativeContainer):
    # Load .env.local if it exists for environment variables
    load_dotenv('.env.local')

    # Wiring Config
    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=[
            "interface.click.command.proactive_monitor_command",
            "interface.click.command.system_health_command"
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
    config.datadog_monitor_env_tag.from_env("DATADOG_MONITOR_ENV_TAG", required=True)
    config.prometheus_host.from_env("PROMETHEUS_HOST", required=True)
    config.prometheus_monitoring_env.from_env("PROMETHEUS_MONITORING_ENV", default="production")

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
        datadog_monitor_env_tag=config.datadog_monitor_env_tag
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
