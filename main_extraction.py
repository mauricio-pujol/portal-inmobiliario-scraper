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

from function_utils import *
from function_scrape_property import * 
from dictionary_locations import locations_url

location = 'Viña del Mar' # Specify the city or area to search for properties. The URL for the location to be searched should be defined in the location.py file.
url = locations_url[location] # locations_url is a dictionary defined in locations.py which contains location:url to search.
print('Initializing property scraper for',location,'\n',url)
try: # Before scraping individual webpages, a set of all propertys urls to scan is generated.
    print('Step 1/3: Generating set of URLs to scan.')
    search_details = get_url_details(url) # Function to obtain website, operation and property type of to search. This further determines the resulting .csv file name.
    set_urls = set()  # Empty set to fill with URLs to further scan.
    next_page_url = True
    i = 0
    while next_page_url: # Iterate until there's no "next page" to look for.
        print(url)
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        href_links = soup.find_all('a', class_='ui-search-result__image ui-search-link', href=True) # Extracts all urls of propertys in current page
        for link in href_links:
            set_urls.add(link.get('href'))
        next_page = soup.find_all('a', class_='andes-pagination__link', href=True)
        try:
            if soup.find_all('a', class_='andes-pagination__link', href=True)[-1].get('href') != '': # Looks for the "next page" URL. If it isn't found, then all pages were scanned.
                url = soup.find_all('a', class_='andes-pagination__link', href=True)[-1].get('href')
            else:
                next_page_url = False
        except:
            next_page_url = False
        i+=1
        print('Scanned', i, 'page(s) with', len(set_urls), 'properties.')
    total_properties_expected = soup.find('div','ui-search-search-result').span.text 
    print('Total expected properties:', total_properties_expected.replace('.','')) # Prints the expected number of property, which should equal the number of URLs in set_urls.
    print('\n Step 2/3: Scan individually each page to extract every property attributes.')
    list_urls = list(set_urls)
    list_raw_columns = ['url', 'title','type','published', 'price', 'maintenance', 'size', 'rooms','broker', 'address', 'google_maps_pin', 'secondary_attributes', 'description']
    df_raw_data = pd.DataFrame(columns=list_raw_columns) # Initialize an empty DataFrame with the specified columns to fill with data of each property to scan.
    list_urls_failed = list() # Another list is created to add failed to scrape URLs to help debug.
    for j in range(len(set_urls)):
        print('Number of property to scan:',j+1,'of',len(set_urls),list_urls[j])
        try:
            df_raw_data = df_raw_data.append(extract_property_raw_data(list_urls[j]))
        except:
            print('Failed to scan propery URL. The URL is added to list_urls_failed.')
            list_urls_failed.append(list_urls[j])
            pass
    print('\n Step 3/3: Save into a .csv file the generated dataframe.')
    text_current_time = str(datetime.now()).replace(':','.') 
    csv_name = search_details['operation']+'-' +search_details['property_type'] +'-'+location+'_'+text_current_time+'.csv'
    path_save = os.path.join('extracted_data', csv_name)
    if not os.path.exists('extracted_data'):
        os.makedirs('extracted_data')
    df_raw_data.to_csv(path_save, index=False)
    print('The file',csv_name,'has been generated. Out of',len(set_urls),'properties,',j+1,'were scanned successfully and',len(list_urls_failed),'unsuccessfully.')
    if len(list_urls_failed) >= 1:
        txt_name = search_details['operation'] + '-' + search_details['property_type'] + '-' + location + '_' + text_current_time + 'exceptions.txt'
        with open(txt_name, 'w') as exceptions_file:
            exceptions_file = '\n'.join(list_urls_failed)
            exceptions_file.write(exceptions_file)

except:
    print('Failed to initialize.')
    pass
