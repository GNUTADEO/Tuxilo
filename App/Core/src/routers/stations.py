from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import cast
from geoalchemy2 import Geography
from geoalchemy2.functions import ST_Transform, ST_SetSRID, ST_MakePoint, ST_Distance

from shared_db import get_db

from models import FlowStation, RainStation, ReservoirDot

router = APIRouter(tags=["Stations"], prefix="/estaciones")

FLOW_STATION_IDS = [
    21080030,
    21160040,
    21200620,
    21200780,
    21201180,
    21201320,
    23050250,
    23085110,
    24015120,
    26030150,
    35060100,
]

@router.get(
    "/flow",
    operation_id="get_all_flow_stations",
)
async def get_all_flow_stations(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todas las estaciones con sus coordenadas"""
    stmt = (
        select(
            FlowStation.id,
            FlowStation.name,
            FlowStation.latitude,
            FlowStation.longitude
        )
        .where(
            FlowStation.latitude.is_not(None),
            FlowStation.longitude.is_not(None),
            FlowStation.name.is_not(None),
        )
        .order_by(FlowStation.name)
    )

    result = await db.execute(stmt)
    rows = result.mappings().all()
    
    features = [
        {
            "id": row["id"],
            "type": "Feature",
            "nombre": row["name"],
            "latitud": float(row["latitude"]) if row["latitude"] else None,
            "longitud": float(row["longitude"]) if row["longitude"] else None,
        }
        for row in rows
    ]
    
    return {"type": "FeatureCollection", "features": features}


@router.get(
    "/rain",
    operation_id="get_all_rain_stations",
)
async def get_all_rain_stations(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todas las estaciones con sus coordenadas"""
    stmt = (
        select(
            RainStation.id,
            RainStation.name,
            RainStation.latitude,
            RainStation.longitude
        )
        .where(
            RainStation.latitude.is_not(None),
            RainStation.longitude.is_not(None),
            RainStation.name.is_not(None)
        )
        .order_by(RainStation.name)
    )

    result = await db.execute(stmt)
    rows = result.mappings().all()
    
    features = [
        {
            "id": row["id"],
            "type": "Feature",
            "nombre": row["name"],
            "latitud": float(row["latitude"]) if row["latitude"] else None,
            "longitud": float(row["longitude"]) if row["longitude"] else None,
        }
        for row in rows
    ]
    
    return {"type": "FeatureCollection", "features": features}


@router.get("/flow/nearest/{embalse_id}")
async def get_nearest_flow_station(
    embalse_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get the FlowStation nearest to a specific ReservoirDot"""

    # Subquery to get the embalse geometry
    embalse_subq = select(ReservoirDot.geom).where(
        ReservoirDot.id == embalse_id
    ).limit(1).scalar_subquery()

    # Calculate distance
    distance_km = (ST_Distance(
        cast(ST_Transform(embalse_subq, 4326), Geography),
        cast(ST_SetSRID(ST_MakePoint(FlowStation.longitude, FlowStation.latitude), 4326), Geography)
    ) / 1000).label("distance_km")

    # Build the query with distance calculation
    stmt = (
        select(
            FlowStation.id,
            FlowStation.name,
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
            "station_id": row["id"],
            "station_name": row["name"],
            "latitude": float(row["latitude"]) if row["latitude"] else None,
            "longitude": float(row["longitude"]) if row["longitude"] else None,
            "distance_km": round(float(row["distance_km"]), 2) if row["distance_km"] else None,
        }
    }