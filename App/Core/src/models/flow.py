from datetime import datetime, date

from sqlalchemy import DECIMAL, DateTime, Date, String, text, BigInteger, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class FlowData(Base):
    __tablename__ = "grdc_daily_flow"
    __table_args__ = {"schema": "geodata", "extend_existing": True}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    station_id: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("geodata.flow_stations.station_id", ondelete="CASCADE"),
        nullable=False
    )
    observation_date: Mapped[date] = mapped_column(Date, nullable=False)
    flow_value: Mapped[float] = mapped_column(DECIMAL(12, 3))
    month_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    flow_value_imputed: Mapped[float] = mapped_column(DECIMAL(12, 3))