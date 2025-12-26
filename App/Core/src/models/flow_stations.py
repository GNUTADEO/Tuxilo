from sqlalchemy import DECIMAL, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class FlowStation(Base):
    __tablename__ = "flow_stations"
    __table_args__ = {"schema": "geodata", "extend_existing": True}

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(DECIMAL(10, 8), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(11, 8), nullable=False)
