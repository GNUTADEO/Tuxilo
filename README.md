# Tuxilo - Análisis Hidroeléctrico y Climático

Proyecto de análisis de datos climáticos (ONI, TSM) y su relación con la generación hidroeléctrica en Colombia.

## Estructura del Proyecto

```
Tuxilo/
├── App/                          # Aplicación principal
│   ├── Core/                     # Lógica de negocio
│   ├── Front/                    # Frontend
│   ├── Deploy/                   # Configuración de despliegue
│   ├── Packages/                 # Paquetes y módulos
│   └── Persistence/              # Capa de persistencia
│
├── notebooks/                    # Jupyter/Marimo notebooks
│   ├── Graficos.py              # Análisis de gráficos
│   ├── hidroelectrica.py        # Análisis hidroeléctrico
│   ├── fenomeno_presence.py     # Análisis de fenómenos climáticos
│   ├── marimo_cuadernos/        # Notebooks Marimo adicionales
│   └── .marimo/                 # Configuración Marimo
│
├── scripts/                      # Scripts de análisis
│   ├── correlation_analysis.py  # Análisis de correlaciones
│   ├── correlation_matrix_viz.py # Visualización de matrices
│   ├── pattern_analysis.py      # Análisis de patrones
│   └── api_test.py              # Tests de API (PyDataXM)
│
├── data/                         # Datos del proyecto
│   ├── raw/                      # Datos crudos
│   │   ├── download-*.csv       # Datos TSM y anomalías
│   │   ├── meiv2.data.txt       # Datos MEI v2
│   │   ├── hidroelectricas      # Lista de hidroeléctricas
│   │   └── C22-4CondicionesClim-Fig1-ComporONI.xlsx
│   ├── processed/                # Datos procesados
│   └── IDEAM_original/           # Datos IDEAM
│       ├── IndicesONI.csv
│       ├── IndicesTSM.csv
│       ├── ChivorPrecipitacion.csv
│       ├── LengupaCaudal.csv
│       ├── stationbasins.geojson
│       ├── subregions.geojson
│       └── *_Q_Day.Cmd.txt      # Datos de caudal diario
│
├── output/                       # Resultados generados
│   └── figures/                  # Gráficos y visualizaciones
│       ├── correlation_matrices_monthly.png
│       ├── correlation_matrix_overall.png
│       ├── correlation_dependent_vars_monthly.png
│       └── pattern_analysis_precipitation.png
│
├── docs/                         # Documentación
│   └── PMV.pdf                  # Documento PMV
│
├── assets/                       # Recursos estáticos
│   └── diagrams/                 # Diagramas
│       └── Arquitectura.drawio  # Diagrama de arquitectura
│
├── Data -> data/IDEAM_original/ # Symlink para retrocompatibilidad
├── results -> output/figures/   # Symlink para retrocompatibilidad
└── LICENSE

```

## Datos Analizados

- **Índices Climáticos**: ONI (Oceanic Niño Index), TSM (Temperatura Superficial del Mar)
- **Datos Hidroeléctricos**: Caudales, precipitación, aportes
- **Fuentes**: IDEAM, datos climáticos regionales

## Uso

### Análisis de Correlaciones
```bash
python scripts/correlation_analysis.py
```

### Visualización de Patrones
```bash
python scripts/pattern_analysis.py
```

### Notebooks Interactivos
```bash
marimo edit notebooks/Graficos.py
```

## Compatibilidad

Los directorios `Data` y `results` son enlaces simbólicos que apuntan a las nuevas ubicaciones para mantener la compatibilidad con scripts existentes.
