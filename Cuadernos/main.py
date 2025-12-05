import marimo

__generated_with = "0.18.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    from pydataxm import pydataxm
    from pydataxm.pydatasimem import CatalogSIMEM

    return (pydataxm,)


@app.cell
def _(pydataxm):
    client = pydataxm.ReadDB()

    # Get all available metrics and entities
    all_metrics = client.get_collections()

    # Get specific collection information
    price_metrics = client.get_collections("PrecBolsNaci")
    return (price_metrics,)


@app.cell
def _(price_metrics):
    price_metrics
    return


if __name__ == "__main__":
    app.run()
