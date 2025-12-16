from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from shared_db import get_db

router = APIRouter(tags=["Embalses"], prefix="/embalses")


@router.get(
    "/",
    operation_id="get_all_embalses",
)
async def get_all_embalses(
        db: AsyncSession = Depends(get_db),
):
    """Obtiene todos los embalses con sus coordenadas"""
    query = text(
        "SELECT id, nombre, latitud, longitud FROM embalses WHERE latitud IS NOT NULL AND longitud IS NOT NULL"
    )
    result = await db.execute(query)
    rows = result.fetchall()
    
    embalses = [
        {
            "id": row[0],
            "nombre": row[1],
            "latitud": float(row[2]) if row[2] else None,
            "longitud": float(row[3]) if row[3] else None,
        }
        for row in rows
    ]
    
    return {"embalses": embalses}

@router.get("/geojson")
async def get_embalses_geojson(db: AsyncSession = Depends(get_db)):
    query = text("""
                  SELECT jsonb_build_object(
         'type', 'FeatureCollection',
         'features', jsonb_agg(feature)
     )
     FROM (
         SELECT jsonb_build_object(
             'type', 'Feature',
             'id', gid,
             'geometry', ST_AsGeoJSON(ST_Transform(ST_SetSRID(geom, 9377), 4326))::jsonb,
             'properties', jsonb_build_object(
                 'nombre', "NOMBRE_GEO",
                 'proyecto', "PROYECTO",
                 'area_km2', ROUND(("SHAPE_Area"/1000000)::numeric, 2)
             )
         ) AS feature
         FROM embalses_geom
     ) features;
    """)
    result = await db.execute(query)
    return result.scalar()
