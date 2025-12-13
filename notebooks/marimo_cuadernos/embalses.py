import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Objetos SIMEM
    """)
    return


@app.cell(hide_code=True)
def _():
    from pydataxm.pydatasimem import CatalogSIMEM, ReadSIMEM
    catalogo_conjuntos = CatalogSIMEM('Datasets')
    return ReadSIMEM, catalogo_conjuntos


@app.cell(hide_code=True)
def _(catalogo_conjuntos):
    catalogo_conjuntos.get_data()
    return


@app.cell(hide_code=True)
def _(ReadSIMEM):
    dataset_id = 'A0CF2A'
    fecha_inicio = '2024-04-01'
    fecha_fin = '2024-04-30'
    generacion = ReadSIMEM(dataset_id, fecha_inicio, fecha_fin)
    return (generacion,)


@app.cell(hide_code=True)
def _(generacion):
    dir(generacion)
    return


@app.cell(hide_code=True)
def _(generacion):
    generacion.get_columns()
    return


@app.cell(hide_code=True)
def _(generacion):
    embalses = generacion.main()['NombreEmbalse'].unique()
    return (embalses,)


@app.cell(hide_code=True)
def _(embalses):
    embalses.sort()
    print(embalses)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Objetos SINERGOX - XM
    """)
    return


@app.cell
def _():
    from pydataxm.pydataxm import ReadDB

    # Construir la clase que contiene los métodos de pydataxm
    objetoAPI = ReadDB()
    objetoAPI.get_collections()
    return (objetoAPI,)


@app.cell
def _(objetoAPI):
    help(objetoAPI.request_data)
    return


@app.cell
def _(objetoAPI):
    objetoAPI.get_collections('ListadoEmbalses')
    return


@app.cell
def _(objetoAPI):
    objetoAPI.request_data('ListadoEmbalses', 'Sistema', '2024-01-01', '2025-12-31')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Información Geográfica de los Embalses
    """)
    return


@app.cell
def _():
    import pandas as pd 
    return (pd,)


@app.cell
def _(pd):
    df = pd.read_csv("../../data/XM/EmbalsesColombia.csv", delimiter=",", encoding="utf-8")
    df.head()
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
