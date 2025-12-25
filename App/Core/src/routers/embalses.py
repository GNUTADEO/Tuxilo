import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy import text

from geoalchemy2.functions import ST_AsGeoJSON, ST_Transform

from shared_db import get_db

from models import FlowStation, RainStation, ReservoirDot, ReservoirPolygon

router = APIRouter(tags=["Embalses"], prefix="/embalses")


@router.get(
    "/",
    operation_id="get_all_embalses",
)
async def get_all_embalses(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todos los embalses con sus coordenadas"""
    stmt = (
        select(
            ReservoirDot.reservoir_id,
            ReservoirDot.nombre,
            ReservoirDot.latitud,
            ReservoirDot.longitud
        ).where(
            ReservoirDot.latitud.is_not(None),
            ReservoirDot.longitud.is_not(None),
            ReservoirDot.nombre.is_not(None)
        )
    )

    result = await db.execute(stmt)
    rows = result.mappings().all()
    
    embalses = [
        {
            "id": row["reservoir_id"],
            "nombre": row["nombre"],
            "latitud": float(row["latitud"]) if row["latitud"] else None,
            "longitud": float(row["longitud"]) if row["longitud"] else None,
        }
        for row in rows
    ]
    
    return {"embalses": embalses}

@router.get("/geojson")
async def get_embalses_geojson(db: AsyncSession = Depends(get_db)):
    stmt = (
        select(
            ReservoirPolygon.reservoir_id,
            ReservoirPolygon.nombre,
            ReservoirPolygon.proyecto,
            ReservoirPolygon.shape_area,
            ST_AsGeoJSON(ST_Transform(ReservoirPolygon.geom, 4326)).label("geom")
        )
        .where(ReservoirPolygon.nombre.is_not(None))
    )
    
    result = await db.execute(stmt)
    rows = result.mappings().all()  # dict-like access

    features = []
    for row in rows:
        features.append({
            "type": "Feature",
            "id": row["reservoir_id"],
            "geometry": json.loads(row["geom"]) if row["geom"] else None,
            "properties": {
                "nombre": row["nombre"],
                "proyecto": row["proyecto"],
                "area_km2": round((row["shape_area"] or 0) / 1_000_000, 2)
            }
        })

    return {"type": "FeatureCollection", "features": features}