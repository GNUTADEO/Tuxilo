import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy import text

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
            ReservoirPolygon
        )
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    
    embalses = [
        {
            "id": row.reservoir_id,
            "nombre": row.nombre,
        }
        for row in rows
    ]
    
    return {"embalses": embalses}
