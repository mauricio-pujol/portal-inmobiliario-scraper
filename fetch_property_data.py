
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
    try:
        div_main_attributes = soup.find('div', class_='ui-pdp--sticky-wrapper ui-pdp--sticky-wrapper-right')
        raw_title = div_main_attributes.find('div', class_='ui-pdp-header__title-container').find('h1', class_='ui-pdp-title').text
        raw_type = div_main_attributes.find('div','ui-pdp-header__subtitle').text
        raw_published = div_main_attributes.find('p', class_=lambda value: value and value.startswith('ui-pdp-color--GRAY ui-pdp-size--XSMALL ui-pdp-family--REGULAR')).text
        raw_price = div_main_attributes.find('div', class_='ui-pdp-price__second-line').text
        try:
            raw_maintenance = div_main_attributes.find('div', class_='ui-pdp-container__row ui-pdp-container__row--maintenance-fee-vis').text
        except:
            raw_maintenance = None
        raw_size = div_main_attributes.find_all('div', class_='ui-pdp-highlighted-specs-res__icon-label')[0].text
        room_tags = soup.find_all('div', class_='ui-pdp-highlighted-specs-res__icon-label')[1:]
        raw_rooms = [room.text for room in room_tags]
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
            'type': raw_type,
            'published': raw_published,
            'price': raw_price,
            'maintenance': raw_maintenance,
            'size': raw_size,
            'rooms': raw_rooms,
            'broker': raw_broker,
            'adress': raw_adress,
            'google_maps_pin': raw_google_maps_pin,
            'secondary_attributes': raw_secondary_attributes,
            'description':raw_description
            }
        raw_property = pd.DataFrame(raw_property,index= [0])
        return(raw_property)
    except:
        pass

x = extract_property_raw_data(r'https://www.portalinmobiliario.com/venta/departamento/_NoIndex_True_item*location_lat:-32.97453380496371*-32.96628891146818,lon:-71.56781844655625*-71.55075959722153')
