import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_url_details(url):
    url_details = dict()
    text_pattern = r'/([^/]+)/([^/]+)/([^/]+)/([^/]+)'
    match = re.search(text_pattern, url)
    url_details['website'] = match.group(1)
    url_details['operation'] = match.group(2)
    url_details['property_type'] = match.group(3)
    return(url_details)

def get_uf_currente_value():
    url = r'https://www.uf-hoy.com/'
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    uf_value_str= soup.find('div', {'id': 'valor_uf'}).text.strip()
    uf_value_flt = float(uf_value_str.replace('.', '').replace(',','.'))
    return(uf_value_flt)