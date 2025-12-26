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
    import folium

    import plotly.express as px
    import plotly.graph_objects as go
    return (pd,)


@app.cell
def _():
    mapa_estaciones = {
        '21080030':'Betania',
        '21160040':'Prado',
        '21200620':'Sisga',
        '21200780':'Tomine',
        '21201180':'Neusa',
        '21201320':'Muña',
        '23050250':'Miel',
        '23085110':'Guatape',
        '24015120':'Fuquene',
        '26030150':'Salvajina',
        '35060100':'Guavio',
    }
    mapa_estaciones_inv = {v: k for k, v in mapa_estaciones.items()}
    return (mapa_estaciones,)


@app.cell
def _(mapa_estaciones, pd):
    estaciones = {
        k: pd.read_csv(f'../data/Precipitación/data/originales/{k}.csv')
        for k in mapa_estaciones
    }

    pivotes = {
        k: 1
        for k in mapa_estaciones
    }


    return (estaciones,)


@app.cell
def _():
    selector = 'Betania'
    return


@app.cell
def _(estaciones, mapa_estaciones):
    for k, dataframe in estaciones.items():
        name = mapa_estaciones[k]
        dataframe.rename(
            columns={
                'CodigoEstacion': 'station_id',
                'Fecha': 'observation_date',
                'Valor': 'value',
            },
            inplace=True,
        )

        dataframe.drop(
            columns=[
                'NombreEstacion',
                'Variable',
                'Parametro',
                'Unidad',
                'NivelAprobacion',
            ],
            inplace=True,
        )
        dataframe.to_csv(f'../data/Precipitación/data/mensual/{name}.csv', index=False)
    return


@app.cell
def _(estaciones, pd):
    data_out = pd.concat(
        estaciones.values(),
        ignore_index=True
    )


    data_out.to_csv(f'../data/Precipitación/data/unificado/data.csv', index=False)
    return


@app.cell
def _():
    # for l, dataframe1 in estaciones.items():
    #     dataframe1['observation_date'] = pd.to_datetime(dataframe1['observation_date'])
    #     dataframe1['year'] = dataframe1['observation_date'].dt.year
    #     dataframe1['month'] = dataframe1['observation_date'].dt.month
    #     pivotes[k] = dataframe1.pivot(index='year', columns='month', values='value')
    #     pivotes[k].rename(columns={
    #         1:'Enero',
    #         2:'Febrero',
    #         3:'Marzo',
    #         4:'Abril',
    #         5:'Mayo',
    #         6:'Junio',
    #         7:'Julio',
    #         8:'Agosto',
    #         9:'Septiembre',
    #         10:'Octubre',
    #         11:'Noviembre',
    #         12:'Diciembre',
    #     }, inplace=True)
    return


@app.cell
def _():
    # class Plotter:
    #     def __init__(self, selector: str):
    #         self.selector = selector
    #         self.df = estaciones[mapa_estaciones_inv[selector]]

    #     def plot(self):
    #         fig = go.Figure()

    #         for year in sorted(self.df['year'].unique()):
    #             dff = self.df[self.df['year'] == year]

    #             fig.add_trace(
    #                 go.Scatter(
    #                     x=dff['month'],
    #                     y=dff['valor'],
    #                     mode='lines',
    #                     name=str(year),
    #                     opacity=0.6,
    #                 )
    #             )

    #         fig.update_layout(
    #             title=f'Monthly precipitation by year – {self.selector}',
    #             xaxis_title='Month',
    #             yaxis_title='Precipitation',
    #             xaxis=dict(dtick=1),
    #         )
    #         print(f'Saving {self.selector}')
    #         fig.write_html(
    #             f'../data/Precipitación/graficas/{self.selector}.html'
    #         )
    return


@app.cell
def _():
    # for s in mapa_estaciones_inv:
    #     Plotter(s).plot()
    return


@app.cell
def _():
    # first_half = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
    # second_half = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    return


@app.cell
def _():
    # for est in mapa_estaciones_inv:

    #     pivot = pivotes[mapa_estaciones_inv[est]]

    #     semestres = pd.DataFrame({
    #         '1s': pivot[first_half].mean(axis=1),
    #         '2s': pivot[second_half].mean(axis=1),
    #     })

    #     df_semestres = (
    #         semestres
    #         .reset_index(names='year')
    #         .melt(
    #             id_vars='year',
    #             var_name='semestre',
    #             value_name='valor'
    #         )
    #     )

    #     # 🔹 ADD THIS: enforce semester order
    #     df_semestres['semestre'] = pd.Categorical(
    #         df_semestres['semestre'],
    #         categories=['1s', '2s'],
    #         ordered=True
    #     )

    #     # 🔹 ADD THIS: sort properly
    #     df_semestres = df_semestres.sort_values(
    #         by=['year', 'semestre']
    #     )

    #     station_id = mapa_estaciones_inv[est]

    #     # build Periodo AFTER sorting
    #     df_semestres['Periodo'] = (
    #         df_semestres['year'].astype(str)
    #         + '-'
    #         + df_semestres['semestre'].astype(str)
    #     )

    #     df_semestres['estacion'] = station_id

    #     df_final = df_semestres[['Periodo', 'estacion', 'valor']]

    #     df_final.rename(
    #         columns={
    #             'estacion': 'Codigo EC',
    #             'valor': 'Precipitación',
    #         },
    #         inplace=True
    #     )
    #     print(df_final)
    #     df_final.to_csv(f'../data/Precipitación/data/semestral/{est}.csv', index=False)
    return


if __name__ == "__main__":
    app.run()
