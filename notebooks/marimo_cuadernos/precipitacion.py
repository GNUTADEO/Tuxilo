import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    import pandas as pd
    import plotly
    import folium
    return


app._unparsable_cell(
    r"""
    import
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
