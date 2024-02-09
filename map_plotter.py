import folium
from IPython.display import display
import numpy as np
import math
from utils import calculate_new_position
# Coordenadas de las esquinas del rectángulo
area_start_coord = np.array([-32.98643, -71.55181])
area_end_coord = np.array([-32.95199, -71.52434])

# Calcular las coordenadas de las otras dos esquinas del rectángulo
area_bottom_left = np.array([area_start_coord[0], area_start_coord[1]]) #ok
area_bottom_right = np.array([area_start_coord[0], area_end_coord[1]]) # ok
area_top_left = np.array([area_end_coord[0], area_start_coord[1]])
area_top_right = np.array([area_end_coord[0], area_end_coord[1]]) #ok
# Calcular el centro del rectángulo
lat_center = (area_start_coord[0] + area_end_coord[0]) / 2
lon_center = (area_start_coord[1] + area_end_coord[1]) / 2

# Crear un mapa centrado en el centro del rectángulo
mapa = folium.Map(location=[lat_center, lon_center], zoom_start=13)

# Agregar el rectángulo al mapa
search_area = folium.Polygon(
    locations=[area_bottom_left, area_bottom_right, area_top_right, area_top_left],
    color='#3498db',  # Bordes en color naranja
    fill=True,
    fill_color='#3498db',  # Relleno en color azul claro
    fill_opacity=0.4
)

# Añadir el rectángulo al mapa
search_area.add_to(mapa)


#796x460
cell_bottom_left= area_bottom_left
cell_top_left = calculate_new_position(cell_bottom_left,460,'north')
cell_top_right= calculate_new_position(cell_bottom_left,700,'east')
cell_bottom_right = calculate_new_position(cell_bottom_left,460,'south')
cell_area = folium.Polygon(
    locations=[cell_bottom_left, cell_top_left, cell_top_right,cell_bottom_right,cell_bottom_left],
    color='red',  # Bordes en color naranja
    fill=True,
    fill_color='#3498db',  # Relleno en color azul claro
    fill_opacity=0.4
)

cell_area.add_to(mapa)



# Mostrar el mapa en la consola
display(mapa)

