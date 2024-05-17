'''
Program: Web Scraping 
Author: Olivia Hinson
Date: 5/13/2024
'''
'''
Program that scrapes data on a website for used cars, 
filters search results, and iterate through web pages 
'''

# Import library packages
from selenium import webdriver # Create driver to help scrape websites 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import pandas as pd 
import warnings
import time
import os

def start_driver(): 
    # Define the website to scrape (Dubizzle used cars)
    website = os.environ.get('WEBSITE')
    # Define path where we downloaded Chrome driver
    path = os.environ.get('CHROME_DRIVER')
        
    # Set available options (if applicable)
    options = webdriver.ChromeOptions()
    options.headless = True
    warnings.filterwarnings('ignore')
        
    # Initializing Google Chrome webdriver from local host as driver 
    cService = webdriver.ChromeService(executable_path=path)
    driver = webdriver.Chrome(options=options, service=cService)
    driver.get(website)
    time.sleep(5)
    
    return driver

def brands_filter(brand, dropdown_list, driver): 
    # Select elements from dropdown by inputting text and clicking 
    dropdown = dropdown_list
    # Almost guaranteed method for clicking the button without issue
    driver.execute_script("arguments[0].click()", dropdown)
    dropdown.send_keys(brand)
    select_option =  driver.find_element(By.XPATH, '//*[@id="lpv-list"]/div[2]/div[2]/div/div/div[1]/div[2]/div/div[2]/div/div/ul/li[2]/span')
    time.sleep(3)
    # Almost guaranteed method for clicking the button without issue
    driver.execute_script("arguments[0].click()", select_option)
    # Allow code to wait before executing next line 
    time.sleep(3)

def get_products(ad, ad_id, link, num_images, price, brand, model, year, title, mileage, location, tag): 
    listing_id = ad.find_element(By.XPATH, './/div/a').get_attribute('href').split('---')[1][:-1]
    listing_image = ad.find_elements(By.XPATH, './/div[@class="sc-iLWXdy jOvNOi"]')
    num_of_images = len(listing_image)
    listing_link = ad.find_element(By.XPATH, './/div/a').get_attribute('href')
    listing_price = ad.find_element(By.XPATH, './/div[@data-testid="listing-price"]').text
    car_brand = ad.find_element(By.XPATH, './/div[@data-testid="heading-text-1"]').text
    car_model = ad.find_element(By.XPATH, './/div[@data-testid="heading-text-2"]').text
    listing_title = ad.find_element(By.XPATH, './/h2[@data-testid="subheading-text"]').text
    listing_year = ad.find_element(By.XPATH, './/div[@data-testid="listing-year"]').text
    listing_kms = ad.find_element(By.XPATH, './/div[@data-testid="listing-kms"]').text
    listing_location = ad.find_element(By.XPATH, './/div[@class="sc-edKZPI gnLJci"]').text
    listing_tag = None
    try: 
        listing_tag = ad.find_element(By.XPATH, './/span[@class="  mui-style-v1rqhp"]').text
    except NoSuchElementException: 
        print('Listing Tag: Not found')   
        
    ad_id.append(listing_id)
    link.append(listing_link)
    num_images.append(num_of_images)
    price.append(listing_price)
    brand.append(car_brand)
    model.append(car_model)
    year.append(listing_year)
    title.append(listing_title)
    mileage.append(listing_kms)
    location.append(listing_location)
    tag.append(listing_tag)
    print(listing_price)
    
    return ad_id, link, num_images, price, brand, model, year, title, mileage, location, tag
    
# main
driver = start_driver()

dropdown = driver.find_element(By.NAME, 'category_1')
filter = ['Lexus', 'Audi', 'BMW', 'Mercedes-Benz', 'Volkswagen', 'Chevrolet']

# Create separate lists for each column in table 
ad_id = []
link = []
num_images = []
price = []
brand = []
model = []
title = []
year = []
mileage = []
location = []
tag = []

count = 0
total = 0
t0 = time.time()

# Clear lists
ad_id.clear()
link.clear()
num_images.clear()
price.clear()
brand.clear()
model.clear()
title.clear()
year.clear()
mileage.clear()
location.clear()
tag.clear()

for search in range(len(filter)): 
    brands_filter(filter[search], dropdown, driver)
    # Retrieve number of pages on a given page
    last_page_button = driver.find_elements(by=By.CLASS_NAME, value='sc-lizKOf.bzkMkX.edge_button')[0]
    number_of_pages = int(last_page_button.get_attribute('href').split('page=')[1])
    print('Number of pages: ' + str(number_of_pages))
    time.sleep(3)
    
    # Iterate through pages
    for page_num in range(1, number_of_pages+1): 
        # Extract data from a listing
        listings = driver.find_elements(By.XPATH, '//*[@id="listing-card-wrapper"]/div')
        time.sleep(3)
        if (page_num == 2 and filter[search] == 'Lexus'): 
            cancel_button = driver.find_element(By.XPATH, '//html/body/div[4]/div[3]/div/div[2]/button[1]')
            if (cancel_button.is_displayed()): 
                cancel_button.click()
        if (page_num < number_of_pages): 
            # Locate element with selenium 
            next_page_button = driver.find_element(By.XPATH, '//a[@class="sc-lizKOf bzkMkX next_button"]')
            time.sleep(3)
            # Scroll down to view pages 
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'end' })", next_page_button)
            time.sleep(3)
            
            # Iterate over list
            for ad in listings:
                get_products(ad, ad_id, link, num_images, price, brand, model, year, title, mileage, location, tag)
                count = count + 1
            time.sleep(3) 
            # Almost guaranteed method for clicking the button without issue
            driver.execute_script("arguments[0].click()", next_page_button)
            time.sleep(3)
        else: 
            time.sleep(3)
            # Iterate over list
            for ad in listings:
                get_products(ad, ad_id, link, num_images, price, brand, model, year, title, mileage, location, tag)
                count = count + 1
    print("Count: " + str(count))
    time.sleep(3)
    
    for i in range(len(filter[search])):
        driver.execute_script("arguments[0].click()", dropdown)
        dropdown.send_keys(Keys.BACKSPACE)
    time.sleep(3)
t1 = time.time()
total_time = t0 + t1
total = total + count
print("Total row count: " + str(total))
print("Total time: " + str(total_time))
    
try:
    # Explicitly wait up to 10 seconds while trying to locate elements
    wait = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="sc-edKZPI gnLJci"]')))
finally:
    # Quit using the Google Chorme webdriver when done
    driver.quit()

# Create a Data Frame using Pandas (Dictionaries)
df = pd.DataFrame({'ad_id': ad_id, 'link': link, 'num_images': num_images, 'price': price, 'carBrand': brand, 'carModel': model,
                  'title': title, 'year': year, 'mileage': mileage, 'location': location, 'tag': tag})

# Export data to CSV file 
df.to_csv('cars.csv', index=False)
print(df)















