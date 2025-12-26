from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, Numeric

from .base import Base

class ReservoirDot(Base):
    __tablename__ = "embalses_points"
    __table_args__ = {"schema": "geodata", "extend_existing": True}

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str | None] = mapped_column(String(255))
    latitude: Mapped[float | None] = mapped_column(Numeric)
    longitude: Mapped[float | None] = mapped_column(Numeric)
    geom: Mapped[str | None] = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326
        )
    )