#utils functions
import re
import pandas as pd 

def get_url_details(url):
    url_details = dict()
    
    numeric_pattern = r'-?\d+\.\d+'
    numeric_values = re.findall(numeric_pattern, url)
    url_details['start_coordinates_x'] = numeric_values[0]
    url_details['start_coordinates_y'] = numeric_values[2]
    url_details['end_coordinates_x'] = numeric_values[1]
    url_details['end_coordinates_u'] = numeric_values[3]

    text_pattern = r'/([^/]+)/([^/]+)/([^/]+)/([^/]+)'
    match = re.search(text_pattern, url)
    url_details['website'] = match.group(1)
    url_details['operation'] = match.group(2)
    url_details['property_type'] = match.group(3)
    url_details['location'] = match.group(4)
    return(url_details)

x = get_url_details(r'https://www.portalinmobiliario.com/venta/departamento/renaca-vina-del-mar-valparaiso-valparaiso/_OrderId_PRICE*DESC_NoIndex_True_item*location_lat:-32.97846822579704*-32.97434605890361,lon:-71.54722782799298*-71.53869840332563')
