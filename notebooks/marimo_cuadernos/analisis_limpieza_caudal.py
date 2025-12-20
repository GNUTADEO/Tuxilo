import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Limpieza y exploración de los datos del caudal
    """)
    return


@app.cell(hide_code=True)
def _():
    import pandas as pd, numpy as np , matplotlib.pyplot as plt, math
    from pathlib import Path
    from datetime import datetime
    return Path, math, np, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Leer datos
    """)
    return


@app.cell(hide_code=True)
def _(Path, pd):
    dfs = {}

    def read_data():
        for csv_file in Path("data/GRDC/").glob("*_Q_Day.Cmd.txt"):
            station_id = csv_file.stem.split("_")[0]
            df = pd.read_csv(csv_file, sep=";", comment="#", encoding="latin1", na_values=["-999.000"], skipinitialspace=True)
            df = df.drop(columns=["hh:mm"])
            dfs[station_id] = df
    read_data()
    return (dfs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Visualizar datos originales
    """)
    return


@app.cell(hide_code=True)
def _(dfs, math, np, plt):
    def visu_data(dfs, column="Value"):
        n = len(dfs)
        cols = 3
        rows = math.ceil(n / cols)
    
        fig, axes = plt.subplots(rows, cols, figsize=(15, 4 * rows))
        axes = axes.flatten()
    
        for ax, (name, df2) in zip(axes, dfs.items()):
            data = df2[column].replace(-999, np.nan).dropna()
            ax.hist(data, bins=50)
            ax.set_title(f"{name} - {df2["YYYY-MM-DD"].min()} a {df2["YYYY-MM-DD"].max()} {df2[column].isna().sum()} nulos")
            ax.set_xlabel("Value")
            ax.set_ylabel("Freq")
        del(data)
        # Hide empty subplots
        for ax in axes[len(dfs):]:
            ax.axis("off")
    
        plt.tight_layout()
        plt.show()

    visu_data(dfs)
    return (visu_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Reemplazar nulos y guardar
    """)
    return


@app.cell(hide_code=True)
def _(dfs, np, pd):
    rng = np.random.default_rng(seed=42)

    dfs_imputed = {}

    for station_id, df in dfs.items():
        df = df.copy()

        # 1. Ensure datetime
        df["YYYY-MM-DD"] = pd.to_datetime(
            df["YYYY-MM-DD"],
            errors="coerce"
        )

        # 2. Extract month
        df["month"] = df["YYYY-MM-DD"].dt.month

        # 3. Build monthly distributions
        monthly_distributions = {
            month: values.dropna().values
            for month, values in df.groupby("month")["Value"]
        }

        # 4. Imputation function
        def impute_value(row):
            if pd.isna(row["Value"]):
                dist = monthly_distributions.get(row["month"], [])
                if len(dist) > 0:
                    return rng.choice(dist)
            return row["Value"]

        # 5. Apply imputation
        df["Value_imputed"] = df.apply(impute_value, axis=1)
        df.to_csv(f"data/GRDC/{station_id}_Q_Day_Clean.Cmd.txt", sep=";", index=False, na_rep="-999.000")
        # 6. Store result
        dfs_imputed[station_id] = df

    return (dfs_imputed,)


@app.cell(hide_code=True)
def _(dfs_imputed, visu_data):
    visu_data(dfs_imputed, column="Value_imputed")
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
