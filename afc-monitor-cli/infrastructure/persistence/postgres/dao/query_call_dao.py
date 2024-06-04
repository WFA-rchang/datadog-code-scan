from datetime import datetime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy import SmallInteger
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column

from infrastructure.persistence.postgres.database.base import Base


class QueryCallDAO(Base):
    __tablename__ = "mp_query_call"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[int] = mapped_column(SmallInteger())
    device_id: Mapped[int] = mapped_column(Integer(), index=True)
    query_date: Mapped[datetime] = mapped_column(DateTime(), index=True)
    license_id: Mapped[int] = mapped_column(Integer(), index=True)
