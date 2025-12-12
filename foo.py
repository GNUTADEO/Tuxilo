from pydataxm.pydataxm import ReadDB  
  
# Crear instancia  
# objetoAPI = ReadDB()  
  
# Obtener listado de ríos disponibles
objetoAPI.get_collections()


# caudales_filtrados = objetoAPI.request_data(
#     coleccion="AporCaudal",
#     metrica="Rio",
#     start_date="1980-01-01",  
#     end_date="2024-01-31",
#     entity="Rio",
#     filtros=["BOGOTA N.R.", "DESV. MANSO", "FLORIDA II"]  
# )

# print(caudales_filtrados)


# rios_disponibles = objetoAPI.request_data(
#     coleccion="ListadoRios",  
#     metrica="Rio",
#     start_date="1980-01-01",  
#    end_date="2024-01-31",
# )

# print(rios_disponibles)
