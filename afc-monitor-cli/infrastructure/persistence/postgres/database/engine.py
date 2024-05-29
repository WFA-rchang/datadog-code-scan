from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%s/%s"


class PostgresEngineFactory:
    @staticmethod
    def create_postgres_engine(db_host, db_port, db_username, db_password, db_name) -> Engine:
        db_url = SQLALCHEMY_DATABASE_URL % (db_username, db_password, db_host, db_port, db_name)
        engine = create_engine(db_url)
        return engine
