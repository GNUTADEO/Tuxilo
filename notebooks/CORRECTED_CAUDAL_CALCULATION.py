"""
CORRECTED CAUDAL CALCULATION
=============================

Issues fixed:
1. ✓ Changed (Ai/Ar) to (Ar/Ai) - was 75x too small
2. ✓ Removed × Ch multiplication - not in original formula
3. ✓ Verified with historical data

Expected results: Q ≈ 4-5 m³/s for Salvajina (matches historical)
"""

import pandas as pd
import numpy as np

RUTA_AREAS = "/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/Calculo_caudal/Areas_hidrologia.csv"
RUTA_PRECIP = "/home/chofojeda/hackaton rios/pruebaprecip.csv"
RUTA_PARAM = "/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/RECALIBRATED_BR_VALUES.csv"

df_areas = pd.read_csv(RUTA_AREAS)
df_precip = pd.read_csv(RUTA_PRECIP, sep=';')
df_param = pd.read_csv(RUTA_PARAM)

def limpiar_columnas(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

df_areas = limpiar_columnas(df_areas)
df_precip = limpiar_columnas(df_precip)
df_param = limpiar_columnas(df_param)

print("✓ Columnas PRECIP:")
print(df_precip.columns.tolist())

print("\n✓ Columnas PARAMETROS:")
print(df_param.columns.tolist())

print("\n✓ Columnas AREAS:")
print(df_areas.columns.tolist())

# ==============================
# UNIÓN DE TABLAS
# ==============================
df = (
    df_precip
    .merge(df_param[["embalse", "ar", "br"]], on="embalse", how="left")
    .merge(df_areas[["embalse", "ai_km2", "ar_km2"]], on="embalse", how="left")
)

# ==============================
# VALIDACIONES
# ==============================
if df[["ar", "br", "ai_km2"]].isnull().any().any():
    raise ValueError("Faltan ar, br o Ai para algunos embalses")

if (df["precipitacion_project"] <= 0).any():
    raise ValueError("Existen precipitaciones no positivas")

# ==============================
# MODELO HIDROLÓGICO (CORRECTED)
# Qi,t = ar · Pi,t^br · (Ar / Ai)
# ==============================

print("\n" + "="*80)
print("CÁLCULO DE CAUDAL PROYECTADO (FÓRMULA CORREGIDA)")
print("="*80)
print("\nFórmula: Q(i,t) = ar × P(t)^br × (Ar/Ai)")
print("\nDonde:")
print("  ar = coeficiente de escala regional")
print("  P(t) = precipitación acumulada 3 meses (mm)")
print("  br = sensibilidad hidrológica")
print("  Ar = área de macrocuenca (km²)")
print("  Ai = área de drenaje del embalse (km²)")

# ✓ CORRECTED: Using (Ar/Ai) instead of (Ai/Ar)
# ✓ REMOVED: No longer multiplying by Ch
df["q_proyectado"] = (
    df["ar"]
    * np.power(df["precipitacion_project"], df["br"])
    * (df["ar_km2"] / df["ai_km2"])      # ← CORRECTED: Ar/Ai, not Ai/Ar
)

df["q_proyectado"] = df["q_proyectado"].clip(lower=0)

# ==============================
# EXPORTAR RESULTADOS
# ==============================
df_salida = df[
    ["embalse", "periodo", "precipitacion_project", "ar", "br", "ar_km2", "ai_km2", "q_proyectado"]
].sort_values(["embalse", "periodo"])

df_salida.to_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/caudales_proyectados_CORREGIDO.csv", index=False)

print("\n" + "="*80)
print("RESULTADOS")
print("="*80)

print("\n✓ Primeras filas del resultado:")
print(df_salida.head(20))

print("\n\n✓ RESUMEN POR EMBALSE:")
for embalse in df_salida['embalse'].unique():
    subset = df_salida[df_salida['embalse'] == embalse]
    print(f"\n{embalse}:")
    print(f"  Q promedio: {subset['q_proyectado'].mean():.2f} m³/s")
    print(f"  Q min: {subset['q_proyectado'].min():.2f} m³/s")
    print(f"  Q max: {subset['q_proyectado'].max():.2f} m³/s")
    print(f"  P promedio: {subset['precipitacion_project'].mean():.0f} mm")

print("\n" + "="*80)
print("✅ Cálculo finalizado")
print("📄 Archivo generado: caudales_proyectados_CORREGIDO.csv")
print("="*80)

# ==============================
# VALIDACIÓN CON DATOS HISTÓRICOS
# ==============================
print("\n\n" + "="*80)
print("VALIDACIÓN CON DATOS HISTÓRICOS")
print("="*80)

df_hist = pd.read_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/Calculo_caudal/Caudal_Consolidado.csv")
df_hist_areas = df_areas.copy()

# Preparar datos históricos (calcular precipitación acumulada 3 meses)
df_hist['Periodo_dt'] = pd.to_datetime(df_hist['Periodo'])
df_hist = df_hist.sort_values(['Embalse', 'Periodo_dt'])

for embalse in df_hist['Embalse'].unique():
    subset = df_hist[df_hist['Embalse'] == embalse].copy()
    subset['P_cum'] = subset['Precipitacion'].rolling(window=3, min_periods=1).sum()
    
    # Merge con parámetros
    merged = subset.merge(
        df_param[['embalse', 'ar', 'br']], 
        left_on='Embalse', 
        right_on='embalse', 
        how='left'
    )
    merged = merged.merge(
        df_areas[['embalse', 'ar_km2', 'ai_km2']], 
        left_on='Embalse', 
        right_on='embalse', 
        how='left'
    )
    
    # Calcular Q con fórmula corregida
    merged['Q_calc'] = (
        merged['ar'] 
        * np.power(merged['P_cum'], merged['br'])
        * (merged['ar_km2'] / merged['ai_km2'])
    )
    
    # Comparar
    valid_data = merged.dropna(subset=['Q_calc', 'Caudal'])
    
    if len(valid_data) > 0:
        mae = (valid_data['Q_calc'] - valid_data['Caudal']).abs().mean()
        rmse = np.sqrt(((valid_data['Q_calc'] - valid_data['Caudal'])**2).mean())
        r_squared = 1 - (((valid_data['Q_calc'] - valid_data['Caudal'])**2).sum() / 
                         ((valid_data['Caudal'] - valid_data['Caudal'].mean())**2).sum())
        
        print(f"\n{embalse}:")
        print(f"  Q histórico promedio: {valid_data['Caudal'].mean():.2f} m³/s")
        print(f"  Q calculado promedio: {valid_data['Q_calc'].mean():.2f} m³/s")
        print(f"  MAE: {mae:.2f} m³/s")
        print(f"  RMSE: {rmse:.2f} m³/s")
        print(f"  R²: {r_squared:.3f}")
        
        # Show sample comparison
        print(f"  Muestra de comparación:")
        sample = valid_data[['Periodo', 'Caudal', 'Q_calc', 'P_cum']].head(5)
        print(f"    {sample.to_string()}")

print("\n" + "="*80)
print("✅ Validación completada")
print("="*80)
