from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import DECIMAL, Date, DateTime, Float, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class ReservoirPolygon(Base):
    __tablename__ = "reservoir_polygon"
    __table_args__ = {"schema": "geodata"}

    reservoir_id: Mapped[str | None] = mapped_column(String(38), primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )

    nombre: Mapped[str | None] = mapped_column(String(50))

    proyecto: Mapped[str | None] = mapped_column(String(30))

    symbol: Mapped[str | None] = mapped_column(String(254))

    fecha: Mapped[datetime | None] = mapped_column(Date)

    ruleid: Mapped[float | None] = mapped_column(Float)

    fecha_1: Mapped[datetime | None] = mapped_column(Date)

    pk_cue: Mapped[float | None] = mapped_column(Numeric)

    shape_leng: Mapped[float | None] = mapped_column(Numeric)

    shape_area: Mapped[float | None] = mapped_column(Numeric)

    geom: Mapped[str | None] = mapped_column(
        Geometry(geometry_type="MULTIPOLYGON", srid=9377)
    )
