import folium
from IPython.display import display
import numpy as np
import math
from utils import calculate_new_position
# Coordenadas de las esquinas del rectángulo
search_area_start_coord = list([-32.98643, -71.55181])
search_area_end_coord = list([-32.95199, -71.52434])

# Calcular las coordenadas de las otras dos esquinas del rectángulo
area_bottom_left = list([search_area_start_coord[0], search_area_start_coord[1]]) #ok
area_bottom_right = list([search_area_start_coord[0], search_area_end_coord[1]]) # ok
area_top_left = list([search_area_end_coord[0], search_area_start_coord[1]])
area_top_right = list([search_area_end_coord[0], search_area_end_coord[1]]) #ok
# Calcular el centro del rectángulo
lat_center = (search_area_start_coord[0] + search_area_end_coord[0]) / 2
lon_center = (search_area_start_coord[1] + search_area_end_coord[1]) / 2

# Crear un mapa centrado en el centro del rectángulo
mapa = folium.Map(location=[lat_center, lon_center], zoom_start=13)

# Agregar el rectángulo al mapa
search_area = folium.Polygon(
    locations=[area_bottom_left, area_bottom_right, area_top_right, area_top_left],
    color='#3498db',  # Bordes en color naranja
    fill=True,
    fill_color='#3498db',  # Relleno en color azul claro
    fill_opacity=0.1
)

# Añadir el rectángulo al mapa
search_area.add_to(mapa)
grid_points = []
cell_bottom_left= area_bottom_left
j= 1
draw_grid = True
while draw_grid:
    #796x460
    cell_top_left = calculate_new_position(cell_bottom_left,460,'north')
    cell_top_right = calculate_new_position(calculate_new_position(cell_bottom_left,460,'north'),796,'east')
    cell_bottom_right= calculate_new_position(cell_bottom_left,796,'east')
    grid_points.append([cell_bottom_left, cell_top_left, cell_top_right,cell_bottom_right,cell_bottom_left])
    cell_area = folium.Polygon(
        locations=[cell_bottom_left, cell_top_left, cell_top_right,cell_bottom_right,cell_bottom_left],
        color='navy',  # Bordes en color naranja
        fill=True,
        fill_color='#3498db',  # Relleno en color azul claro
        fill_opacity=0.2
    )
    cell_bottom_left = calculate_new_position(cell_bottom_left,700,'east')
    if cell_bottom_right[1] >area_bottom_right[1]:#Si se sale del recuadro horizontalmente
         cell_bottom_left = calculate_new_position(area_bottom_left,400*j,'north')
         j+=1
    if cell_top_right[0] > area_top_right[0] and cell_top_right[1] > area_top_right[1]:
         draw_grid = False
    cell_area.add_to(mapa)

ajuste_lat = -(grid_points[-1][2][0]-area_top_right[0])/2
ajuste_lon = -(grid_points[-1][2][1]-area_top_right[1])/2

# Mostrar el mapa en la consola
display(mapa)


new_map = folium.Map(location=[lat_center, lon_center], zoom_start=13)
for cell in grid_points:
     cell = np.array(cell) 
     cell[:, 0] += ajuste_lat
     cell[:, 1] += ajuste_lon
     cell[0] = cell[-1]
     cell_area = folium.Polygon(
        locations=[cell],
        color='navy',  # Bordes en color naranja
        fill=True,
        fill_color='#3498db',  # Relleno en color azul claro
        fill_opacity=0.2
    )
     cell_area.add_to(new_map)


search_area = folium.Polygon(
    locations=[area_bottom_left, area_bottom_right, area_top_right, area_top_left],
    color='#3498db',  # Bordes en color naranja
    fill=True,
    fill_color='#3498db',  # Relleno en color azul claro
    fill_opacity=0.1
)

# Añadir el rectángulo al mapa
search_area.add_to(new_map)


display(new_map)


