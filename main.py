from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re
from datetime import datetime
import time
import numpy as np
from openpyxl import load_workbook
from datetime import datetime
import os

from utils import *
from fetch_property_data import * 
from locations import locations_coordinates
from map_plotter import generate_search_grid_points

location = 'renaca'
print('Iniciando busqueda de propiedades en',location)
start_point, end_point = locations_coordinates[location]
grid_points = generate_search_grid_points(start_point, end_point)
n = 1
for cell in grid_points:
    print('Escaneando celda:',n)
    url = generate_location_url(cell[0],cell[2])
    search_details = get_url_details(url)
    set_of_urls = set()
    next_page_url = True
    i = 0
    while next_page_url:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        enlaces = soup.find_all('a', class_='ui-search-result__image ui-search-link', href=True)
        for link in enlaces:
            set_of_urls.add(link.get('href'))
        next_page = soup.find_all('a', class_='andes-pagination__link', href=True)
        try:
            if soup.find_all('a', class_='andes-pagination__link', href=True)[1].get('href') != '':
                url = soup.find_all('a', class_='andes-pagination__link', href=True)[1].get('href')
            else:
                next_page_url = False
        except:
            next_page_url = False
        i+=1
        print('Se revisaron',i,'páginas en el área de la celda',n,'y se encontraron',len(set_of_urls))

    set_of_urls = list(set_of_urls)
    print('Todas las páginas escaneadas con propiedades en',location)

    raw_columns = [
        'url', 'title','type','published', 'price', 'maintenance', 'size', 'bedrooms', 'bathrooms',
        'broker', 'adress', 'google_maps_pin', 'secondary_attributes', 'description'
    ]
    # Inicializar un DataFrame vacío con las columnas
    raw_properties_df = pd.DataFrame(columns=raw_columns)
    for j in len(set_of_urls):
        print('Propiedad numero:',j,set_of_urls[j])
        try:
            raw_properties_df = raw_properties_df.append(extract_property_raw_data(set_of_urls[j]))
            print('Exito')
        except:
            print('Fallido')
            pass

    current_time_text = str(datetime.now()).replace(':','.')
    csv_name = search_details['operation']+'-' +search_details['property_type'] +'-'+location+'_'+current_time_text+'.csv'
    path_save = os.path.join('properties_raw_data', csv_name)
    if not os.path.exists('properties_raw_data'):
        os.makedirs('properties_raw_data')
    raw_properties_df.to_csv(path_save, index=False)
    n+=1
    break
