from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re
from datetime import datetime
import time
import numpy as np
from openpyxl import load_workbook

# Url con la página 1 para iniciar la búsqueda. Debe especificarse una ciudad y rango de precios. #
url = r'https://www.portalinmobiliario.com/venta/departamento/_PriceRange_0CLF-4000CLF_item*location_lat:-33.031038768693136*-32.99807568837874,lon:-71.58067156573888*-71.51243616840001'
enlace = True
enlaces_list = [url]
while enlace: # Ciclo para obtener las url de cada página de busqueda y guardarlos en la lista "enlaces_list". #
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        ultima_etiqueta_li = soup.find('nav', {'aria-label': 'Paginación'}).find('ul', {'class': 'andes-pagination'}).find_all('li')[-1]
        enlace = ultima_etiqueta_li.find('a', {'class': 'andes-pagination__link'}).get('href')
        if enlace:
            enlaces_list.append(enlace)
            url = enlace
            print("Enlace encontrado:", url)
result_df = pd.DataFrame(columns=['link','titulo','precio', 'tipo_venta', 'num_banos', 'superficie', 'ubicacion']) # Se inicializa el dataframe vacío. #
for url in enlaces_list: # Se itera página por página para extraer los datos de todas las propiedades en tal página. #
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    html_div= soup.find_all("div") # Los datos se encuentran en un tag div. #
    for div in html_div:
        try:
            if type(div.get("class")) is not type(None):
                if div.get("class")[0]== 'ui-search-result__content':
                    link = div.find('a', {'class': 'ui-search-link'}).get('href')
                    titulo = div.find('div', class_='ui-search-item__title-label-grid').get_text(strip=True)
                    precio = div.find('span', class_='andes-money-amount__fraction').get_text(strip=True)
                    tipo_venta = div.find('div', class_='ui-search-item__subtitle-grid').get_text(strip=True)
                    num_banos = div.find('li', class_='ui-search-card-attributes__attribute', string=re.compile(r'\bbaño\b', flags=re.IGNORECASE)).get_text(strip=True)
                    superficie = div.find('li', class_='ui-search-card-attributes__attribute', string=re.compile(r'\bm²\b', flags=re.IGNORECASE)).get_text(strip=True)
                    ubicacion = div.find('p', class_='ui-search-item__location-label').get_text(strip=True)
                    new_data = {
                        'link': [link],
                        'titulo': [titulo],
                        'precio': [precio],
                        'tipo_venta': [tipo_venta],
                        'num_banos': [num_banos],
                        'superficie': [superficie],
                        'ubicacion': [ubicacion]
                        }
                    new_df = pd.DataFrame(new_data)
                    result_df = result_df.append(new_df, ignore_index=True)
                    print(new_df)
        except:
            pass


#cleaning
result_df['precio'] = result_df['precio'].apply(lambda x: int(x.replace('.', ''))).apply(lambda x: np.round(x / 36721.16,0) if x > 100000 else x)
result_df['metros_cuadrados'] = result_df['superficie'].str.extract(r'(\d+)', expand=False).astype(int)
result_df['precio_metro_cuadrado'] = result_df['precio']/result_df['metros_cuadrados'] 
result_df['fecha_hora_de_carga'] = datetime.now()

csv_filename = 'propiedades.csv'

# Intentar cargar el archivo existente
try:
    # Cargar el archivo CSV existente si está presente
    existing_df = pd.read_csv(csv_filename)
    # Concatenar el DataFrame existente con el nuevo DataFrame
    result_df = pd.concat([existing_df, result_df], ignore_index=True)
except FileNotFoundError:
    # Si el archivo no existe, simplemente utiliza el nuevo DataFrame
    pass

# Guardar el DataFrame en el archivo CSV
result_df.to_csv(csv_filename, index=False, encoding='utf-8')

# Mostrar un mensaje indicando que se han añadido los resultados al archivo CSV
print(f"Resultados añadidos al archivo CSV: {csv_filename}")