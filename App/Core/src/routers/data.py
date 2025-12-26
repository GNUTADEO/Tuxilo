
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select


from shared_db import get_db

from models import FlowData, RainData, PredictedData

router = APIRouter(tags=["Data"], prefix="/data")

# Mapping between frontend embalse IDs and database embalse names
EMBALSE_ID_TO_NAME = {
    66: "Guavio",
    60: "Neusa",
    46: "Prado",
    58: "Tomine",
    35: "Guatape",
    71: "Miel-Norcasia",
    32: "Salvajina",
    59: "Sisga",
    67: "Betania",
    48: "Muna",
    55: "Gachaneca"
}

@router.get(
    "/semestres",
    operation_id="get_all_semesters",
)
async def get_all_semesters(db: AsyncSession = Depends(get_db)):
    """Obtiene todos los semestres del modelo"""
    stmt = (
        select(
            PredictedData,
        )
        .limit(10)
    )

    result = await db.execute(stmt)
    rows = result.scalars().all()  # <-- ORM objects
    
    features = [
        {
            "id": row.id,
            "periodo": row.periodo,
        }
        for row in rows
    ]
    
    return {"features": features}


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

@router.get(
    "/q_proyectado/{embalse_id}/{periodo}",
    operation_id="get_q_proyectado",
)
async def get_q_proyectado(
    embalse_id: int,
    periodo: str,
    db: AsyncSession = Depends(get_db)
):
    """Obtiene el q_proyectado para un embalse y periodo específicos"""
    
    # Convert embalse_id to database embalse name
    embalse_name = EMBALSE_ID_TO_NAME.get(embalse_id)
    
    if not embalse_name:
        raise HTTPException(status_code=404, detail=f"Embalse ID {embalse_id} not found")
    
    stmt = (
        select(PredictedData)
        .where(
            PredictedData.embalse == embalse_name,
            PredictedData.periodo == periodo
        )
        .limit(1)
    )
    
    result = await db.execute(stmt)
    row = result.scalars().first()
    
    if not row:
        raise HTTPException(
            status_code=404, 
            detail=f"No data found for embalse '{embalse_name}' and periodo '{periodo}'"
        )
    
    return {
        "embalse_id": embalse_id,
        "embalse": row.embalse,
        "periodo": row.periodo,
        "q_proyectado": float(row.q_proyectado),
        "precipitacion_project": float(row.precipitacion_project),
        "ar": float(row.ar),
        "br": float(row.br),
        "ar_km2": float(row.ar_km2),
        "ai_km2": float(row.ai_km2)
    }


@router.get(
    "/media/{graph_filename}",
    operation_id="get_media_from_graph",
)
async def get_media_from_graph(graph_filename: str):
    """Extrae el valor de Media de un archivo HTML de gráfico"""
    import re
    from pathlib import Path
    import os
    
    # Check if running in Docker (volume mounted at /api/graphs)
    # or locally (relative path from Core/src/routers)
    if os.path.exists("/api/graphs"):
        graph_path = Path("/api/graphs") / graph_filename
    else:
        graph_path = Path(__file__).parent.parent.parent.parent / "Front" / "front" / "static" / "graphs" / graph_filename
    
    if not graph_path.exists():
        raise HTTPException(status_code=404, detail=f"Graph file '{graph_filename}' not found at {graph_path}")
    
    try:
        with open(graph_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Search for "Media = value" pattern
        match = re.search(r'Media = ([\d.]+)', content)
        
        if not match:
            raise HTTPException(status_code=404, detail=f"Media value not found in '{graph_filename}'")
        
        media_value = float(match.group(1))
        
        return {
            "filename": graph_filename,
            "media": media_value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
