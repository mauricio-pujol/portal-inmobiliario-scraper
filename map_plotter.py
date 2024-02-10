import folium
from IPython.display import display
import numpy as np
import math
from utils import calculate_new_position

def generate_search_grid_points(search_area_start_coord,search_area_end_coord):
    # Calcular las coordenadas de las otras dos esquinas del rectángulo
    area_bottom_left = list([search_area_start_coord[0], search_area_start_coord[1]])
    area_bottom_right = list([search_area_start_coord[0], search_area_end_coord[1]]) 
    area_top_left = list([search_area_end_coord[0], search_area_start_coord[1]])
    area_top_right = list([search_area_end_coord[0], search_area_end_coord[1]]) 

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
    while draw_grid: # El área de busqueda de cada celda es 796mx460m.  219.63xo 365.5
        cell_top_left = calculate_new_position(cell_bottom_left,219.63,'north')
        cell_top_right = calculate_new_position(calculate_new_position(cell_bottom_left,219.63,'north'),365.5,'east')
        cell_bottom_right= calculate_new_position(cell_bottom_left,365.5,'east')
        grid_points.append([cell_bottom_left, cell_top_left, cell_top_right,cell_bottom_right,cell_bottom_left])
        cell_area = folium.Polygon(
            locations=[cell_bottom_left, cell_top_left, cell_top_right,cell_bottom_right,cell_bottom_left],
            color='navy',  # Bordes en color naranja
            fill=True,
            fill_color='#3498db',  # Relleno en color azul claro
            fill_opacity=0.2
        )
        cell_bottom_left = calculate_new_position(cell_bottom_left,300,'east')
        if cell_bottom_right[1] >area_bottom_right[1]:#Si se sale del recuadro horizontalmente
            cell_bottom_left = calculate_new_position(area_bottom_left,180*j,'north')
            j+=1
        if cell_top_right[0] > area_top_right[0] and cell_top_right[1] > area_top_right[1]: #Si se sale del recuadro horizontal y verticalmente
            draw_grid = False
        cell_area.add_to(mapa)

    ajuste_lat = -(grid_points[-1][2][0]-area_top_right[0])/2
    ajuste_lon = -(grid_points[-1][2][1]-area_top_right[1])/2


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
    print('Mostrando mapa generado con',len(grid_points),'celdas. En color celeste es el área de búsqueda original y en azul las celdas en que se busca individualmente.')
    display(new_map)
    return(grid_points)

#search_area_start_point= list([-32.98643, -71.55181])
#search_area_end_point = list([-32.95199, -71.52434])
#generate_search_grid_points(search_area_start_point,search_area_end_point)