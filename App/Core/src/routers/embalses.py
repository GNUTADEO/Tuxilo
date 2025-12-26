import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select

from geoalchemy2.functions import ST_AsGeoJSON, ST_Transform

from shared_db import get_db

from models import ReservoirDot, ReservoirPolygon

router = APIRouter(tags=["Embalses"], prefix="/embalses")

RESERVOIR_IDS = [
    67,
    32,
    46,
    48,
    66,
    58,
    59,
    60,
    55,
    71,
    35
]

@router.get(
    "/points",
    operation_id="get_all_embalse_points",
)
async def get_all_embalse_points(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todos los embalses con sus coordenadas"""
    stmt = (
        select(
            ReservoirDot.id,
            ReservoirDot.name,
            ReservoirDot.latitude,
            ReservoirDot.longitude
        ).where(
            ReservoirDot.latitude.is_not(None),
            ReservoirDot.longitude.is_not(None),
            ReservoirDot.name.is_not(None),
            ReservoirDot.id.in_(RESERVOIR_IDS)
        )
        .order_by(ReservoirDot.name)
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
    "/polygons",
    operation_id="get_all_embalse_polygons",
)
async def get_all_embalse_polygons(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(
            ReservoirPolygon.id,
            ReservoirPolygon.name,
            ReservoirPolygon.shape_area,
            ST_AsGeoJSON(ST_Transform(ReservoirPolygon.geom, 4326)).label("geom")
        )
        .where(
            ReservoirPolygon.name.is_not(None),
            ReservoirPolygon.id.in_(RESERVOIR_IDS)
        )
    )
    
    result = await db.execute(stmt)
    rows = result.mappings().all()  # dict-like access

    features = [
        {
            "id": row["id"],
            "type": "Feature",
            "properties": {
                "nombre": row["name"],
                "area_km2": round((row["shape_area"] or 0) / 1_000_000, 2),
            },
            "geometry": json.loads(row["geom"]) if row["geom"] else None,
        }
        for row in rows
    ]

    return {"type": "FeatureCollection", "features": features}