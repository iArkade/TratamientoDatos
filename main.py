from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from mongo import MongoConnection

db_client = MongoConnection().client
db = db_client.get_database('MercadoLibre')
col = db.get_collection('laptops')


opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
driver = webdriver.Edge(service = Service(EdgeChromiumDriverManager().install()), options=opts)

driver.get('https://listado.mercadolibre.com.ec/laptops-gamer')


PAGINACION_MAX = 2
PAGINACION_ACTUAL = 1

sleep(3) 

try: 
    disclaimer = driver.find_element(By.XPATH, '//button[@data-testid="action:understood-button"]')
    disclaimer.click() 
except Exception as e:
    print (e) 
    None

while PAGINACION_MAX > PAGINACION_ACTUAL:

    links_productos = driver.find_elements(By.XPATH, '//a[@class="ui-search-item__group__element shops__items-group-details ui-search-link"]')
    links_de_la_pagina = []
    for a_link in links_productos:
        links_de_la_pagina.append(a_link.get_attribute("href"))

    for link in links_de_la_pagina:
        sleep(2)
        try:
            driver.get(link)
            titulo = driver.find_element(By.XPATH, '//h1').text
            precio = driver.find_element(By.XPATH, '//span[contains(@class,"ui-pdp-price")]').text
            descripcion = driver.find_element(By.XPATH, '//p[contains(@class,"ui-pdp-description")]').text
            
            precio = precio.replace('\n', '').replace('\t', '').split("U$S")

            document = {
                "titulo": titulo,
                "precio": precio[1].strip(),
                "descripcion": descripcion
            }

            col.insert_one(document=document)
            
            print (titulo)
            print (precio[1].strip())
            #print (descripcion)
            print("="*50)

            driver.back()
        except Exception as e:
            print (e)
            driver.back()

    try:
        puedo_seguir_horizontal = driver.find_element(By.XPATH, '//span[text()="Siguiente"]')
        puedo_seguir_horizontal.click()
    except: 
        break

    PAGINACION_ACTUAL += 1