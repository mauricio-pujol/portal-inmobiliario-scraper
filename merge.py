import pandas as pd 
import os
from utils import *
directorio = 'properties_raw_data'
archivos_csv = [archivo for archivo in os.listdir(directorio) if archivo.endswith('.csv')]
dataframes = []

# Iterar sobre cada archivo y cargarlo en un DataFrame
for archivo in archivos_csv:
    ruta_completa = os.path.join(directorio, archivo)
    df = pd.read_csv(ruta_completa)
    dataframes.append(df)

# Concatenar los DataFrames en uno solo
raw_merge_df = pd.concat(dataframes, ignore_index=True)

#raw_merge_df.to_excel('raw_merge_df.xlsx', index=False)


def calculate_days(description):
    match = re.search(r'(\d+)', description)
    if match:
        cantidad = int(match.group())
        if 'mes' in description:
            dias= cantidad * 30
        elif 'año' in description:
            dias= cantidad * 365
        elif 'día' in description:
            dias= cantidad
    print(description)
    return dias

def clean_to_uf(price,uf_current_value):
    if 'UF' in price:
        return(int(re.sub(r'\D', '', price)))
    else:
        return(int(float(re.sub(r'\D', '', price))/uf_current_value))

def clean_to_clp(price,uf_current_value):
    if 'UF' in price:
        return(int(float(re.sub(r'\D', '', price))*uf_current_value))
    else:
        return(int(float(re.sub(r'\D', '', price))))
    
def clean_maintenance(description):
    if pd.notna(description):
        match = re.search(r'\b(\d+(\.\d+)?)\b', str(description))
        return(int(match.group(1).replace('.','')))
    else:
        return None

def clean_size(size_input):
    match = re.search(r'\b(\d+(\.\d+)?)\b', str(size_input))
    if 'total' in size_input:
        match = re.search(r'\b(\d+(\.\d+)?)\b', str(size_input))
        clean_size = float(match.group(1))
    else:
        clean_size = None
    return clean_size

def clean_room(room_input):
    match = re.search(r'\b\d{1,2}\b', str(room_input))
    if match:
        return int(match.group(0))
    else:
        return None



raw_merge_df
uf_value = get_uf_currente_value()

clean_df = raw_merge_df[['url','title','type','broker','adress']]
clean_df['published_days'] = raw_merge_df['published'].apply(calculate_days)
clean_df['price_uf'] = raw_merge_df['price'].apply(clean_to_uf,uf_current_value = uf_value)
clean_df['price_clp'] = raw_merge_df['price'].apply(clean_to_clp,uf_current_value = uf_value)
clean_df['maintenance'] = raw_merge_df['maintenance'].apply(clean_maintenance)
clean_df['size_m2'] = raw_merge_df['size'].apply(clean_size)
clean_df['bedrooms'] = raw_merge_df['bedrooms'].apply(clean_room)
clean_df['bathrooms'] = raw_merge_df['bathrooms'].apply(clean_room)
clean_df