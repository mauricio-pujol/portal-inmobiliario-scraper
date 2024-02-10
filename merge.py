import pandas as pd 
import os

directorio = 'properties_raw_data'
archivos_csv = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.csv')]
dataframes = []

# Iterar sobre cada archivo y cargarlo en un DataFrame
for archivo in archivos_csv:
    ruta_completa = os.path.join(directorio, archivo)
    df = pd.read_csv(ruta_completa)
    dataframes.append(df)

# Concatenar los DataFrames en uno solo
resultado_final = pd.concat(dataframes, ignore_index=True)

resultado_final.to_excel('resultado_final.xlsx', index=False)