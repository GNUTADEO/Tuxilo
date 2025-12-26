import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from sqlalchemy import text

from geoalchemy2.functions import ST_AsGeoJSON, ST_Transform

from shared_db import get_db

from models import FlowData, RainData

router = APIRouter(tags=["Data"], prefix="/data")


@router.get(
    "/flow",
    operation_id="get_all_flow_data",
)
async def get_all_flow_data(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todos los embalses con sus coordenadas"""
    stmt = (
        select(
            FlowData,
        )
        .where(
            FlowData.flow_value.is_not(None)
        )
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()  # returns list of FlowData objects
    
    embalses = [
        {
            "id": row.id,
            "station_id": row.station_id,
            "flow_value": row.flow_value,
        }
        for row in rows
    ]
    
    return {"embalses": embalses}
