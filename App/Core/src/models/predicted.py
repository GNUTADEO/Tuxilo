from decimal import Decimal

from sqlalchemy import String, BigInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class PredictedData(Base):
    __tablename__ = "predicted_data"
    __table_args__ = {"schema": "data", "extend_existing": True}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    embalse: Mapped[str] = mapped_column(String(50))
    periodo: Mapped[str] = mapped_column(String(10))
    precipitacion_project: Mapped[Decimal] = mapped_column(Numeric(25, 16))
    ar: Mapped[Decimal] = mapped_column(Numeric(25, 16))
    br: Mapped[Decimal] = mapped_column(Numeric(25, 4))
    ar_km2: Mapped[Decimal] = mapped_column(Numeric(25, 3))
    ai_km2: Mapped[Decimal] = mapped_column(Numeric(25, 3))
    q_proyectado: Mapped[Decimal] = mapped_column(Numeric(25, 16))
