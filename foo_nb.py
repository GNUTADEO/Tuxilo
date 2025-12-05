import marimo

__generated_with = "0.18.2"
app = marimo.App()


@app.cell
def _():
    from pydataxm.pydataxm import ReadDB  

    # Crear instancia  
    objetoAPI = ReadDB()  
    # Obtener listado de ríos disponibles
    objetoAPI.get_collections()
    return (objetoAPI,)


@app.cell
def _(objetoAPI):
    caudales_filtrados = objetoAPI.request_data(
        coleccion="AporCaudal",
        metrica="Rio",
        start_date="2014-01-01",  
        end_date="2024-01-31",
        filtros=["BOGOTA N.R.", "DESV. MANSO", "FLORIDA II"]
    )

    print(caudales_filtrados)


    # rios_disponibles = objetoAPI.request_data(
    #     coleccion="ListadoRios",  
    #     metrica="Rio",
    #     start_date="1980-01-01",  
    #    end_date="2024-01-31",
    # )

    # print(rios_disponibles)
    return


if __name__ == "__main__":
    app.run()
