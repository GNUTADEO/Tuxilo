from datetime import date

from sqlalchemy import DECIMAL, Date, String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RainData(Base):
    __tablename__ = "rain_data"
    __table_args__ = {"schema": "geodata", "extend_existing": True}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    station_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("geodata.rain_stations.station_id", ondelete="CASCADE"),
        nullable=False
    )
    observation_date: Mapped[date] = mapped_column(Date, nullable=False)
    value: Mapped[float] = mapped_column(DECIMAL(12, 3))