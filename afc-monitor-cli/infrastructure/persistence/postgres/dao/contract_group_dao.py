import datetime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy import SmallInteger
from sqlalchemy.orm import mapped_column

from infrastructure.persistence.postgres.database.base import Base


class ContractGroupDAO(Base):
    __tablename__ = "mp_contract_group"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(Integer(), ForeignKey("mp_company.id"), nullable=False, index=True)
    type: Mapped[int] = mapped_column(SmallInteger(), nullable=False, default=1)
    uri: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
