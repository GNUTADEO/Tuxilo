from datetime import datetime

from sqlalchemy import DECIMAL, DateTime, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class RainStation(Base):
    __tablename__ = "flow_stations"
    __table_args__ = {"schema": "geodata"}

    station_id: Mapped[str] = mapped_column(String(50), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )

    river_name: Mapped[str] = mapped_column(String(255), nullable=False)

    station_name: Mapped[str] = mapped_column(String(255), nullable=False)

    latitude: Mapped[float] = mapped_column(DECIMAL(10, 8), nullable=False)

    longitude: Mapped[float] = mapped_column(DECIMAL(11, 8), nullable=False)
