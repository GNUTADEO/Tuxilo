import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import csv
    import numpy as np
    return mo, np, pd


@app.cell
def _(pd):
    # Cargar el archivo
    tsm = pd.read_excel('C22-4CondicionesClim-Fig1-ComporONI.xlsx')

    # La columna 'Unnamed: 0' es el nombre de cada variable → usar como índice
    tsm = tsm.set_index('Unnamed: 0')

    # Convertir columnas (fechas) a datetime
    tsm.columns = pd.to_datetime(tsm.columns)

    # Transponer
    tsm_volteado = tsm.T
    return (tsm_volteado,)


@app.cell
def _(tsm_volteado):
    tsm_volteado["YEAR"] = tsm_volteado.index.year
    tsm_volteado["MONTH"] = tsm_volteado.index.month
    return


@app.cell
def _(tsm_volteado):
    tsm_filtrada = tsm_volteado[
        ((tsm_volteado["YEAR"] == 2017) & (tsm_volteado["MONTH"] >= 10)) |
        ((tsm_volteado["YEAR"] > 2017) & (tsm_volteado["YEAR"] < 2021)) | 
        ((tsm_volteado["YEAR"] == 2021) & (tsm_volteado["MONTH"] <= 7))]

    return (tsm_filtrada,)


@app.cell
def _(tsm_filtrada):
    tsm_drop = tsm_filtrada.drop(columns=['Umbral La Niña', 'Umbral El Niño', 'Anomalías de Aportes Agregados al SIN', 'YEAR', 'MONTH'])
    return (tsm_drop,)


@app.cell
def _(tsm_drop):
    tsm_drop
    return


@app.cell
def _(np, pd):
    enso = 'meiv2.data.txt'

    df = pd.read_csv(enso, 
                     delim_whitespace=True,
                     skiprows=1,  
                     skipfooter=4,
                     engine='python',
                     names=["YEAR", "DJ", "JF", "FM", "MA", "AM", "MJ", 
                            "JJ", "JA", "AS", "SO", "ON", "ND"])

    # Convertir a numérico y reemplazar -999.00 con NaN
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.replace(-999.00, np.nan)
    return (df,)


@app.cell
def _(df):
    df_filtered = df[(df['YEAR'] >= 2017) & (df['YEAR'] <= 2019)]
    print(f"Forma original: {df.shape}")
    print(f"Forma filtrada: {df_filtered.shape}")
    return (df_filtered,)


@app.cell
def _(df_filtered):
    df_filtered
    return


@app.cell
def _(df_filtered):
    df_long = df_filtered.melt(
        id_vars=["YEAR"],
        value_vars=["DJ", "JF", "FM", "MA", "AM", "MJ", "JJ", "JA", "AS", "SO", "ON", "ND"],
        var_name="MONTH",
        value_name="VALUE"
    )
    return (df_long,)


@app.cell
def _(df_long):
    month_map = {
        "DJ": 12, "JF": 1, "FM": 2, "MA": 3, "AM": 4, "MJ": 5,
        "JJ": 6, "JA": 7, "AS": 8, "SO": 9, "ON": 10, "ND": 11
    }

    df_long["MONTH_NUM"] = df_long["MONTH"].map(month_map)

    return


@app.cell
def _(df_long, pd):
    df_long["DATE"] = pd.to_datetime(
        df_long["YEAR"].astype(str) + "-" + df_long["MONTH_NUM"].astype(str) + "-01"
    )
    return


@app.cell
def _(df_long):
    df_1= df_long.sort_values("DATE").reset_index(drop=True)
    return


@app.cell
def _(df_long):
    df_final = df_long[["DATE", "VALUE"]].copy()
    return (df_final,)


@app.cell
def _(df_final):
    df_final_2 = df_final.sort_values("DATE").reset_index(drop=True)
    return (df_final_2,)


@app.cell
def _(df_final_2):
    df_final_2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Presencia de los fenomenos por año
    """)
    return


@app.cell
def _():
    from pathlib import Path
    return (Path,)


@app.cell
def _(Path, pd):
    # Load the data
    data_dir = Path('Data/IDEAM')
    oni = pd.read_csv(data_dir / 'IndicesONI.csv', parse_dates=['DATE'])
    indice_tms = pd.read_csv(data_dir / 'IndicesTSM.csv', parse_dates=['Fecha'])

    # Rename columns for consistency
    oni.columns = ['Fecha', 'ONI']
    indice_tms.columns = ['Fecha', 'TSM_Calida', 'TSM_Fria', 'Anomalias_Aportes']

    # Merge datasets
    merge = oni.merge(indice_tms, on='Fecha', how='outer')
    merge = merge.sort_values('Fecha')

    # Extract year
    merge['Year'] = pd.to_datetime(merge['Fecha']).dt.year
    return (merge,)


@app.cell
def _(merge):
    # Classify phenomena
    def classify_phenomenon(row):
        oni_val = row['ONI']
        tsm_calida = row['TSM_Calida']
        tsm_fria = row['TSM_Fria']

        if oni_val < 0 and tsm_fria < 0:
            return 'La Niña'
        elif oni_val > 0 and tsm_calida > 0:
            return 'El Niño'
        else:
            return 'Neutral'


    merge['Fenomeno'] = merge.apply(classify_phenomenon, axis=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Presencia de Fenómenos ENSO por Año

    **Criterios de clasificación:**
    - **La Niña**: ONI < 0 (negativo) Y TSM_Fria < 0 (frío)
    - **El Niño**: ONI > 0 (positivo) Y TSM_Calida > 0 (cálido)
    - **Neutral**: Otros casos
    """)
    return


@app.cell
def _(merge, pd):
    # Calculate presence percentage by year
    summary_data = []

    for year in sorted(merge['Year'].unique()):
        year_data = merge[merge['Year'] == year]
        total_months = len(year_data)

        if total_months > 0:
            nina_count = len(year_data[year_data['Fenomeno'] == 'La Niña'])
            nino_count = len(year_data[year_data['Fenomeno'] == 'El Niño'])
            neutral_count = len(year_data[year_data['Fenomeno'] == 'Neutral'])

            nina_pct = (nina_count / total_months) * 100
            nino_pct = (nino_count / total_months) * 100
            neutral_pct = (neutral_count / total_months) * 100

            summary_data.append({
                'Año': year,
                'Total_Meses': total_months,
                'La_Niña_Meses': nina_count,
                'La_Niña_%': round(nina_pct, 1),
                'El_Niño_Meses': nino_count,
                'El_Niño_%': round(nino_pct, 1),
                'Neutral_Meses': neutral_count,
                'Neutral_%': round(neutral_pct, 1)
            })

    summary_df = pd.DataFrame(summary_data)
    return (summary_df,)


@app.cell
def _(mo, summary_df):
    mo.ui.table(summary_df, selection=None)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Patrones
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
