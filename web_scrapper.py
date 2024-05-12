import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging

logging.basicConfig(
    filename='web_scrapper_log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)


def start_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)

    return driver

# url = 'https://uae.dubizzle.com/motors/used-cars/'
page_num = 1
prod_info = []
for page in range(1, 7):
    url = f'https://uae.dubizzle.com/motors/used-cars/toyota/?page={page}'
    driver = start_driver(url)
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
        'location':None,
        'tag':None
    }
    iteration = 1
    for product in product_list:
        iteration=iteration+1
        ad_dict['id'] = product.get_attribute('href').split('---')[1]
        ad_dict['link'] = product.get_attribute('href')
        for key, val in prod_class_names.items():
            if key=='year':
                try:
                    ad_dict[key] = product.find_elements(by=By.CLASS_NAME, value=val)[0].text
                except:
                    logging.error(f'Error retreiving information for {key}')
            elif key=='km':
                try:
                    ad_dict[key] = product.find_elements(by=By.CLASS_NAME, value=val)[1].text
                except:
                    logging.error(f'Error retreiving information for {key}')
            else:
                try:
                    ad_dict[key] = product.find_element(by=By.CLASS_NAME, value=val).text
                except:
                    logging.error(f'Error retreiving information for {key}')
        prod_info.append(ad_dict)
        
cars_df = pd.DataFrame(prod_info)
