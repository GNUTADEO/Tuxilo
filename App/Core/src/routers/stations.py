from this import s
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy import select
from sqlalchemy import cast
from geoalchemy2 import Geography
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
    """Get the FlowStation nearest to a specific ReservoirDot"""

    # Subquery to get the embalse geometry
    embalse_subq = select(ReservoirDot.geom).where(
        ReservoirDot.reservoir_id == embalse_id
    ).limit(1).scalar_subquery()

    # Calculate distance
    distance_km = (ST_Distance(
        cast(ST_Transform(embalse_subq, 4326), Geography),
        cast(ST_SetSRID(ST_MakePoint(FlowStation.longitude, FlowStation.latitude), 4326), Geography)
    ) / 1000).label("distance_km")

    # Build the query with distance calculation
    stmt = (
        select(
            FlowStation.station_id,
            FlowStation.station_name,
            FlowStation.river_name,
            FlowStation.latitude,
            FlowStation.longitude,
            distance_km
        )
        .where(
            FlowStation.latitude.is_not(None),
            FlowStation.longitude.is_not(None)
        )
        .order_by(distance_km)
        .limit(1)
    )

    # Execute
    result = await db.execute(stmt)
    row = result.mappings().first()

    if not row:
        return {"station": None}

    # Return clean dict
    return {
        "station": {
            "station_id": row["station_id"],
            "station_name": row["station_name"],
            "river_name": row["river_name"],
            "latitude": float(row["latitude"]) if row["latitude"] else None,
            "longitude": float(row["longitude"]) if row["longitude"] else None,
            "distance_km": round(float(row["distance_km"]), 2) if row["distance_km"] else None,
        }
    }