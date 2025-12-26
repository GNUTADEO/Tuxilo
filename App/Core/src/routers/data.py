
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


from shared_db import get_db

from models import FlowData, RainData

router = APIRouter(tags=["Data"], prefix="/data")

@router.get(
    "/semestres",
    operation_id="get_all_semesters",
)
async def get_all_semesters(db: AsyncSession = Depends(get_db)):
    """Obtiene todos los semestres del modelo"""

    start_year = 2025
    end_year = 2029
    semesters_per_year = [1, 2]

    semestres_list = []

    for year in range(start_year, end_year + 1):
        for sem in semesters_per_year:
            sem_id = f"{year}-{sem}"
            semestres_list.append({
                "id": sem_id,
                "nombre": sem_id
            })

    return {"semestres": semestres_list}


@router.get(
    "/flow",
    operation_id="get_all_flow_data",
)
async def get_all_flow_data(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todos los datos de caudal"""
    stmt = (
        select(
            FlowData,
        )
        .where(
            FlowData.value.is_not(None)
        )
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()  # returns list of FlowData objects
    
    datapoints = [
        {
            "id": row.id,
            "station_id": row.station_id,
            "date": row.observation_date,
            "value": row.value,
        }
        for row in rows
    ]
    
    return {"datapoints": datapoints}

@router.get(
    "/rain",
    operation_id="get_all_rain_data",
)
async def get_all_rain_data(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todos los datos de precipitación"""
    stmt = (
        select(
            RainData,
        )
        .where(
            RainData.value.is_not(None)
        )
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()  # returns list of FlowData objects
    
    datapoints = [
        {
            "id": row.id,
            "station_id": row.station_id,
            "date": row.observation_date,
            "value": row.value,
        }
        for row in rows
    ]
    
    return {"datapoints": datapoints}
