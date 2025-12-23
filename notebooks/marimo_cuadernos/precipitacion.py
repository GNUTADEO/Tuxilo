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
    return go, pd


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
    return mapa_estaciones, mapa_estaciones_inv


@app.cell
def _(mapa_estaciones, pd):
    estaciones = {
        k: pd.read_csv(f'../../data/Precipitación/data/originales/{k}.csv')
        for k in mapa_estaciones
    }
    pivotes = {
        k: 1
        for k in mapa_estaciones
    }

    for k, dataframe in estaciones.items():
        dataframe.rename(
            columns={
                'CodigoEstacion': 'Codigo EC',
                'Fecha': 'fecha',
                'Valor': 'valor',
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
        dataframe['fecha'] = pd.to_datetime(dataframe['fecha'])
        dataframe['year'] = dataframe['fecha'].dt.year
        dataframe['month'] = dataframe['fecha'].dt.month
        pivotes[k] = dataframe.pivot(index='year', columns='month', values='valor')
        pivotes[k].rename(columns={
            1:'Enero',
            2:'Febrero',
            3:'Marzo',
            4:'Abril',
            5:'Mayo',
            6:'Junio',
            7:'Julio',
            8:'Agosto',
            9:'Septiembre',
            10:'Octubre',
            11:'Noviembre',
            12:'Diciembre',
        }, inplace=True)
    return estaciones, pivotes


@app.cell
def _():
    selector = 'Betania'
    return (selector,)


@app.cell
def _(estaciones, mapa_estaciones_inv, selector):
    estaciones[mapa_estaciones_inv[selector]]
    return


@app.cell
def _(mapa_estaciones_inv, pivotes, selector):
    pivotes[mapa_estaciones_inv[selector]]
    return


@app.cell
def _(estaciones, go, mapa_estaciones_inv):
    class Plotter:
        def __init__(self, selector: str):
            self.selector = selector
            self.df = estaciones[mapa_estaciones_inv[selector]]

        def plot(self):
            fig = go.Figure()

            for year in sorted(self.df['year'].unique()):
                dff = self.df[self.df['year'] == year]

                fig.add_trace(
                    go.Scatter(
                        x=dff['month'],
                        y=dff['valor'],
                        mode='lines',
                        name=str(year),
                        opacity=0.6,
                    )
                )

            fig.update_layout(
                title=f'Monthly precipitation by year – {self.selector}',
                xaxis_title='Month',
                yaxis_title='Precipitation',
                xaxis=dict(dtick=1),
            )
            print(f'Saving {self.selector}')
            fig.write_html(
                f'../../data/Precipitación/graficas/{self.selector}.html'
            )

    return (Plotter,)


@app.cell
def _(Plotter, mapa_estaciones_inv):
    for s in mapa_estaciones_inv:
        Plotter(s).plot()
    return


@app.cell
def _():
    first_half = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
    second_half = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

    return first_half, second_half


@app.cell
def _(first_half, mapa_estaciones_inv, pd, pivotes, second_half):
    for est in mapa_estaciones_inv:

        pivot = pivotes[mapa_estaciones_inv[est]]
    
        semestres = pd.DataFrame({
            '1s': pivot[first_half].mean(axis=1),
            '2s': pivot[second_half].mean(axis=1),
        })
    
        df_semestres = (
            semestres
            .reset_index(names='year')
            .melt(
                id_vars='year',
                var_name='semestre',
                value_name='valor'
            )
        )
    
        # 🔹 ADD THIS: enforce semester order
        df_semestres['semestre'] = pd.Categorical(
            df_semestres['semestre'],
            categories=['1s', '2s'],
            ordered=True
        )
    
        # 🔹 ADD THIS: sort properly
        df_semestres = df_semestres.sort_values(
            by=['year', 'semestre']
        )
    
        station_id = mapa_estaciones_inv[est]
    
        # build Periodo AFTER sorting
        df_semestres['Periodo'] = (
            df_semestres['year'].astype(str)
            + '-'
            + df_semestres['semestre'].astype(str)
        )
    
        df_semestres['estacion'] = station_id
    
        df_final = df_semestres[['Periodo', 'estacion', 'valor']]
    
        df_final.rename(
            columns={
                'estacion': 'Codigo EC',
                'valor': 'Precipitación',
            },
            inplace=True
        )
        print(df_final)
        df_final.to_csv(f'../../data/Precipitación/data/limpios/{est}.csv', index=False)

    return


@app.cell
def _(mapa_estaciones_inv, pivotes, selector):
    pivotes[mapa_estaciones_inv[selector]].info(verbose=True)
    return


if __name__ == "__main__":
    app.run()
