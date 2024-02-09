
#url = r'https://www.portalinmobiliario.com/MLC-1445907571-el-encanto-a-una-cuadra-de-av-borgono-linda-vista-al-mar-_JM#position=24&search_layout=grid&type=item&tracking_id=b2d8e76f-5bb0-488c-a1fe-771f1981fc5a'
url = r'https://www.portalinmobiliario.com/MLC-1461323009-departamento-edificio-las-terrazas-vina-del-mar-_JM#reco_item_pos=2&reco_backend=triggered_realestate_recommendations&reco_backend_type=function&reco_client=classi-realestate-vip&reco_id=f08aab98-86bc-435d-98eb-acbb87579e67&referred_item_status=closed'

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


def extract_property_raw_data(url):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    driver = webdriver.Chrome(options = option)
    driver.get(url)
    driver.refresh()
    page_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page_content, "html.parser")

    ## property main attributes
    div_main_attributes = soup.find('div', class_='ui-pdp--sticky-wrapper ui-pdp--sticky-wrapper-right')
    raw_title = div_main_attributes.find('div', class_='ui-pdp-header__title-container').find('h1', class_='ui-pdp-title').text
    raw_published = div_main_attributes.find('p', class_=lambda value: value and value.startswith('ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR')).text
    raw_price = div_main_attributes.find('div', class_='ui-pdp-price__second-line').text
    try:
        raw_maintenance = div_main_attributes.find('div', class_='ui-pdp-container__row ui-pdp-container__row--maintenance-fee-vis').text
    except:
        raw_maintenance = None
    raw_size = div_main_attributes.find_all('div', class_='ui-pdp-highlighted-specs-res__icon-label')[0].text
    raw_bedrooms = div_main_attributes.find_all('div', class_='ui-pdp-highlighted-specs-res__icon-label')[1].text
    raw_bathrooms = div_main_attributes.find_all('div', class_='ui-pdp-highlighted-specs-res__icon-label')[1].text
    raw_broker = div_main_attributes.find('div', class_='ui-vip-profile-info__info-link').text

    #property location attributes
    div_google_maps = soup.find('div', class_='ui-pdp-container__col col-1 ui-vip-core-container--content-left')
    raw_adress = div_google_maps.find('div', class_='ui-pdp-media__body').find('p', class_='ui-pdp-color--BLACK ui-pdp-size--SMALL ui-pdp-family--REGULAR ui-pdp-media__title').text
    raw_google_maps_pin = div_google_maps.find('div', class_='ui-vip-location__map').find('img')['src']

    #property secondary attributes
    div_secondary_attributes = soup.find_all('div', class_='ui-pdp-container__row ui-vpp-highlighted-specs__attribute-columns__row')
    raw_secondary_attributes = ','.join([elemento.text for elemento in div_secondary_attributes])


    #property text description
    raw_description =soup.find('div', class_='ui-pdp-container__row ui-pdp-container__row--description').find('p').text

    raw_property= {
        'url':url,
        'title': raw_title,
        'published': raw_published,
        'price': raw_price,
        'maintenance': raw_maintenance,
        'size': raw_size,
        'bedrooms': raw_bedrooms,
        'bathrooms': raw_bathrooms,
        'broker': raw_broker,
        'adress': raw_adress,
        'google_maps_pin': raw_google_maps_pin,
        'secondary_attributes': raw_secondary_attributes,
        'description':raw_description
    }
    raw_property = pd.DataFrame(raw_property,index= [0])
    return(raw_property)



