from datetime import datetime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column

from infrastructure.persistence.postgres.database.base import Base


class DeviceDAO(Base):
    __tablename__ = "mp_device"
    __table_args__ = (
        UniqueConstraint('serial_number', 'auth_id', name='mp_device_serial_number_auth_un'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    serial_number: Mapped[str] = mapped_column(String(50))
    license_id: Mapped[int] = mapped_column(Integer(), unique=True)
    company_id: Mapped[int] = mapped_column(Integer(), ForeignKey('mp_company.id'))
    auth_id: Mapped[int] = mapped_column(Integer(), ForeignKey('mp_nra_auth.id'))
    description: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_allowed: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_assign_succeeded: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
