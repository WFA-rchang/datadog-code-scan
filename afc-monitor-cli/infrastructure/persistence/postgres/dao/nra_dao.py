from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy import SmallInteger
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import mapped_column

from infrastructure.persistence.postgres.database.base import Base


class NRADAO(Base):
    __tablename__ = "mp_nra_auth"
    __table_args__ = (
        UniqueConstraint('certification_id', 'ruleset_id', name='mp_nra_auth_un_code_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    certification_id: Mapped[str] = mapped_column(String(32))
    is_authed: Mapped[bool] = mapped_column(nullable=False, default=False)
    ruleset_id: Mapped[str] = mapped_column(String(32))
    deployment_type: Mapped[int] = mapped_column(SmallInteger(), nullable=False, default=1)
