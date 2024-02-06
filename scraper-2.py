from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import re
from datetime import datetime
import time
import numpy as np
from openpyxl import load_workbook

# Url con la página 1 para iniciar la búsqueda. Debe especificarse una ciudad y rango de precios. #


url = r'https://www.portalinmobiliario.com/venta/departamento/renaca-vina-del-mar-valparaiso-valparaiso/_OrderId_PRICE*DESC_NoIndex_True_item*location_lat:-32.97846822579704*-32.97434605890361,lon:-71.54722782799298*-71.53869840332563'
# Extraer atributos del punto de partida, como el sector donde se buscará y las coordenadas. #
numeric_values = re.findall(r'-?\d+\.\d+', url)
start_coord = numeric_values[0],numeric_values[2]
end_coord = numeric_values[1],numeric_values[3]
search_location = re.search(r'/departamento/([^/-]+)-', url).group(1)

# Variables para empezar a iterar
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
    if soup.find_all('a', class_='andes-pagination__link', href=True)[1].get('href') != '':
        url = soup.find_all('a', class_='andes-pagination__link', href=True)[1].get('href')
    else:
        next_page_url = False
    i+=1
    print('Propiedades encontradas hasta ahora:',len(set_of_urls),'Páginas revisadas:',i)

set_of_urls = list(set_of_urls)
print('Todas las páginas escaneadas con propiedades en',search_location)
