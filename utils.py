#utils functions
import re
import pandas as pd 
import math
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_url_location(url):
    url_location = dict()
    numeric_pattern = r'-?\d+\.\d+'
    numeric_values = re.findall(numeric_pattern, url)
    url_location['start_coordinates_x'] = numeric_values[0]
    url_location['start_coordinates_y'] = numeric_values[2]
    url_location['end_coordinates_x'] = numeric_values[1]
    url_location['end_coordinates_u'] = numeric_values[3]
    return(url_location)

def get_url_details(url):
    url_details = dict()
    text_pattern = r'/([^/]+)/([^/]+)/([^/]+)/([^/]+)'
    match = re.search(text_pattern, url)
    url_details['website'] = match.group(1)
    url_details['operation'] = match.group(2)
    url_details['property_type'] = match.group(3)
    return(url_details)

def calculate_new_position(coord, distance, direction):
    # Convert latitude to radians
    lat_radians = math.radians(coord[0])
    # Calculate the length of one degree of latitude in meters
    lat_degree_length = (40008000 / 360)

    # Calculate the equivalence in degrees
    lat_equivalence_degrees = distance / lat_degree_length

    # Calculate the length of one degree of longitude in meters
    lon_degree_length = (40075160 * math.cos(lat_radians)) / 360

    # Calculate the equivalence in degrees for longitude
    lon_equivalence_degrees = distance / lon_degree_length
    vector = np.array([0,0])
    # Adjust the position based on the direction
    if "north" in direction.lower():
        vector = vector+np.array([lat_equivalence_degrees,0])
    elif "south" in direction.lower():
        vector = vector-np.array([lat_equivalence_degrees,0])
    if "east" in direction.lower():
        vector = vector + np.array([0,lon_equivalence_degrees])
    elif "west" in direction.lower():
        vector = vector-np.array([0,lon_equivalence_degrees])
    new_position = list(coord+vector)
    return(new_position)

def generate_location_url(start_point,end_point):
    prefix = r'https://www.portalinmobiliario.com/venta/departamento/_item*location_'
    lat = 'lat:'+str(start_point[0])+'*'+str(end_point[0])
    lon = 'lon'+str(start_point[1])+'*'+str(end_point[1])
    return(prefix+lat+','+lon)

def get_uf_currente_value():
    url = r'https://www.uf-hoy.com/'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    uf_value_str= soup.find('div', {'id': 'valor_uf'}).text.strip()
    uf_value_flt = float(uf_value_str.replace('.', '').replace(',','.'))
    return(uf_value_flt)