from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Numeric, DateTime, DECIMAL, text

from geoalchemy2 import Geometry

from .base import Base

class ReservoirDot(Base):
    __tablename__ = "reservoir_dot"
    __table_args__ = {"schema": "geodata"}

    reservoir_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    nombre: Mapped[str | None] = mapped_column(
        String(255)
    )

    latitud: Mapped[float | None] = mapped_column(
        Numeric
    )

    longitud: Mapped[float | None] = mapped_column(
        Numeric
    )

    geom: Mapped[str | None] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326
        )
    )