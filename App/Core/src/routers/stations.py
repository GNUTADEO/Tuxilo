from this import s
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from sqlalchemy import select
from geoalchemy2.functions import ST_Intersects, ST_Transform, ST_SetSRID, ST_MakePoint, ST_Distance

from shared_db import get_db

from models import FlowStation, RainStation, ReservoirDot, ReservoirPolygon

router = APIRouter(tags=["Stations"], prefix="/stations")




@router.get("/test-orm")
async def test_orm(
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(
            FlowStation
        )
        .where(
            FlowStation.station_name == "Example Station",
        )
    )

    result = await db.execute(stmt)

    return result.scalars().all()


@router.get(
    "/",
    operation_id="get_all_stations",
)
async def get_all_stations(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todas las estaciones con sus coordenadas"""
    stmt = (
        select(
            FlowStation.station_id,
            FlowStation.station_name,
            FlowStation.river_name,
            FlowStation.latitude,
            FlowStation.longitude
        )
        .where(
            FlowStation.latitude.is_not(None),
            FlowStation.longitude.is_not(None),
            FlowStation.station_name.is_not(None)
        )
        .order_by(FlowStation.station_name)
    )

    result = await db.execute(stmt)
    rows = result.mappings().all()
    
    stations = [
        {
            "station_id": row['station_id'],
            "station_name": row['station_name'],
            "river_name": row['river_name'],
            "latitude": float(row['latitude']) if row['latitude'] else None,
            "longitude": float(row['longitude']) if row['longitude'] else None,
        }
        for row in rows
    ]
    
    return {"stations": stations}


@router.get("/nearest/{embalse_id}")
async def get_nearest_station(
    embalse_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene la estación más cercana a un embalse específico"""

    # Subquery to get the embalse geometry
    embalse_subq = select(ReservoirDot.geom).where(
        ReservoirDot.reservoir_id == embalse_id
    ).limit(1).subquery()

    # Transform embalse geom to 4326
    embalse_geom_4326 = ST_Transform(embalse_subq.c.geom, 4326)

    # Compute distance for all FlowStations
    stmt = (
        select(
            FlowStation.station_id,
            FlowStation.station_name,
            FlowStation.river_name,
            FlowStation.latitude,
            FlowStation.longitude,
            (ST_Distance(
                embalse_geom_4326.cast("geography"),
                ST_SetSRID(ST_MakePoint(FlowStation.longitude, FlowStation.latitude), 4326).cast("geography")
            ) / 1000).label("distance_km")
        )
        .where(
            FlowStation.latitude.is_not(None),
            FlowStation.longitude.is_not(None)
        )
        .order_by("distance_km")
        .limit(1)
    )

    result = await db.execute(stmt)
    row = result.mappings().first()

    if not row:
        return {"station": None}

    station = {
        "station_id": row["station_id"],
        "station_name": row["station_name"],
        "river_name": row["river_name"],
        "latitude": float(row["latitude"]) if row["latitude"] else None,
        "longitude": float(row["longitude"]) if row["longitude"] else None,
        "distance_km": float(row["distance_km"]),
    }

    return {"station": station}
