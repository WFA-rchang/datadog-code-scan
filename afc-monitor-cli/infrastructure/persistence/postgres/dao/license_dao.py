from datetime import datetime
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure.persistence.postgres.database.base import Base


class LicenseDAO(Base):
    __tablename__ = "mp_license"

    id: Mapped[int] = mapped_column(primary_key=True)
    contract_id: Mapped[int] = mapped_column(Integer(), ForeignKey("mp_contract.id"), nullable=False)
    last_used_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    is_available: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
