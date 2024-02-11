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
from locations import locations_url
#from map_plotter import generate_search_grid_points

location = 'Reñaca'
url = locations_url[location]
print('Iniciando busqueda de propiedades en',location,'\n',url)
try:
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
        print('Se han escaneado',i,'página/s con un acumulado de',len(set_of_urls),'propiedades.')
    total_properties_expected = soup.find('div','ui-search-search-result').span.text
    print('Total de propiedades esperadas:', total_properties_expected)
    set_of_urls = list(set_of_urls)
    raw_columns = [
            'url', 'title','type','published', 'price', 'maintenance', 'size', 'bedrooms', 'bathrooms',
            'broker', 'adress', 'google_maps_pin', 'secondary_attributes', 'description'
        ]
    # Inicializar un DataFrame vacío con las columnas
    raw_properties_df = pd.DataFrame(columns=raw_columns)
    for j in range(20):
        print('Propiedad numero:',j+1,set_of_urls[j])
        try:
            raw_properties_df = raw_properties_df.append(extract_property_raw_data(set_of_urls[j]))
        except:
            print('Fallido')
            pass

    current_time_text = str(datetime.now()).replace(':','.')
    csv_name = search_details['operation']+'-' +search_details['property_type'] +'-'+location+'_'+current_time_text+'.csv'
    path_save = os.path.join('properties_raw_data', csv_name)
    if not os.path.exists('properties_raw_data'):
        os.makedirs('properties_raw_data')
    raw_properties_df.to_csv(path_save, index=False)
except:
    print('No se pudo completar la busqueda.')
    pass
