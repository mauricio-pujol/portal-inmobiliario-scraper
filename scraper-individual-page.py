
url = r'https://www.portalinmobiliario.com/MLC-1445907571-el-encanto-a-una-cuadra-de-av-borgono-linda-vista-al-mar-_JM#position=24&search_layout=grid&type=item&tracking_id=b2d8e76f-5bb0-488c-a1fe-771f1981fc5a'


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(options = option)
driver.get(url)
driver.refresh()

page_content = driver.page_source

driver.quit()