import logging
from dotenv import load_dotenv
from dependency_injector import containers, providers

from application.mp_application_implementation import MPApplicationImplementation
from infrastructure.persistence.postgres.database.engine import PostgresEngineFactory
from infrastructure.persistence.postgres.nra_repository_implementation import NRARepositoryImplementation
from infrastructure.persistence.postgres.device_repository_implementation import DeviceRepositoryImplementation
from infrastructure.persistence.postgres.contract_repository_implementation import ContractRepositoryImplementation
from infrastructure.persistence.postgres.query_call_repository_implementation import QueryCallRepositoryImplementation


class Container(containers.DeclarativeContainer):
    # Load .env.local if it exists for environment variables
    load_dotenv('.env.local')

    # Wiring Config
    wiring_config = containers.WiringConfiguration(
        modules=[],
        packages=[
            "interface.click.command.proactive_monitor_command",
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

    # Repositories
    nra_repository = providers.Factory(
        NRARepositoryImplementation,
        engine=postgres_engine
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

    # Applications
    mp_application = providers.Factory(
        MPApplicationImplementation,
        nra_repository=nra_repository,
        contract_repository=contract_repository,
        device_repository=device_repository,
        query_call_repository=query_call_repository
    )
