from django.shortcuts import render
from selenium.webdriver.chrome.options import Options
import re
import csv
import time
import random
import selenium
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
# Create your views here.

from django.http import HttpResponse
from django.conf import settings

from urllib.parse import urlencode, quote_plus
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse, parse_qs, urlencode,urlunparse,unquote,urljoin


def main(csvreader):
    print("HELLO",csvreader)
    chrome_options = uc.ChromeOptions()
    
    # chrome_options.add_argument('--proxy-server=%s' % PROXY)
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # Exclude the collection of enable-automation switches 
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--headless') 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),  options=chrome_options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.execute_script('''window.open("https://www.fashionphile.com/");''')
    window_handles = driver.window_handles

    # Loop through each handle and switch to the window, then print the URL
    for handle in window_handles:
        driver.switch_to.window(handle)
        print(driver.current_url)
    print('Handles Lenght', len(driver.window_handles))
    new_window = driver.window_handles[1]
    print('Fashion',driver.current_url)
    driver.switch_to.window(new_window)
    wait = WebDriverWait(driver, 30)
    products_list = []
    
    try:
        time.sleep(10)
        # --- If site doesn't gets open then open new tab
        print('--->> Site Not Open 1')
        driver.find_element(By.XPATH,'//h1[text()="Establishing a Secure Connection"]')
        print('--->> Site Not Open 2')
        driver.execute_script('''window.open("https://www.fashionphile.com/");''')
        print('--->> Site Not Open 3')
        time.sleep(5)
        print('WIndow Open')
        driver.refresh()
        
    except Exception as s_e:
        print('WIndow Open error', s_e)
        pass

    for row in csvreader:
        desc = row[0]
        print("hello1",desc)
        print('Product --->>',row[0])
        desc = row[0]
        time.sleep(20)
        print("hello1")
        search_bar = driver.find_element(By.XPATH,'/html/body/div[1]/header/div/div[2]/div[3]/div/div/div/div/div/div/div/input')
        print("hello0",desc)
        search_bar.send_keys(desc)
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="__next"]/header/div/div[2]/div[2]/div/div[2]/div/div/div/div/span[2]/button').click()
        time.sleep(1)
        try:
            #  ----- Join Now Popup
            driver.find_element(By.XPATH,'//*[@id="__next"]/div[4]/div[2]/div[1]/div[2]').click()
        except:
            pass
        time.sleep(3)
        try:
            driver.find_element(By.XPATH,'/html/body/div[18]/div[2]/div').click()
        except:
            pass
        time.sleep(3)
        try:
            driver.find_element(By.XPATH,'//*[@id="__next"]/div[4]/div[2]/div[1]/div[2]/div').click()
        except:
            pass
        time.sleep(3)
        try:
            driver.find_element(By.XPATH,'/html/body/div[13]/div[2]/div').click()
        except:
            pass
        time.sleep(2)
        try:
            print('Try --------->>>>')
            WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH,'//h5[text()="No results were found for"]'))) 
            el = driver.find_element(By.XPATH,'//h5[text()="No results were found for"]')
            # Removing last word from description
            words = desc.rsplit(" ", 1)
            # Rejoin the words without the last one
            desc = words[0]
            print('Description --->>> ', desc)
        except Exception as e:
            print('Except--------->>>>')
            # Fetching all Products
            products = driver.find_elements(By.CLASS_NAME,'product')
            for product in products:
                price = product.find_element(By.CSS_SELECTOR,'[itemprop="price"]').text
                title_ = product.find_element(By.CLASS_NAME,'productTitle')
                title = title_.find_element(By.TAG_NAME,'a').text
                print(title, price)
                temp = {'title': title, 'price': price}
                products_list.append(temp)
            break

    driver.quit()
    # Creating CSV of products title and prices
    random_number = random.randint(1, 10000)
    keys = products_list[0].keys()
    file_path = f'static/products{random_number}.csv'
    with open(file_path, 'w', newline='',errors="ignore") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(products_list)
    return file_path


def home(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr = []
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }

        json_data = {
            'query': {
                'filter': '{"paymentStatus":"PAID"}',
                'sort': '{"number": "desc"}',
                'paging': {
                    'limit': '50',
                },
            },
        }

        # GETTING All PRODUCTS
        response = requests.post('https://www.wixapis.com/stores/v1/products/query', headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Handle the retrieved products data
            for product in data['products']:
                print('Product --->>', product['name'])
                description_arr.append(product['name'])
            file_path = ''
            while 1:
                try:
                    print('function calling')
                    file_path = main(description_arr) 
                    break
                except Exception as e:
                    print('<------ Access Denied ------>',e)
                    time.sleep(10)

            return render(request, 'fashionphile.html', context={'csv_file': file_path})
        else:
            # Handle the error
            print(f"Error: {response.status_code} - {response.text}") 
    
    return render(request, 'fashionphile.html')








def search_madison(search_query, driver):
    search_query = search_query.replace(',',' ')
    print('--- Search Function ---', search_query)
    driver.get("https://www.madisonavenuecouture.com/")
    #search
    time.sleep(2)    
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/header/div[3]/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div[1]/form/input[2]')))
    input_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/header/div[3]/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div[1]/form/input[2]')
    input_element.send_keys(Keys.CONTROL + "a")  # Select all text
    input_element.send_keys(Keys.DELETE)         # Delete selected text
    # input_element.clear()
    time.sleep(5)
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/header/div[3]/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div[1]/form/input[2]')))
    input_element.send_keys(search_query)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/header/div[3]/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div[1]/form/button').click()

def close_modal_dialog(driver):
    
    try:
        # Wait for the pop-up to appear
        popup_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "internationalization-modal")))

        # Close the pop-up
        close_button = popup_element.find_element(By.CLASS_NAME, "close")
        close_button.click()
    except Exception as e:
        print('Exception occurred:', str(e))

    try:
        # Wait for the pop-up to appear
        popup_element_big = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div[2]/div/div")))

        # Close the pop-up
        close_button = popup_element_big.find_element(By.CLASS_NAME, "rbg-popup-generic__close-icon")
        close_button.click()
    except Exception as e:
        print('Exception occurred:', str(e))

def search_rebag(search_queries, driver):
    for search_query in search_queries:
        print("hello",search_queries)
        # Convert the search_query list to a single string
        search_query_str = ','.join(search_query)
        search_query_str = search_query_str.replace(',',' ')

        print('--- Search Function ---', search_query)

        driver.get("https://shop.rebag.com/search?")
        #search
        time.sleep(10)
        body_element = driver.find_element(By.TAG_NAME, 'body')
        body_element.click()
        time.sleep(5)
        close_modal_dialog(driver)
        # time.sleep(10) 
        try:   
            time.sleep(10)
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div/div[2]/div/div/div[1]/div/form/div/input')))
            try:
                input_element = driver.find_element(By.XPATH, '/html/body/div[2]/header/div/div/div[2]/div/div/div[1]/div/form/div/input')
            except:
                input_element = driver.find_element(By.XPATH, '/html/body/div[2]/header/div/div/div[2]/div/div/div[1]/div/form/div/input')

            input_element.send_keys(Keys.CONTROL + "a")  # Select all text
            input_element.send_keys(Keys.DELETE)         # Delete selected text

            # input_element.clear()
            # time.sleep(5)
            # WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/header[2]/div/div/div[2]/div/div/div[1]/div/form/div/input')))
            input_element.send_keys(search_query, Keys.RETURN)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'plp__products-grid-container')))
            print('Search Done for Rebag')
            break
        except Exception as e:
            print('<------ Access Denied ------>',e)


def search_firstdibs(search_query, driver):
    print('--- Search Function ---', search_query)
    driver.get("https://1stdibs.com")
    #search
    time.sleep(5) 
    while 1:
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/div[1]/div/form/div/div/div/div/div[1]/div/input')))
            input_element = driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/div[1]/div/form/div/div/div/div/div[1]/div/input')
            input_element.clear()
            WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/div[1]/div/form/div/div/div/div/div[1]/div/input')))
            input_element.send_keys(search_query)
            driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/div[1]/div/form/div/div/div/div/div[2]/div[2]/button').click()
            break
        except Exception as e:
            print('<------ Access Denied in search 1sdibs ------>',e)

def get_results(driver):
    try:
        items_grid = driver.find_element(By.XPATH,'/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul')
        items_list = items_grid.find_elements(By.CLASS_NAME,'s-item__wrapper')
        print(len(items_list))
    except:
        print("No result found")
        items_list = []
    return items_list

def fetch_details(item):
    print('------ Fetch Details Function -------')
    
    temp_item_list = []
    try:
        item_title = item.find_element(By.CLASS_NAME,'s-item__title').text
        temp_item_list.append(re.sub(r'[^\w\s]', '', item_title))
        item_price = item.find_element(By.CLASS_NAME,'s-item__price').text
        temp_item_list.append(item_price)
        try:
            item_price_before_discount = item.find_element(By.CLASS_NAME,'s-item__additional-price').text
            item_price_before_discount = item_price_before_discount.replace('Was: ','')
            item_price_before_discount = item_price_before_discount.replace('List price: ','')
            temp_item_list.append(item_price_before_discount)
        except:
            item_price_before_discount = 0
            temp_item_list.append(item_price_before_discount)
        try:    
            item_condition = item.find_element(By.CLASS_NAME,'SECONDARY_INFO').text
        except:
            item_condition = ''
        temp_item_list.append(item_condition)
    except:
        print('Error in fetch details')
    return temp_item_list

def scrap_items(scraped_list, driver):
    items_list = get_results(driver)
    for item in items_list:
        scraped_list.append(fetch_details(item))


def chk_pagination(driver):
    try:
        pagination_div = driver.find_element(By.CLASS_NAME,'pagination')
        try:
            pagination_btn = pagination_div.find_element(By.CLASS_NAME,'pagination__next')
            if pagination_btn.tag_name == "button":
                print("We don't have new page we have butoon")
                return False
            else:
                pagination_btn.click()
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul')))
                time.sleep(2)
                print("We have new page")
                return True
        except Exception as e:
            print("We don't have new page: ",e)
            return False
    except:
        print("No pagination")
        return False




def save_to_csv_firstdibs(scraped_list):
    # Open CSV file for writing
    api_url = 'https://www.wixapis.com/stores/v1/products'
    api_token = 'YOUR_WIX_API_TOKEN'
    print("gere")
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }
    print("game`")
    print(scraped_list)
    print(scraped_list[0])
    print(scraped_list[1][1])

    price1 = price_str_to_int(scraped_list[1][1])
    price2 = price_str_to_int(scraped_list[2][1])
    price3 = price_str_to_int(scraped_list[3][1])

    json_data = {
        'product': {
            'name': scraped_list[1][0],
            'productType': 'physical',
            'priceData': {
                'price': price1,
            },
            'condition': scraped_list[1][2],
            # Add other fields as needed for the Wix API
        }
    }

    response = requests.post(api_url, headers=headers, json=json_data)
    print(response)

def save_to_csv_madison(scraped_list):

    api_url = 'https://www.wixapis.com/stores/v1/products'
    api_token = 'YOUR_WIX_API_TOKEN'
    print("gere")
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }
    print("game`")
    print(scraped_list)
    print(scraped_list[0])
    print(scraped_list[1][1])

    price1 = price_str_to_int(scraped_list[1][1])
    price2 = price_str_to_int(scraped_list[2][1])
    price3 = price_str_to_int(scraped_list[3][1])

    json_data = {
        'product': {
            'name': scraped_list[1][0],
            'productType': 'physical',
            'priceData': {
                'price': price1,
            },
            'condition': scraped_list[1][2],
            # Add other fields as needed for the Wix API
        }
    }

    response = requests.post(api_url, headers=headers, json=json_data)
    print(response)

import re

def price_str_to_int(price_str):
    # Check if the price string is None
    if price_str is None:
        return 0  # Or any other default value you want to use

    # Remove commas from the price string
    price_str = re.sub(r'[^\d.]', '', price_str)
    
    # Check if the price string is empty after removing commas
    if not price_str:
        return 0  # Or any other default value you want to use

    # Convert the price to an integer
    return int(float(price_str))


def save_to_csv_rebag(scraped_list,image_element1,image_element2,image_element3):
    api_url = 'https://www.wixapis.com/stores/v1/products'
    api_token = 'YOUR_WIX_API_TOKEN'
    print("gere")

    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }
    print("game`")
    print(scraped_list)
    print(scraped_list[0])
    print(scraped_list[1][1])

    price1 = price_str_to_int(scraped_list[1][1])
    price2 = price_str_to_int(scraped_list[2][1])
    price3 = price_str_to_int(scraped_list[3][1])

    image1 = image_element1.get_attribute('src')
    image2 = image_element2.get_attribute('src')
    image3 = image_element3.get_attribute('src')

    # Adding the image URL to the existing JSON data structure
    json_data = {
    'product': {
        'name': scraped_list[1][0],
        'productType': 'physical',
        'priceData': {
            'price': price1,
        },
        'condition': scraped_list[1][2],
    },
    }

    json_data1 = {
    'product': {
        'name': scraped_list[2][0],
        'productType': 'physical',
        'priceData': {
            'price': price1,
        },
        'condition': scraped_list[2][2],
    },
    }

    json_data2 = {
    'product': {
        'name': scraped_list[3][0],
        'productType': 'physical',
        'priceData': {
            'price': price1,
        },
        'condition': scraped_list[3][2],
    },
    }

    json_data3 = {
    'product': {
        'name': scraped_list[4][0],
        'productType': 'physical',
        'priceData': {
            'price': price1,
        },
        'condition': scraped_list[4][2],
    },
    }

    response1 = requests.post(api_url, headers=headers, json=json_data)
    response2 = requests.post(api_url, headers=headers, json=json_data1)
    response3 = requests.post(api_url, headers=headers, json=json_data2)
    response4 = requests.post(api_url, headers=headers, json=json_data2)


    print(f'Status code: {response1.status_code}')
    print(f'Status code: {response2.status_code}')
    print(f'Status code: {response3.status_code}')
    print(f'Status code: {response4.status_code}')
    print(f'Response: {response1.json()}')



def close_modal_dialog_firstdibs(driver):
    
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[7]/div/div/button")))
        popup_element=driver.find_element(By.XPATH, "/html/body/div[7]/div/div/button")
        popup_element.click()
    except Exception as e:
        print('Exception occurred ', str(e))


def start_process(reader, driver):
    scraped_list = []
    csv_haeding = ['Discription', 'Current Price', 'Before Discount', 'Condition']
    scraped_list.append(csv_haeding)
    for row in reader:
        print("*********",row,"*********")
        search(row, driver)
        scrap_items(scraped_list , driver)
        while chk_pagination(driver):
            scrap_items(scraped_list , driver)
    file_path = save_to_csv(scraped_list)
    return file_path

def scrapData(scraped_data_list,href,driver,base_url):
    
    driver.switch_to.default_content()
    full_url = urljoin(base_url, href)
    driver.get(full_url)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div/main/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]")))
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    description_element_div = soup.select_one('div[class="col-md-6 product-shop"]')
    description_element=description_element_div.find("h1",class_="product-title herm")
    price_element_div = soup.select_one("div[class='prices']")
    price_element=price_element_div.find("span", class_="money")
    condition_element = price_element_div.find("div", class_="product-condition")

    description = description_element.text.strip() if description_element else None
    price = price_element.text.strip() if price_element else None
    condition = condition_element.text.replace("Condition:", "").strip() if condition_element else None
    data=[]
    data.append(description)
    data.append(price)
    data.append(condition)
    print('---------------------------------------')
    print('Description', description)
    print('price', price)
    print('condition', condition)

    # Append the data to the list
    scraped_data_list.append(data)
    return scraped_data_list
    
def scrapData_firstdibs(scraped_data_list,href,driver,base_url):
    # full_url = urljoin(base_url, href)
    driver.get(href)
    try:
        close_modal_dialog_firstdibs(driver)
    except Exception as e:
        print('<------ Access Denied in scrapp data top ------>',e)

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-tn='pdp-main-title']")))
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tn="pdp-main-title"]')))
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(2)
    description_element = soup.select_one('div[data-tn="pdp-main-title"]')
    price_element = soup.select_one("span[data-tn='price-amount']")
    condition_element = soup.select_one("span[data-tn='pdp-spec-detail-condition']")

    description = description_element.text if description_element else None
    price = price_element.text if price_element else None
    condition = condition_element.text if condition_element else None
    data=[]
    data.append(description)
    data.append(price)
    data.append(condition)
    print('---------------------------------------------')
    print('description', description)
    print('Price', price)
    print('condition', condition)
    # Append the data to the list
    scraped_data_list.append(data)

    return scraped_data_list
    
def start_process_firstdibs(search_queries, driver):
    print(" in 1stdibs process function")
    base_url="https://1stdibs.com"
    scraped_data_list=[]
    csv_haeding = ['Description', 'Price', 'Condition']
    scraped_data_list.append(csv_haeding)
    page_number=1
    next_button_status=True
    search_result_url=""
    
    for query in search_queries:
        search_firstdibs(query, driver)
        time.sleep(5)
        try:
            close_modal_dialog_firstdibs(driver)
        except Exception as e:
            print('<------ Access Denied ins start of query------>',e)
        time.sleep(2)
        searched_url=driver.current_url
        p=1
        # next_button=soup.find('a', {'data-tn': 'page-forward'})
        while next_button_status==True:
            if page_number>1:
                driver.get(next_button)
                searched_url=next_button
                time.sleep(5)
                try:
                    close_modal_dialog_firstdibs(driver)
                except Exception as e:
                    print('<------ Access Denied  ------>',e)
             

            # get relevant div and extract links in href_list
            html=driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            div_elements = soup.find_all('div', {'class': '_95b421a2'})
            #Print the div_element to see its content
            if div_elements:
                    i=1
                    for div_element in div_elements:
                        a_tag = div_element.find('a', {'href': True, 'class': '_9e04a611 _9f85bf45 _f7a3e2b1'})

                        if a_tag:
                            search_result_url = a_tag['href']
                            full_url = urljoin(base_url, search_result_url)
                            scrapData_firstdibs(scraped_data_list,full_url,driver,base_url)
                            
                    save_to_csv_firstdibs(scraped_data_list)
            else:
                print("No div element found ")
                break
            p+=1
            
            page_number+=1
            driver.get(searched_url)
            time.sleep(10)
            try:
                close_modal_dialog_firstdibs(driver)
            except Exception as e:
                print('<------ Access Denied  ------>',e)
                driver.get(searched_url)
             

            # next_button = driver.find_element(By.CSS_SELECTOR,'button.findify-widget--pagination__next')
            next_button=soup.find('a', {'data-tn': 'page-forward'})
            if next_button:
                next_button=next_button['href']
                next_button = urljoin(base_url, next_button)
            else:
                next_button_status=False
        page_number=1
        next_button_status=True    
        print("all data in while scrapped successfully...")
    print("  for loop ends for query")

    file_path = save_to_csv_firstdibs(scraped_data_list)
    return file_path

def start_process_rebag(search_queries, driver):
    print(" in rebag process function")
    base_url="https://shop.rebag.com/search?"
    scraped_data_list = []
    csv_heading = ['Description', 'Price', 'Condition']
    scraped_data_list.append(csv_heading)
    page_number=1
    next_button_status='false'
    searched_url=""
    
    for query in search_queries:
        
        search_rebag(query, driver)
        # time.sleep(10)
        # close_modal_dialog(driver)
        time.sleep(10)
        search_result_url=driver.current_url
        # p=1
        while next_button_status=='false':
            if page_number>1:
                if search_result_url == 'NULL':
                    search_result_url=driver.current_url
                # Modify the URL to include the page number
                modified_url = f"{search_result_url}&page={page_number}"
                driver.get(modified_url)
                time.sleep(10)
                close_modal_dialog(driver)
                WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'plp__products-grid-container')))
                productGrid=driver.find_element(By.CLASS_NAME, 'plp__products-grid-container')
            
            # get relevant div and extract links in href_list
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            div_elements=[]
            div_elements = soup.find_all('div', {'class': 'plp-product'})
            image_element1 = driver.find_element(By.XPATH, f'/html/body/div[2]/div/section/div[5]/div/div/div[2]/div[2]/div[2]/div[1]/a/div[2]/img')
            image_element2 = driver.find_element(By.XPATH, f'/html/body/div[2]/div/section/div[5]/div/div/div[2]/div[2]/div[2]/div[2]/a/div[2]/img')
            image_element3 = driver.find_element(By.XPATH, f'/html/body/div[2]/div/section/div[5]/div/div/div[2]/div[2]/div[2]/div[3]/a/div[2]/img')
            
            #Print the div_element to see its content
            # print(div_elements) 
            # i=1
            if div_elements:
                
                for div_element in div_elements:
                    title_element = div_element.find('span', {'class': 'products-carousel__card-title'})
                    title_element_text=title_element.text.strip()
                    condition_element = div_element.find('span', {'class': 'products-carousel__card-condition'})
                    condition_element_text=condition_element.text.strip()
                    price_element = div_element.find('span', {'class': 'products-carousel__card-price'})
                    price_element_text=price_element.text.strip()
                    data=[]
                    data.append(title_element_text)
                    data.append(price_element_text)
                    data.append(condition_element_text)
                    print('-------------------')
                    print('description', title_element_text)
                    print('price', price_element_text)
                    print('condition', condition_element_text)
                    scraped_data_list.append(data)
                    print(str(data))
                    query=""
            else:
                print("No div element found ")
                break
            # i+=1
            # print("i -  :"+str(i))
            # if i==3:
            #     break
            save_to_csv_rebag(scraped_data_list,image_element1,image_element2,image_element3)
            page_number +=1
            # Check if there is a next page
            next_page_element = soup.find('a', {'class': 'rbg-pagination__next'})
            if next_page_element == None:
                next_button_status='true'
            else:
                next_page_element = soup.find('a', {'class': 'rbg-pagination__next'})
                next_button_status=next_page_element.get('aria-disabled')
                # p+=1
            # if p==3:
            #     break
        # p=1
        next_button_status='false' 
        page_number =1     
        print(str(query)+" has run succesfully")
    print("  for loop ends for query")
    print("Data to be saved:", scraped_data_list[1:])  # Print the data without headers
    save_to_csv_rebag(scraped_data_list[1:],image_element1,image_element2,image_element3)  # Pass the data without headers to the function
    file_path = save_to_csv_rebag(scraped_data_list)
    return file_path

def start_process_madison(search_queries, driver):
    print("in madison view process function ")
    base_url="https://www.madisonavenuecouture.com/"
    scraped_data_list=[]
    
    csv_haeding = ['Description', 'Price', 'Condition']
    scraped_data_list.append(csv_haeding)
    
    next_button_status=True
    searched_url=""
    for query in search_queries:
        search_madison(query, driver)
        searched_url=driver.current_url
        time.sleep(5)
        # p=1
        while next_button_status==True:
            if searched_url != driver.current_url and searched_url!="":
                driver.get(searched_url)
            # Find the iframe element
            iframe = driver.find_element(By.CSS_SELECTOR,'iframe[data-reactroot=""]')
            # Switch to the iframe
            driver.switch_to.frame(iframe)
            # get relevant div and extract links in href_list
            html=driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            div_elements = soup.find_all('a', {'class': 'findify-widget--product _1anW_'})
            #Print the div_element to see its content
            if div_elements:
                    for div in div_elements:
                        if div:
                            search_result_url = div['href']
                            
                            full_url = urljoin(base_url, search_result_url)
                            scrapData(scraped_data_list,full_url,driver,base_url)
                            
                    save_to_csv_madison(scraped_data_list)
            else:
                print("No div element found ")
                break
        
            driver.get(searched_url)

            time.sleep(5)
            next_button=soup.find('button', {'class': 'findify-widget--pagination__next'})
            if next_button==None:
                next_button_status=False
            else:
                parsed_url = urlparse(searched_url)
                query_params = parse_qs(parsed_url.query)
                findify_limit = query_params.get('findify_limit', [None])[0]
                findify_offset = query_params.get('findify_offset', [None])[0]
                if findify_offset==None:
                    findify_offset = findify_limit
                    del query_params['findify_limit']  # Remove findify_limit 
                    query_params['findify_limit'] = findify_limit
                    query_params['findify_offset'] = findify_offset

                    query_params_str = urlencode(query_params, doseq=True)
                    decoded_query_params_str = unquote(query_params_str)
                    decoded_query_params_str = decoded_query_params_str.replace('+', '%20')

                    modified_url = urlunparse(parsed_url._replace(query=decoded_query_params_str))
                    searched_url=modified_url
                    print(" new url for first time is "+searched_url)
                else:
                    doubled_offset = int(findify_offset) + 24
                    query_params['findify_offset'] = [str(doubled_offset)]
                    query_params_str = urlencode(query_params, doseq=True)
                    modified_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{query_params_str}"
                    searched_url=modified_url
                    print(" new url for first second time is "+searched_url)
        next_button_status=True    
        driver.get(base_url)
        print("all data in while scrapped successfully...")
    print("  for loop ends for query")

    file_path = save_to_csv_madison(scraped_data_list)
    return file_path

def read_search_queries():
    # Replace 'YOUR_API_AUTHORIZATION_TOKEN' with your actual API authorization token
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }

    # Fetching the products
    response = requests.post('https://www.wixapis.com/stores/v1/products/query', headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Handle the retrieved products data
        search_queries = []
        for product in data['products']:
            item = product['name']

            # Append the search query to the list
            search_queries.append([item])
            print(item,id)
        return search_queries
    else:
        print("Failed to fetch products. Status code:", response.status_code)
        return []

import requests
import json

def get_product_names_from_wix():
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }

    # GETTING All PRODUCTS
    response = requests.post('https://www.wixapis.com/stores/v1/products/query', headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Handle the retrieved products data
        product_names = []  # Create an empty list to store product names
        product_id = []  # Create an empty list to store product names
        for product in data['products']:
            product_names.append(product['name']) 
            product_id.append(product['id'])
        return product_names,product_id
    else:
        print("Failed to fetch products. Status code:", response.status_code)
        return []
    
def madison(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr = get_product_names_from_wix()
        print(description_arr[0])
        for row in description_arr[0]:
            print('Product --->>', row)
        file_path = ''
        while 1:
            try:
                chrome_options = uc.ChromeOptions()
                
                driver = webdriver.Chrome(executable_path="chromedriver.exe", service=Service(ChromeDriverManager().install()), options=chrome_options)
                driver.maximize_window()
                # driver = uc.Chrome(service=Service(ChromeDriverManager().install()))
                print('function calling')
                time.sleep(5)
                file_path = start_process_madison(description_arr, driver)

                driver.quit()
                print('File Path',file_path)
                file_path = "/" + file_path
                break
            except Exception as e:
                print('<------ Access Denied ------>',e)
                driver.quit()
                time.sleep(10)
          
        return render(request, 'madison.html',context={'csv_file':file_path})
    return render(request, 'madison.html')

    
def rebag(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr = read_search_queries()
        file_path = ''
        while 1:
            try:
                chrome_options = Options()
                driver = webdriver.Chrome(executable_path='chromedriver.exe')
                driver.maximize_window()
                print('function calling')
                file_path = start_process_rebag(description_arr, driver)

                driver.quit()
                print('File Path', file_path)
                file_path = "/" + file_path
                break
            except Exception as e:
                print('<------ Access Denied ------>', e)
                driver.quit()
                time.sleep(10)
          
        return render(request, 'rebag.html', context={'csv_file': file_path})
    return render(request, 'rebag.html')

def fetch_wix_data():
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }

    # GETTING All PRODUCTS
    response = requests.post('https://www.wixapis.com/stores/v1/products/query', headers=headers)

    if response.status_code == 200:
        data = response.json()
        product_names = [product['name'] for product in data['products']]
        return product_names
    else:
        print("Failed to fetch products. Status code:", response.status_code)
        return []
    
def firstdibs(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr = fetch_wix_data()
        # for row in description_arr:
        #     print('Product --->>',row)
        file_path = ''
        while 1:
            try:
                chrome_options = uc.ChromeOptions()
                
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),  options=chrome_options)
                driver.maximize_window()
                # driver = uc.Chrome(service=Service(ChromeDriverManager().install()))
                print('function calling')
                # time.sleep(5)
                try:
                    file_path = start_process_firstdibs(description_arr, driver)
                except:
                    print(" in main firstdibs inner exception ")
                driver.quit()
                print('File Path',file_path)
                file_path = "/" + file_path
                break
            except Exception as e:
                print('<------ Access Denied ------> in main firstdibs',e)
                driver.quit()
                time.sleep(10)
          
        return render(request, 'firstdibs.html',context={'csv_file':file_path})
    return render(request, 'firstdibs.html')




import time
import random
import csv
import requests
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.shortcuts import render  # Assuming this is a Django web application

def search(key_word, driver, data_list):
    print('--- Search Function ---', key_word)
    driver.get("https://www.ebay.com/")
    time.sleep(2)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[1]/div[1]/div/input[1]')))
    driver.find_element(By.XPATH,'/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[1]/div[1]/div/input[1]').send_keys(key_word)
    driver.find_element(By.XPATH,'/html/body/header/table/tbody/tr/td[3]/form/table/tbody/tr/td[3]/input').click()
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="srp-river-results"]/ul')))
    time.sleep(2)

    # Collect the data from the search results
    try:
        result_elements = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="srp-river-results"]/ul/li')))
        for element in result_elements:
            # Get the text representation of the whole search result
            result_text = element.text

            # Parse the text to extract the required details (assuming a specific format)
            description = None
            current_price = None
            before_discount = None
            condition = None

            # Parse the result_text to extract the relevant details.
            # Modify the parsing logic based on the actual format of the result_text.
            # This example assumes the format: "Description\nCurrent Price\nBefore Discount\nCondition"
            details_list = result_text.split('\n')
            print(len(details_list))
            if len(details_list) >= 4:
                description = details_list[0]
                current_price = details_list[1]
                before_discount = details_list[2]
                condition = details_list[3]
                condition4 = details_list[4]
                condition5 = details_list[5]
                condition6 = details_list[6]
                condition7 = details_list[7]
                condition8= details_list[8]
                condition9 = details_list[9]

            # Append the extracted details to the data_list as a tuple
            data_list.append((description, current_price, before_discount, condition,condition4,condition5,condition6,condition7,condition8,condition9))
    except Exception as e:
        print("Error while collecting data:", e)

def save_to_csv(scraped_list):
    api_url = 'https://www.wixapis.com/stores/v1/products'
    api_token = 'YOUR_WIX_API_TOKEN'
    print("gere")
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }
    print("game`")
    print(scraped_list)
    print(scraped_list[0])
    print(scraped_list[1][1])

    price1 = price_str_to_int(scraped_list[1][1])
    price2 = price_str_to_int(scraped_list[2][1])
    price3 = price_str_to_int(scraped_list[3][1])

    json_data = {
        'product': {
            'name': scraped_list[1][0],
            'productType': 'physical',
            'priceData': {
                'price': price1,
            },
            'condition': scraped_list[1][2],
            # Add other fields as needed for the Wix API
        }
    }

    response = requests.post(api_url, headers=headers, json=json_data)

    json_data = {
        'product': {
            'name': scraped_list[2][0],
            'productType': 'physical',
            'priceData': {
                'price': price2,
            },
            'condition': scraped_list[2][2],
            # Add other fields as needed for the Wix API
        }
    }

    response = requests.post(api_url, headers=headers, json=json_data)
    
    json_data = {
        'product': {
            'name': scraped_list[3][0],
            'productType': 'physical',
            'priceData': {
                'price': price3,
            },
            'condition': scraped_list[3][2],
            # Add other fields as needed for the Wix API
        }
    }

    response = requests.post(api_url, headers=headers, json=json_data)

    print(f'Status code: {response.status_code}')
    print(f'Response: {response.json()}')










from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.shortcuts import render

def ebay(request):
    if request.method == 'POST':
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }

        response = requests.post('https://www.wixapis.com/stores/v1/products/query', headers=headers)

        if response.status_code == 200:
            data = response.json()
            products_array = []

            for product in data['products']:
                products_array.append({
                    'name': product['name'],
                    'product_id': product['id'],
                    'product_price': product['price']
                })

            driver = webdriver.Chrome(executable_path='chromedriver.exe')

            scraped_data = {
                'Image': [],
                'Title': [],
                'Price': [],
            }

            updated_product_ids = set()

            for product_data in products_array:
                product_name = product_data['name']
                product_id = product_data['product_id']

                if product_id in updated_product_ids:
                    print(f"Product already updated: {product_name}")
                    continue

                # Extract the first three words from the product_name
                search_words = ' '.join(product_name.split()[:3])

                driver.get("https://www.ebay.com/")
                time.sleep(2)

                search_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, '_nkw')))
                search_input.send_keys(search_words)

                search_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'gh-btn')))
                search_button.click()

                time.sleep(2)
                try:
                    # Scraping the elements
                    try:
                        image_element = driver.find_element(By.XPATH, f'/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[3]/div/div[1]/div/a/div/img')
                    except NoSuchElementException:
                        try:
                            image_element = driver.find_element(By.XPATH, f'/html/body/div[5]/div/4/div[2]/div[1]/div[2]/ul/li[2]/div/div[1]/div/a/div/img')
                        except NoSuchElementException:
                            try:
                                image_element = driver.find_element(By.XPATH, f'/html/body/div[5]/div/4/div[2]/div[1]/div[2]/ul/li[4]/div/div[1]/div/a/div/img')
                            except NoSuchElementException:
                                raise NoSuchElementException(f"No image found for product: {product_name}")

                    try:
                        title_element = driver.find_element(By.XPATH, f'/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[3]/div/div[2]/a/div/span')
                    except NoSuchElementException:
                        try:
                            title_element = driver.find_element(By.XPATH, f'/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[2]/a/div/span')
                        except NoSuchElementException:
                            raise NoSuchElementException(f"No title found for product: {product_name}")

                    try:
                        price_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[3]/div/div[2]/div[4]/div[1]/span')
                    except NoSuchElementException:
                        try:
                            price_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[2]/div/div[2]/div[3]/div[1]/span')
                        except NoSuchElementException:
                            try:
                                price_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[1]/div/div[2]/div[4]/div[1]/span')
                            except NoSuchElementException:
                                price_element = driver.find_element(By.XPATH, '/html/body/div[5]/div[4]/div[2]/div[1]/div[2]/ul/li[1]/div/div[2]/div[3]/div[1]/span')
                    # Extract the relevant information
                    image = image_element.get_attribute('src')
                    title = title_element.text
                    price = price_element.text

                    # Extract numeric part of the price and convert to integer
                    price_numeric = re.findall(r'\d+\.\d+', price)
                    if len(price_numeric) > 0:
                        price_int = int(float(price_numeric[0]) * 100)  # Convert to cents (integer) for better precision
                    else:
                        print(f"Failed to extract numeric price for product: {product_name}. Skipping...")
                        continue

                    # Prepare the data for API update
                    scraped_product_data = {
                        'product': {
                            'name': title,
                            'productType': 'physical',
                            'priceData': {
                                'price': price_int,
                            },
                        },
                    }

                    response = requests.patch(f'https://www.wixapis.com/stores/v1/products/{product_id}', headers=headers, json=scraped_product_data)
                    response1 = requests.post('https://www.wixapis.com/stores/v1/products', headers=headers, json=scraped_product_data)

                    if response1.status_code == 200:
                        print(f"Product updated successfully: {product_name}")
                        updated_product_ids.add(product_id)  # Add the product ID to the set
                    else:
                        print(f"Failed to update product: {product_name}. Status code: {response.status_code}, {response.content}")

                    if response.status_code == 200:
                        print(f"Product updated successfully: {product_name}")
                        updated_product_ids.add(product_id)  # Add the product ID to the set
                    else:
                        print(f"Failed to update product: {product_name}. Status code: {response.status_code}, {response.content}")

                except (NoSuchElementException, InvalidSelectorException) as e:
                    print(f"Element not found or invalid selector for product: {product_name}. Retrying... Error: {str(e)}")

                else:
                # If the loop completes without a successful break, print a message
                    print(f"Could not scrape data for product: {product_name} even after retries. Skipping...")
                    continue
            driver.quit()
        else:
            print(f"Failed to fetch products. Status code: {response.status_code}, {response.content}")

    return render(request, 'ebay.html')











# Sign in
def realreal_signin(driver):
    print('------ Signing In -------')
    driver.get("https://www.therealreal.com")
    #Sign in button
    driver.find_element(By.XPATH,'/html/body/div[3]/div/div[1]/div[2]/div/div[1]/a').click()
    time.sleep(3)
    #Email input
    email_element = driver.find_elements(By.ID,'user_email')
    email_element[1].send_keys("test009@gmail.com")
    time.sleep(2)
    #Password input
    password_element = driver.find_elements(By.ID,'user_password')
    password_element[1].send_keys("test0099")
    #Login
    time.sleep(2)
    login_btn_parent = driver.find_elements(By.ID,'user_submit_action')
    login_btn = login_btn_parent[1].find_element(By.CLASS_NAME,'form-field__submit')
    login_btn.click()

# search
# /html/body/div[1]/header/div[4]/div[1]/div[1]/form/div/div/input
# /html/body/div[1]/header/div[4]/div[1]/div[1]/form/div/div/button
def search_realreal(keyword, driver):
    print('------ Searching Products -------')
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/nav/div[1]/div[2]/div[1]/form/div/div/input')))       
    driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/div[1]/div[2]/div[1]/form/div/div/input').send_keys(keyword)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/nav/div[1]/div[2]/div[1]/form/div/div/div/button[2]')))
    driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/div[1]/div[2]/div[1]/form/div/div/div/button[2]').click()
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/main/div[2]/div[4]/div[5]/div')))
        items_grid = driver.find_element(By.XPATH,'/html/body/div[1]/div[1]/main/div[2]/div[4]/div[5]/div')
        item_list = items_grid.find_elements(By.CLASS_NAME,'js-product-card-wrapper')
        print(len(item_list),"<---- Total Items")
        return item_list
    except:
        if len(keyword.rsplit(' ')) > 1:
            new_keyword = keyword.rsplit(' ', 1)[0]
            search_realreal(new_keyword)
        else:
            print("Keyword not found")
def fetch_details_realreal(item):
    print('------ Real Real Fetching Details -------')
    brand_name = item.find_element(By.CLASS_NAME, 'product-card__brand').text
    discription = item.find_element(By.CLASS_NAME, 'product-card__description').text

    try:
        temp_price = item.find_element(By.CLASS_NAME, 'product-card__msrp').text
        temp_price_split = temp_price.split('$')
        retail_price = temp_price_split[1]
    except:
        retail_price = 0

    try:
        temp_price = item.find_element(By.CLASS_NAME, 'product-card__price').text
        temp_price_split = temp_price.split('$')
        product_price = temp_price_split[1]
    except:
        temp_price = item.find_element(By.CLASS_NAME, 'product-card__price-strike-through').text
        temp_price_split = temp_price.split('$')
        product_price = temp_price_split[1]

    try:
        temp_price = item.find_element(By.CLASS_NAME, 'product-card__discount-price').text
        temp_price_split = temp_price.split('$')
        discount_price = temp_price_split[1].split('\n')[0]
    except:
        discount_price = 0

    hold_details = []
    hold_details.append(brand_name)
    hold_details.append(discription)
    hold_details.append(retail_price)
    hold_details.append(product_price)
    hold_details.append(discount_price)
    return(hold_details)

def realreal_process(reader,driver):
    scraped_list = []
    csv_haeding = ['Brand Name', 'Discription', 'Retail Price', 'Product Price', 'Discount Price']
    scraped_list.append(csv_haeding)
    realreal_signin(driver)
    time.sleep(2)
    for row in reader:
        item_list = search_realreal(row, driver)
        for item in item_list:
            scraped_list.append(fetch_details_realreal(item))
    print('Item List',item_list)
    random_number = random.randint(1, 10000)
    file_path = f'static/realrealproducts{random_number}.csv'
    with open(file_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write each row of data to the CSV file
        for row in scraped_list:
            writer.writerow(row)
    return file_path

def realreal(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr=[]
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('iso-8859-1').splitlines()
        reader = csv.reader(decoded_file)
        for row in reader:
            print('Product --->>',row[0])
            description_arr.append(row)
        file_path = ''
        try:
            try:
                driver = uc.Chrome()
            except Exception as e:
                print(e,"<<<<<<<<<<<<<")
            print('function calling')
            time.sleep(5)
            file_path = realreal_process(description_arr, driver)

            driver.quit()
            print('File Path',file_path)
            file_path = "/" + file_path
        except Exception as e:
            print('<------ Access Denied ------>',e)
            time.sleep(10)
          
        return render(request, 'realreal.html',context={'csv_file':file_path})
    return render(request, 'realreal.html')



import requests
import random
import csv
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

import requests
import random
import csv
from urllib.parse import quote_plus
from bs4 import BeautifulSoup


def maisondeluxe(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr = []
        base_url = "https://www.maisondeluxeonline.com/search"

        # Fetching the products from Wix
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
            'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
        }

        response = requests.post('https://www.wixapis.com/stores/v1/products/query', headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for product in data.get('products', []):
                description_arr.append(product.get('name', ''))
        else:
            print("Failed to fetch products from Wix. Status code:", response.status_code)
            return render(request, 'maisondeluxe.html')

        scrapped_list = []
        csv_haeding = ['Discription','Product Price', 'Discount Price' , 'Status','Condition']
        scrapped_list.append(csv_haeding)
        for desc in description_arr:
            print('<<----- Product Desc --->>',desc)
            # Define the search query
            search_query = desc

            # Encode the search query
            encoded_query = quote_plus(search_query)

            # Construct the full URL
            full_url = f"{base_url}?type=product&page=1&q={encoded_query}"

            # Get the HTML of the website
            response = requests.get(full_url)
            # print(response)
            # Create a BeautifulSoup object
            soup = BeautifulSoup(response.content, "html.parser")
            try:
                pages  = soup.find(class_="pagecount").text
                # Split the string by spaces
                split_text = pages.split()

                # Get the last element from the split
                last_value = split_text[-1]
                for page in range(int(last_value)):
                    page_number = page+1
                    page_str = str(page_number)
                    print(page+1)
                    full_url = f"{base_url}?type=product&page={page_str}&q={encoded_query}"
                    response = requests.get(full_url)
                    # Create a BeautifulSoup object
                    soup = BeautifulSoup(response.content, "html.parser")
                    # Find all div elements with class "product-detail"
                    product_details = soup.find_all('div', class_='product-detail')
                    product_infos = soup.find_all('div', class_='product-info')
                    # print(product_details)
                    # Iterate over the found elements
                    for product_detail in product_details:
                        scrapped_data = []
                        # Find the nested elements with classes "title" and "price-area"
                        title_element = product_detail.find(class_="title")
                        price_element = product_detail.find(class_="price-area")
                        product_info = product_detail.find_previous_sibling('div')

                        # Extract the text from the nested elements
                        title_text = title_element.find('a').get_text(strip=True) if title_element else ''
                        try:
                            org_price_text = price_element.find(class_="was-price").get_text(strip=True) if price_element else ''
                        except:
                            org_price_text = 0
                        dis_price_text = price_element.find(class_="price").get_text(strip=True) if price_element else ''

                        # Print the extracted text
                        scrapped_data.append(title_text )
                        if org_price_text != 0:
                            scrapped_data.append(org_price_text )
                            scrapped_data.append(dis_price_text )
                        else:
                            scrapped_data.append(dis_price_text)
                            scrapped_data.append('None' )
                        status = ''
                        if org_price_text == '' and dis_price_text == '':
                            status = 'Sold out'
                        else:
                            status  = 'Available'
                        scrapped_data.append(status)
                        product_info = product_detail.find_previous_sibling('div')
                        try:
                            condition = product_info.find(class_="price").find_next_sibling().get_text(strip=True)
                        except:
                            condition = ''
                        scrapped_data.append(condition)
                        scrapped_list.append(scrapped_data)
                                            
                        
                        print("Title:", title_text)
                        print("Price:", org_price_text)
                        print("Discount Price:", dis_price_text)
                        print("Condition:", condition)
                        print()  # Add a blank line for readability
            except:
                product_details = soup.find_all('div', class_='product-detail')
                # print(product_details)
                # Iterate over the found elements
                for product_detail in product_details:
                    scrapped_data = []
                    # Find the nested elements with classes "title" and "price-area"
                    title_element = product_detail.find(class_="title")
                    price_element = product_detail.find(class_="price-area")

                    # Extract the text from the nested elements
                    title_text = title_element.find('a').get_text(strip=True) if title_element else ''
                    try:
                        org_price_text = price_element.find(class_="was-price").get_text(strip=True) if price_element else ''
                    except:
                        org_price_text = 0
                    dis_price_text = price_element.find(class_="price").get_text(strip=True) if price_element else ''

                    # Print the extracted text
                    scrapped_data.append(title_text )
                    if org_price_text != 0:
                        scrapped_data.append(org_price_text )
                        scrapped_data.append(dis_price_text )
                    else:
                        scrapped_data.append(dis_price_text)
                        scrapped_data.append('None' )
                    status = ''
                    if org_price_text == '' and dis_price_text == '':
                        status = 'Sold out'
                    else:
                        status  = 'Available'
                    scrapped_data.append(status)
                    product_info = product_detail.find_previous_sibling('div')
                    try:
                        condition = product_info.find(class_="price").find_next_sibling().get_text(strip=True)
                    except:
                        condition = ''
                    scrapped_data.append(condition)
                    scrapped_list.append(scrapped_data)
                    print("Title:", title_text)
                    print("Price:", org_price_text)
                    print("Discount Price:", dis_price_text)
                    print()  # Add a blank line for readability
        print('------------------------------------')
        print(scrapped_list)
        if dis_price_text:
            price = float(dis_price_text.replace(',', '').replace('$', ''))
        else:
            price = 5000  # Or any other appropriate default value

        for product_detail in product_details:
            scrapped_data = []


            # Your existing code to extract data...

            # Create the JSON data for adding a product to Wix
            json_data = {
                'product': {
                    'name': title_text,
                    'productType': 'physical',
                    'priceData': {
                        'price': price,
                    },
                    # Other data fields you want to add...
                }
            }

            # Send a POST request to add the product to Wix
            response = requests.post('https://www.wixapis.com/stores/v1/products', headers=headers, json=json_data)

            if response.status_code == 200:
                print("Product added to Wix:", title_text)
            else:
                print("Failed to add product to Wi  x. Status code:", response.content)
    
        return render(request, 'maisondeluxe.html')
    
    return render(request, 'maisondeluxe.html')

def main_page(request):
    return render(request, 'index.html')
