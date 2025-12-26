from datetime import datetime

from geoalchemy2 import Geometry
from sqlalchemy import Date, Float, Numeric, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class ReservoirPolygon(Base):
    __tablename__ = "embalses_polygons"
    __table_args__ = {"schema": "geodata", "extend_existing": True}

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str | None] = mapped_column(String(50))
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
