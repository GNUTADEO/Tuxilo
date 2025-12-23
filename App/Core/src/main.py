import os
import logging

from typing import Literal
from fastapi import FastAPI

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from routers.embalses import router as router_embalses
from routers.stations import router as router_stations

VERSION = "0.1.0"
COOKIES_SECURE = False

PUBLIC_ORIGINS = ["*"]
PUBLIC_METHODS = ["*"]
PUBLIC_HEADERS = ["*"]

COOKIES_SAMESITE: Literal["lax", "strict", "none"] = ("lax")

##############################################################################################
# Context Manager
##############################################################################################


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


##############################################################################################
# APIS
##############################################################################################

api = FastAPI(
    title="Main API",
    description="API base sin ninguna función específica.",
    version=VERSION,
    lifespan=lifespan,
)

api_public = FastAPI(
    title="Endpoints publicos para Tuxhydro",
    description="""API de embalses y estaciones.
    """,
    version=VERSION,
    lifespan=lifespan,
)

##############################################################################################
# MIDDLEWARE
##############################################################################################

api.add_middleware(
    CORSMiddleware,
    allow_origins=PUBLIC_ORIGINS,
    allow_credentials=COOKIES_SECURE,
    allow_methods=PUBLIC_METHODS,
    allow_headers=PUBLIC_HEADERS,
    max_age=86400,
)

api_public.add_middleware(
    CORSMiddleware,
    allow_origins=PUBLIC_ORIGINS,
    allow_credentials=COOKIES_SECURE,
    allow_methods=PUBLIC_METHODS,
    allow_headers=PUBLIC_HEADERS,
    max_age=86400,
)

##############################################################################################
# Montaje de frontend en la aplicación principal
##############################################################################################

api.mount("/public", api_public)
api_public.include_router(router_embalses)
api_public.include_router(router_stations)

##############################################################################################
# Validador en /
##############################################################################################

@api.get("/")
async def main():
    """Base path"""
    return {
        "message": "Main app is working",
        "cors": f"conditional_credentials: {COOKIES_SECURE}",
    }
