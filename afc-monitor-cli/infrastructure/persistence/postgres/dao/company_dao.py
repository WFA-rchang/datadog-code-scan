from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.persistence.postgres.database.base import Base


class CompanyDAO(Base):
    __tablename__ = "mp_company"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    oid: Mapped[str] = mapped_column(String(32), unique=True, index=True)
