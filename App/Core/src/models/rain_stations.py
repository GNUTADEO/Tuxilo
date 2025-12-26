from sqlalchemy import DECIMAL, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class RainStation(Base):
    __tablename__ = "rain_stations"
    __table_args__ = {"schema": "geodata", "extend_existing": True}

    station_id: Mapped[str] = mapped_column(String(50), primary_key=True)

    station_name: Mapped[str] = mapped_column(String(255), nullable=False)

    latitude: Mapped[float] = mapped_column(DECIMAL(10, 8), nullable=False)

    longitude: Mapped[float] = mapped_column(DECIMAL(11, 8), nullable=False)
