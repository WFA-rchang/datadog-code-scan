import datetime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy import ForeignKey
from sqlalchemy import SmallInteger
from sqlalchemy.orm import mapped_column

from infrastructure.persistence.postgres.database.base import Base


class ContractDAO(Base):
    __tablename__ = "mp_contract"

    id: Mapped[int] = mapped_column(primary_key=True)
    uri: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    company_id: Mapped[int] = mapped_column(Integer(), ForeignKey("mp_company.id"), nullable=False, index=True)
    licensed_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    contract_group_id: Mapped[int] = mapped_column(Integer(), ForeignKey("mp_contract_group.id"), index=True)
    monthly_bucket: Mapped[int] = mapped_column(SmallInteger(), index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
