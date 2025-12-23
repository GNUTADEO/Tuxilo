import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from pathlib import Path
    return Path, mo, pd


@app.cell
def _(Path, pd):
    # Load the data
    data_dir = Path('Data/IDEAM')
    oni = pd.read_csv(data_dir / 'IndicesONI.csv', parse_dates=['DATE'])
    tsm = pd.read_csv(data_dir / 'IndicesTSM.csv', parse_dates=['Fecha'])

    # Rename columns for consistency
    oni.columns = ['Fecha', 'ONI']
    tsm.columns = ['Fecha', 'TSM_Calida', 'TSM_Fria', 'Anomalias_Aportes']

    # Merge datasets
    df = oni.merge(tsm, on='Fecha', how='outer')
    df = df.sort_values('Fecha')

    # Extract year
    df['Year'] = pd.to_datetime(df['Fecha']).dt.year
    return (df,)


@app.cell
def _(df):
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

    df['Fenomeno'] = df.apply(classify_phenomenon, axis=1)
    return


@app.cell
def _(mo):
    mo.md("""
    # Presencia de Fenómenos ENSO por Año

    **Criterios de clasificación:**
    - **La Niña**: ONI < 0 (negativo) Y TSM_Fria < 0 (frío)
    - **El Niño**: ONI > 0 (positivo) Y TSM_Calida > 0 (cálido)
    - **Neutral**: Otros casos
    """)
    return


@app.cell
def _(df, pd):
    # Calculate presence percentage by year
    summary_data = []

    for year in sorted(df['Year'].unique()):
        year_data = df[df['Year'] == year]
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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
