import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(
    filename='web_scraper_log.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


def start_driver(url):
    logging.info("Requesting URL: %s", url)
    driver = webdriver.Chrome()
    driver.get(url)

    return driver


def get_product_info(driver, main_url, last_page):
    prod_info = []
    
    # added for testing purposes
    last_page = 3
    for page in range(1, last_page+1):
        url = main_url + f'?page={page}'
        logging.info('Currently running page: %s',page)
        driver = start_driver(url)
        logging.info("Waiting for listing-card-wrapper element to show")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'listing-card-wrapper'))
            )
        product_wrapper = driver.find_elements(by=By.ID, value='listing-card-wrapper')
        products = product_wrapper[0].find_elements(by=By.TAG_NAME, value='a')
        product_list = []
        for prod in products:
            if prod.find_element(by=By.XPATH, value='.//*').tag_name == 'div':
                product_list.append(prod)
        
        prod_class_names = {
            'num_of_pic':'sc-kUdmhA.IibdL.mui-style-v1rqhp',
            'price':'sc-jdkBTo.sc-kpKSZj.kTOKgo.hlPXGZ',
            'brand':'sc-jdkBTo.sc-gtJxfw.kTOKgo.jJwkYg.heading-text-1',
            'model':'sc-jdkBTo.sc-gtJxfw.kTOKgo.jJwkYg.heading-text-2',
            'title':'sc-cspYLC.fSIcIP',
            'year':'sc-dQEtJz.iIgTYO',
            'km':'sc-dQEtJz.iIgTYO',
            'steering_side':'sc-dQEtJz.iIgTYO',
            'region_specs':'sc-dQEtJz.iIgTYO'
            'location':'sc-edKZPI.gnLJci',
            'tags':'mui-style-hwdwqa'
        }
        
        ad_dict = {
            'id':None,
            'link':None,
            'num_of_pic':None,
            'price':None,
            'brand':None,
            'model':None,
            'title':None,
            'year':None,
            'km':None,
            'steering_side':None,
            'region_specs':None,
            'location':None,
            'tag':None
        }

        for product in product_list:
            ad_dict['id'] = product.get_attribute('href').split('---')[1]
            ad_dict['link'] = product.get_attribute('href')
            for key, val in prod_class_names.items():
                if key=='year':
                    try:
                        ad_dict[key] = product.find_elements(by=By.CLASS_NAME, value=val)[0].text
                    except:
                        logging.error(f'Error retreiving information for {key} link to car: %s', ad_dict['link'])
                elif key=='km':
                    try:
                        ad_dict[key] = product.find_elements(by=By.CLASS_NAME, value=val)[1].text
                    except:
                        logging.error(f'Error retreiving information for {key} link to car: %s', ad_dict['link'])
                elif key=='steering_side':
                    try:
                        ad_dict[key] = product.find_elements(by=By.CLASS_NAME, value=val)[2].text
                    except:
                        logging.error(f'Error retreiving information for {key} link to car: %s', ad_dict['link'])
                elif key=='region_specs':
                    try:
                        ad_dict[key] = product.find_elements(by=By.CLASS_NAME, value=val)[3].text
                    except:
                        logging.error(f'Error retreiving information for {key} link to car: %s', ad_dict['link'])
                else:
                    try:
                        ad_dict[key] = product.find_element(by=By.CLASS_NAME, value=val).text
                    except:
                        logging.error(f'Error retreiving information for {key} link to car: %s', ad_dict['link'])
            prod_info.append(ad_dict)
    driver.quit()
    return prod_info

url = 'https://uae.dubizzle.com/motors/used-cars/toyota/'
driver = start_driver(url)
last_page = driver.find_elements(by=By.CLASS_NAME, value='sc-lizKOf.bzkMkX.edge_button')[0]
last_page = int(last_page.get_attribute('href').split('page=')[1])
logging.info('The last Page is: %s', str(last_page))
logging.info('Retrieving product information')
prod_info = get_product_info(driver, url, last_page)
cars_df = pd.DataFrame(prod_info)
