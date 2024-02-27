import pandas as pd 
import os
from function_utils import *
directory = 'extracted_data'
csv_files = [file for file in os.listdir(directory) if file.endswith('.csv')]
dataframes = []

for file in csv_files:
    ruta_completa = os.path.join(directory, file)
    df = pd.read_csv(ruta_completa)
    df = df[~df['type'].str.contains('proyecto', case=False, na=False)] # Esto excluye los proyectos
    date = re.search(r'(\d{4}-\d{2}-\d{2})',file).group(0)
    df['load_date'] = date
    dataframes.append(df)

raw_merge_df = pd.concat(dataframes, ignore_index=True)

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
    else:
        return None
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

def clean_room(room_input,room_type):
    match = re.search(r'\b\d{1,2}\b', str(room_input))
    if match and room_type in room_input.lower():
        return int(match.group(0))
    else:
        return None

def clean_room(room_input, room_type):
    bedroom_pattern = re.compile(r'(\d+)\s*dormitorio', re.IGNORECASE)
    bathroom_pattern = re.compile(r'(\d+)\s*baño', re.IGNORECASE)
    room_pattern = bathroom_pattern if room_type.lower() == 'baño' else bedroom_pattern
    match = room_pattern.search(str(room_input))
    return int(match.group(1)) if match else None

def clean_map_location(location_input):
    match = re.search(r'center=(-?\d+\.\d+)%2C(-?\d+\.\d+)', location_input)
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return {'latitude': latitude, 'longitude': longitude}
    else:
        return None
    
def clean_secondary_details(detail_input, detail_type):
    # Construir el patrón de expresión regular con la categoría proporcionada
    pattern = re.compile(f'{detail_type}: ([^,]*)', re.IGNORECASE)
    
    # Buscar la coincidencia en el texto
    match = pattern.search(str(detail_input))
    
    # Devolver la información si hay una coincidencia, de lo contrario, None
    return match.group(1).strip() if match else None

def clean_orientation(orientation_input):
    cleaned_orientation = ''
    if orientation_input is not None: 
        if 'nor' in orientation_input.lower():
            cleaned_orientation += 'N'
        if 'sur' in orientation_input.lower():
            cleaned_orientation += 'S'
        if 'pon' in orientation_input.lower():
            cleaned_orientation += 'P'
        if 'ori' in orientation_input.lower():
            cleaned_orientation += 'O'
    if cleaned_orientation == '' or orientation_input == '-':
        cleaned_orientation = None
    if orientation_input in ('N','S','P','O','NP','NO','NS','SP','SO','SP','OSP','NOSP','NSO','NOP'):
        cleaned_orientation = orientation_input
    return cleaned_orientation

def clean_age(age_input):
    match = re.match(r'-?\b\d+\b', str(age_input))
    if match and int(match.group(0)) <100:
        return int(match.group(0))
    else:
        return None
    
def extract_orientation(orientation_input,orientation_selected):
    if orientation_input is None or orientation_input.isdigit() or orientation_input in '-' or 'consult' in orientation_input.lower():
        return None
    if (orientation_selected[0:3].lower() in orientation_input.lower()) or (len(orientation_input) <= 4 and orientation_selected[0] in orientation_input) or 'tod' in orientation_input.lower():
        return True
    else:
        return False

raw_merge_df
uf_value = get_uf_currente_value()

clean_df = raw_merge_df[['url','title','type','broker','address']].copy()
clean_df['published_days'] = raw_merge_df['published'].apply(calculate_days)
clean_df['price_uf'] = raw_merge_df['price'].apply(clean_to_uf,uf_current_value = uf_value)
clean_df['price_clp'] = raw_merge_df['price'].apply(clean_to_clp,uf_current_value = uf_value)
clean_df['maintenance'] = raw_merge_df['maintenance'].apply(clean_maintenance)
clean_df['size_m2'] = raw_merge_df['size'].apply(clean_size)
clean_df['price_uf_m2'] =(clean_df['price_uf']/clean_df['size_m2']).round(1)
clean_df['bedrooms'] = raw_merge_df['rooms'].apply(clean_room, room_type='dormitorio').astype('Int64').fillna(0)
clean_df['bathrooms'] = raw_merge_df['rooms'].apply(clean_room, room_type='baño')
clean_df['location_latitude'] = raw_merge_df['google_maps_pin'].apply(clean_map_location).apply(lambda x: x['latitude'])
clean_df['location_longitude'] = raw_merge_df['google_maps_pin'].apply(clean_map_location).apply(lambda x: x['longitude'])
clean_df['orientation'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Orientación')
clean_df['orientation_north'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Orientación').apply(extract_orientation,orientation_selected = 'Norte')
clean_df['orientation_south'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Orientación').apply(extract_orientation,orientation_selected = 'Sur')
clean_df['orientation_east'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Orientación').apply(extract_orientation,orientation_selected = 'Oriente')
clean_df['orientation_west'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Orientación').apply(extract_orientation,orientation_selected = 'Poniente')
clean_df['pool'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Piscina').apply(clean_orientation).map({"Sí": True, "No": False, None: False})
clean_df['parking'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Estacionamientos').astype(int)
clean_df['elevator'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Ascensor').map({"Sí": True, "No": False, None: False})
clean_df['balcony'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Terraza').map({"Sí": True, "No": False, None: False})
clean_df['storage'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Bodegas').fillna(0).astype(int).apply(lambda x: None if x > 5 else int(x))
clean_df['age'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Antigüedad').apply(clean_age)
clean_df['floor'] = raw_merge_df['secondary_attributes'].apply(clean_secondary_details, detail_type='Número de piso de la unidad').apply(lambda x: int(x) if x is not None and x.isdigit() and int(x) <= 50 else None)
clean_df['load_date'] = raw_merge_df['load_date']
clean_df