test_urls = ['https://www.portalinmobiliario.com/MLC-2023071526-oportunidad-buen-sector-buenas-vista-buen-precio-_JM#position=28&search_layout=grid&type=item&tracking_id=48e8c660-d741-424f-a148-e234c5a85f4d',
 'https://www.portalinmobiliario.com/MLC-2124650310-vendo-departamento-en-bosques-de-montemar-_JM#position=1&search_layout=grid&type=item&tracking_id=988431c5-978d-47a6-bb40-8ccc050873ad',
 'https://www.portalinmobiliario.com/MLC-1405646873-departamento-en-renaca-_JM#position=12&search_layout=grid&type=item&tracking_id=a991a596-9b96-470a-afe4-313171ac5c24',
 'https://www.portalinmobiliario.com/MLC-2204033410-depto-espectacular-vista-playa-renaca-5d-4b-183-m2-_JM#position=10&search_layout=grid&type=item&tracking_id=7b51daf3-178b-42b5-959d-91a308b4ecaa',
 'https://www.portalinmobiliario.com/MLC-1452817895-departamento-en-venta-jardin-del-mar-renaca-vina-del-mar-_JM#position=22&search_layout=grid&type=item&tracking_id=9b83ece4-dc16-4e88-9e39-95e832f1dd32',
 'https://www.portalinmobiliario.com/MLC-1397909323-departamento-en-venta-de-3-dorm-en-la-foresta-_JM#position=41&search_layout=grid&type=item&tracking_id=cb82bc73-406e-43d0-a163-0f0e05a1f5ac',
 'https://www.portalinmobiliario.com/MLC-2157463444-departamento-jardin-del-mar-_JM#position=30&search_layout=grid&type=item&tracking_id=77ec9689-e920-43dd-b97a-3f8d503802f4',
 'https://www.portalinmobiliario.com/MLC-2063139864-lindo-depto-a-pasos-de-la-playa-renaca-_JM#position=14&search_layout=grid&type=item&tracking_id=2fe25723-1453-44d9-b5b7-e9a496f41567',
 'https://www.portalinmobiliario.com/MLC-2109774746-excelente-ubicacion-lindo-departamento-_JM#position=41&search_layout=grid&type=item&tracking_id=48e8c660-d741-424f-a148-e234c5a85f4d',
 'https://www.portalinmobiliario.com/MLC-2109782572-excelente-departamento-con-arquitectura-de-vanguar-_JM#position=4&search_layout=grid&type=item&tracking_id=81724b72-7759-417c-baeb-3db970340462',
 'https://www.portalinmobiliario.com/MLC-1421974243-renaca-vista-al-mar-5d5b-terrazas-3-estacionamientos-_JM#position=2&search_layout=grid&type=item&tracking_id=7b51daf3-178b-42b5-959d-91a308b4ecaa',
 'https://www.portalinmobiliario.com/MLC-1435000179-departamento-en-renaca-_JM#position=19&search_layout=grid&type=item&tracking_id=7b51daf3-178b-42b5-959d-91a308b4ecaa',
 'https://www.portalinmobiliario.com/MLC-1978073204-se-vende-departamento-con-primera-vista-al-mar-en-edmundo-e-_JM#position=39&search_layout=grid&type=item&tracking_id=651bb303-db09-45bb-8444-b67c568da65e',
 'https://www.portalinmobiliario.com/MLC-2019265458-penthouse-en-venta-vina-del-mar-_JM#position=44&search_layout=grid&type=item&tracking_id=29346192-a712-4ef6-b076-fd85e76bb0c5',
 'https://www.portalinmobiliario.com/MLC-1986127076-departamento-de-3-dormitorios-en-jardin-del-mar-_JM#position=38&search_layout=grid&type=item&tracking_id=fde6aad8-a61f-4adb-b323-374bdbb34ec0',
 'https://www.portalinmobiliario.com/MLC-2079088812-depto-exclusivo-excelente-ubicacion-c211014-_JM#position=42&search_layout=grid&type=item&tracking_id=81724b72-7759-417c-baeb-3db970340462',
 'https://www.portalinmobiliario.com/MLC-2154794822-broker-jardin-del-mar-2d-2b-1e-1bod-_JM#position=30&search_layout=grid&type=item&tracking_id=0fc512a3-6e8c-4796-9593-e48e59592095',
 'https://www.portalinmobiliario.com/MLC-1436863431-edmundo-eluchans-1615-_JM#position=34&search_layout=grid&type=item&tracking_id=48e8c660-d741-424f-a148-e234c5a85f4d']



raw_columns = [
    'url', 'title', 'published', 'price', 'maintenance', 'size', 'bedrooms', 'bathrooms',
    'broker', 'adress', 'google_maps_pin', 'secondary_attributes', 'description'
]

# Inicializar un DataFrame vacío con las columnas
raw_properties_df = pd.DataFrame(columns=raw_columns)

i = 1
for e in test_urls:
    print('Propiedad numero:',i,e)
    raw_properties_df = raw_properties_df.append(extract_property_raw_data(e))
    i+=1

raw_properties_df