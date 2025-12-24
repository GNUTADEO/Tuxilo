SET CLIENT_ENCODING TO UTF8;
SET STANDARD_CONFORMING_STRINGS TO ON;
BEGIN;
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE TABLE "public"."embalses_geom" (
"NOMBRE_GEO" varchar(50),
"PROYECTO" varchar(30),
"SYMBOL" varchar(254),
"FECHA" date,
"RULEID" float8,
"FECHA_1" date,
"PK_CUE" numeric,
"GLOBALID" varchar(38),
"SHAPE_Leng" numeric,
"SHAPE_Area" numeric);
ALTER TABLE "public"."embalses_geom" ADD PRIMARY KEY ("GLOBALID");
SELECT AddGeometryColumn('public','embalses_geom','geom','0','MULTIPOLYGON',2);
COMMIT;