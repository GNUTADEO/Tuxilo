from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from sqlalchemy import select, func
from geoalchemy2.functions import ST_Intersects, ST_Transform, ST_SetSRID, ST_MakePoint

from shared_db import get_db

from models import FlowStation, RainStation, ReservoirDot, ReservoirPolygon

router = APIRouter(tags=["Stations"], prefix="/stations")




@router.get("/test-orm")
async def test_orm(
    db: AsyncSession = Depends(get_db),
):
    point_9377 = ST_Transform(
        ST_SetSRID(
            ST_MakePoint(
                FlowStation.longitude,
                FlowStation.latitude
            ),
            4326
        ),
        9377
    )

    stmt = (
        select(
            FlowStation.station_id,
            FlowStation.station_name,
            FlowStation.river_name,
            ReservoirPolygon.reservoir_id,
            ReservoirPolygon.nombre.label("reservoir_name"),
        )
        .join(
            ReservoirPolygon,
            ST_Intersects(ReservoirPolygon.geom, point_9377)
        )
        .where(
            FlowStation.latitude.is_not(None),
            FlowStation.longitude.is_not(None),
        )
        .order_by(ReservoirPolygon.nombre, FlowStation.station_name)
    )

    result = await db.execute(stmt)

    return result.mappings().all()


@router.get(
    "/",
    operation_id="get_all_stations",
)
async def get_all_stations(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todas las estaciones con sus coordenadas"""
    query = text("""
    SELECT
        station_id,
        station_name,
        river_name,
        latitude,
        longitude
    FROM flow_stations
    WHERE latitude IS NOT NULL
      AND longitude IS NOT NULL
      AND station_name IS NOT NULL
    ORDER BY station_name
""")

    result = await db.execute(query)
    rows = result.fetchall()
    
    stations = [
        {
            "station_id": row[0],
            "station_name": row[1],
            "river_name": row[2],
            "latitude": float(row[3]) if row[3] else None,
            "longitude": float(row[4]) if row[4] else None,
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
    query = text("""
    WITH embalse_point AS (
        SELECT geom
        FROM embalses_points
        WHERE reservoir_id = :embalse_id
    )
    SELECT
        s.station_id,
        s.station_name,
        s.river_name,
        s.latitude,
        s.longitude,
        ST_Distance(
            ST_Transform(e.geom, 4326)::geography,
            ST_SetSRID(ST_MakePoint(s.longitude, s.latitude), 4326)::geography
        ) / 1000 as distance_km
    FROM flow_stations s, embalse_point e
    WHERE s.latitude IS NOT NULL
      AND s.longitude IS NOT NULL
    ORDER BY ST_Distance(
        ST_Transform(e.geom, 4326)::geography,
        ST_SetSRID(ST_MakePoint(s.longitude, s.latitude), 4326)::geography
    )
    LIMIT 1
    """)

    result = await db.execute(query, {"embalse_id": embalse_id})
    row = result.fetchone()
    
    if not row:
        return {"station": None}
    
    station = {
        "station_id": row[0],
        "station_name": row[1],
        "river_name": row[2],
        "latitude": float(row[3]) if row[3] else None,
        "longitude": float(row[4]) if row[4] else None,
        "distance_km": round(float(row[5]), 2) if row[5] else None,
    }
    
    return {"station": station}
