from django.shortcuts import render
from selenium.webdriver.chrome.options import Options
import re
import os
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
import random
import string
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



import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup



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


def remove_non_bmp_characters(input_string):
    return ''.join(char for char in input_string if ord(char) <= 0xFFFF)





def search_madison(row, driver):
    # Extract the first three words from the search_query
    first_three_words = ' '.join(row.split()[:3])
    print('--- Search Function ---', first_three_words)
    driver.get("https://www.madisonavenuecouture.com/")
    
    # Other code for searching, waiting, and interacting with the page elements
    # ...

    # Update the input element with the first three words
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/header/div[3]/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div[1]/form/input[2]')))
    input_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/header/div[3]/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div[1]/form/input[2]')
    input_element.send_keys(Keys.CONTROL + "a")  # Select all text
    input_element.send_keys(Keys.DELETE)         # Delete selected text
    time.sleep(2)
    
    # Send the first three words to the input element
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/header/div[3]/div/div[2]/div[2]/div/div[3]/div[1]/div/div/div[1]/form/input[2]')))
    input_element.send_keys(remove_non_bmp_characters(first_three_words))
    
    # Click the search button
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

def search_rebag(query, driver):
        
        print("hello", query)

        driver.get("https://shop.rebag.com/search?")
        time.sleep(3)
        body_element = driver.find_element(By.TAG_NAME, 'body')
        body_element.click()
        time.sleep(3)
        close_modal_dialog(driver)
        
        try:
            time.sleep(3)
            try:
                input_element = driver.find_element(By.XPATH, '/html/body/div[2]/header/div/div/div[2]/div/div/div[1]/div/form/div/input')
            except:
                input_element = driver.find_element(By.XPATH, '/html/body/div[2]/header/div/div/div[2]/div/div/div[1]/div/form/div/input')

            input_element.send_keys(Keys.CONTROL + "a")
            input_element.send_keys(Keys.DELETE)

            # Convert list elements to strings and join them
            search_query_parts = query.split()
            # Extract the desired parts from the split query parts
            result_parts = search_query_parts[:3] + search_query_parts[5:6]  # Extract specific parts
            result_string = " ".join(result_parts)
            input_element.send_keys(result_string, Keys.RETURN)



            print("working", result_string)

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'plp__products-grid-container')))
            print('Search Done for Rebag')

        except Exception as e:
            print('<------ Access Denied ------>', e)




def search_firstdibs(search_query, driver):
    print('--- Search Function ---', search_query)
    driver.get("https://1stdibs.com")
    #search
    time.sleep(5) 
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/div[1]/div/form/div/div/div/div/div[1]/div/input')))
        input_element = driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/div[1]/div/form/div/div/div/div/div[1]/div/input')
        input_element.clear()
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/div[1]/div/form/div/div/div/div/div[1]/div/input')))
        input_element.send_keys(search_query)
        driver.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/div[1]/div/form/div/div/div/div/div[2]/div[2]/button').click()
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




def save_to_csv_firstdibs(scraped_data_list):
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
    print("first dibs working",scraped_data_list)
    print(scraped_data_list[0])
    print(scraped_data_list[1][0])
    print(scraped_data_list[1][1])
    print(scraped_data_list[1][2])
    

    price1 = price_str_to_int(scraped_data_list[1][1])
    json_data = {
        'product': {
            'name': scraped_data_list[1][0],
            'productType': 'physical',
            'priceData': {
                'price': price1,
            },
            'condition': scraped_data_list[1][2],
            # Add other fields as needed for the Wix API
        }
    }
    image= scraped_data_list[1][3]

    response = requests.post(api_url, headers=headers, json=json_data)
    print(response)
    response_data = response.json()
    # Extract the product ID from the response content
    extracted_product_id = response_data['product']['id']
    print(extracted_product_id)
    json_data = {
        'media': [
            {
                'mediaId': '19620272_1687322489998.jpg',
            },
            {
                'url': image,
            },
            {
                'mediaId': '19620272_1687322489998',
            },
        ],
    }
    response = requests.post(
        f'https://www.wixapis.com/stores/v1/products/{extracted_product_id}/media',
        headers=headers,
        json=json_data,
    )
    print(response.status_code)
    print(response.json())

    csv_file_path = 'output_datafirst.csv'  # Change to your desired CSV file path
    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_file_path)

    # Open the CSV file in the appropriate mode
    with open(csv_file_path, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        if not file_exists:
            writer.writerow(['Image', 'Title', 'Price', 'Condition'])  # Write header row

        for scrapped_data in scraped_data_list:
            Condition = scrapped_data[2]  # Use the current scrapped_data instead of the entire list
            title = scrapped_data[0]
            price = scrapped_data[1]
            writer.writerow([image, title, price, Condition])

def save_to_csv_madison(scraped_list):

    api_url = 'https://www.wixapis.com/stores/v1/products'
    api_token = 'YOUR_WIX_API_TOKEN'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjYzYzA5MDk4LTk1M2ItNDJmOC1iOWUyLWY3NWM0NmJjZGI0ZFwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcImNiZWEwNTJiLWM3YjctNGY2Ny1hNTE2LTM5ZGQwMjhhMjJkMlwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCI4ODA1ZDA2MC03NjA4LTQ0NzYtYTMzYS03ODA0YWM0YzZhMmNcIn19IiwiaWF0IjoxNjkyMTI2OTk5fQ.fdAs9YtidmgITS1B_DYr6YmKuGyUMjPDpRj-L-FWl_qwYVcrW4sZMSvdyPVOSe32gqKLbm0t8MzeIb1cUs8D_Tz1tXoWEeZLoQODwXNQ6eqniMEhJrKkekEh5KlguyDNcEKIWgxkeeIeVqk7BDAGrZvv-f6XNgyxlVw4KWHL3006XGsk9W182vpKd3I1_1l1_zSdfYQrnoFjQRCw-sU_HYaL8wvIf-PMD8ufjswe4GyGPmUgzHN6uYijLZ7yac6m22AI6B1nVNnSDoUb0DWa_6bkcb4mFMca4ji7uq4A3BcTqeJtd7sQzdGYu0RiFaU5pe3fU5rCXqgrNNjeAfXWgw',
        'wix-site-id': 'a4577014-181b-4d27-bb2d-ad476751caef',
    }

    data_to_write = []  # This list will store the data for CSV

    for scraped_item in scraped_list:
        try:
            print("get here")
            prod_name = scraped_item[0]
            prod_price_str = scraped_item[1]
            prod_condition = scraped_item[2]
            prod_image = scraped_item[3]

            numeric_part = re.search(r'\d+(,\d{3})*\.\d+', prod_price_str).group()
            prod_price = float(numeric_part.replace(',', ''))

            json_data = {
                'product': {
                    'name': prod_name,
                    'productType': 'physical',
                    'priceData': {
                        'price': prod_price,
                    },
                    'condition': prod_condition,
                }
            }

            response = requests.post(api_url, headers=headers, json=json_data)
            print(response.content)
            response_data = response.json()
            extracted_product_id = response_data['product']['id']

            url1 = 'https:' + prod_image
            json_data1 = {
                'media': [
                    {
                        'mediaId': '19620272_1687322489998.jpg',
                    },
                    {
                        'url': url1,
                    },
                    {
                        'mediaId': '19620272_1687322489998',
                    },
                ],
            }

            response = requests.post(
                f'https://www.wixapis.com/stores/v1/products/{extracted_product_id}/media',
                headers=headers,
                json=json_data1,
            )

            # Append data to the list for CSV
            data_to_write.append([prod_name, prod_price_str, prod_condition, prod_image, extracted_product_id])
        except Exception as e:
            print(e)
            continue
    # Save data to CSV file
    with open('product_datamadison.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Name', 'Price', 'Condition', 'Image', 'Product ID'])  # Writing header
        csv_writer.writerows(data_to_write)


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


def save_to_csv_rebag(scraped_list):
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
    price4 = price_str_to_int(scraped_list[4][1])

    image1 = scraped_list[1][3]
    image2 = scraped_list[2][3]
    image3 = scraped_list[3][3]
    image4 = scraped_list[4][3]



    print(image1,image2,image3,image4)


    # Adding the image URL to the existing JSON data structure
    json_data = {
    'product': {
        'name': "Hermes "+ scraped_list[1][0],
        'productType': 'physical',
        'priceData': {
            'price': price1,
        },
        'condition': scraped_list[1][2],
    },
    }

    json_data1 = {
    'product': {
        'name': "Hermes "+ scraped_list[2][0],
        'productType': 'physical',
        'priceData': {
            'price': price2,
        },
        'condition': scraped_list[2][2],
    },
    }

    json_data2 = {
    'product': {
        'name': "Hermes "+ scraped_list[3][0],
        'productType': 'physical',
        'priceData': {
            'price': price3,
        },
        'condition': scraped_list[3][2],
    },
    }

    json_data3 = {
    'product': {
        'name': "Hermes "+ scraped_list[4][0],
        'productType': 'physical',
        'priceData': {
            'price': price4,
        },
        'condition': scraped_list[4][2],
    },
    }

    response1 = requests.post(api_url, headers=headers, json=json_data)
    response2 = requests.post(api_url, headers=headers, json=json_data1)
    response3 = requests.post(api_url, headers=headers, json=json_data2)
    response4 = requests.post(api_url, headers=headers, json=json_data3)


    print(f'Status code: {response1.status_code}')
    print(f'Status code: {response2.status_code}')
    print(f'Status code: {response3.status_code}')
    print(f'Status code: {response4.status_code}')
    print(f'Response: {response1.json()}')


    response_data1 = response1.json()
    extracted_product_id1 = response_data1['product']['id']
    print(extracted_product_id1)
    json_data = {
        'media': [
            {
                'mediaId': '19620272_1687322489998.jpg',
            },
            {
                'url': image1,
            },
            {
                'mediaId': '19620272_1687322489998',
            },
        ],
    }
    response11 = requests.post(
        f'https://www.wixapis.com/stores/v1/products/{extracted_product_id1}/media',
        headers=headers,
        json=json_data,
    )
    print(response11.status_code)
    print(response11.json())


    response_data2 = response2.json()
    extracted_product_id2 = response_data2['product']['id']
    print(extracted_product_id2)
    json_data = {
        'media': [
            {
                'mediaId': '19620272_1687322489998.jpg',
            },
            {
                'url': image2,
            },
            {
                'mediaId': '19620272_1687322489998',
            },
        ],
    }
    response22 = requests.post(
        f'https://www.wixapis.com/stores/v1/products/{extracted_product_id2}/media',
        headers=headers,
        json=json_data,
    )
    print(response22.status_code)
    print(response22.json())

    response_data3 = response3.json()
    extracted_product_id3 = response_data3['product']['id']
    print(extracted_product_id3)
    json_data = {
        'media': [
            {
                'mediaId': '19620272_1687322489998.jpg',
            },
            {
                'url': image3,
            },
            {
                'mediaId': '19620272_1687322489998',
            },
        ],
    }
    response = requests.post(
        f'https://www.wixapis.com/stores/v1/products/{extracted_product_id3}/media',
        headers=headers,
        json=json_data,
    )
    print(response.status_code)
    print(response.json())



    response_data4 = response4.json()
    extracted_product_id4 = response_data4['product']['id']
    print(extracted_product_id4)
    json_data = {
        'media': [
            {
                'mediaId': '19620272_1687322489998.jpg',
            },
            {
                'url': image4,
            },
            {
                'mediaId': '19620272_1687322489998',
            },
        ],
    }
    response44 = requests.post(
        f'https://www.wixapis.com/stores/v1/products/{extracted_product_id4}/media',
        headers=headers,
        json=json_data,
    )
    print(response44.status_code)
    print(response44.json())


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

    description_image= soup.select_one('div[class="col-md-6 product-photos"]')
    print("description_image",description_image)
    description_element_div = soup.select_one('div[class="col-md-6 product-shop"]')

    description_element=description_element_div.find("h1",class_="product-title herm")
    price_element_div = soup.select_one("div[class='prices']")
    price_element=price_element_div.find("span", class_="money")
    condition_element = price_element_div.find("div", class_="product-condition")

    images = description_image.find("img", class_="lazyautosizes lazyloaded")

    print("image",images)
    image_url = images['src'] if images and 'src' in images.attrs else None
    description = description_element.text.strip() if description_element else None
    price = price_element.text.strip() if price_element else None
    condition = condition_element.text.replace("Condition:", "").strip() if condition_element else None
    data=[]
    data.append(description)
    data.append(price)
    data.append(condition)
    data.append(image_url)
    print('---------------------------------------')
    print('Description', description)
    print('price', price)
    print('condition', condition)
    print('condition', image_url)

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
    images = soup.select_one("img[class='_cfe61f48 _b62d9092']")
    print("images",images)

    image_url = images['src'] if images and 'src' in images.attrs else None
    description = description_element.text if description_element else None
    price = price_element.text if price_element else None
    condition = condition_element.text if condition_element else None

    data=[]
    data.append(description)
    data.append(price)
    data.append(condition)
    data.append(image_url)
    print('---------------------------------------------')
    print('description', description)
    print('Price', price)
    print('condition', condition)
    print('image', image_url)
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
    
    
    search_firstdibs(search_queries, driver)
    time.sleep(2)
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
            time.sleep(2)
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
                for div_element in div_elements[:1]:
                    a_tag = div_element.find('a', {'href': True, 'class': '_9e04a611 _9f85bf45 _f7a3e2b1'})

                    if a_tag:
                        search_result_url = a_tag['href']
                        full_url = urljoin(base_url, search_result_url)
                        scrapData_firstdibs(scraped_data_list,full_url,driver,base_url)
                        print("check working or not",scraped_data_list)
                
        else:
            print("No div element found ")
            break
        p+=1
        
        
        page_number+=1
        driver.get(searched_url)
        time.sleep(2)
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
    print(scraped_data_list)
    
       
    print("all data in while scrapped successfully...")
    print("  for loop ends for query")
    save_to_csv_firstdibs(scraped_data_list)

    
    return

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
        print(query)
        search_rebag(query, driver)
        # time.sleep(10)
        # close_modal_dialog(driver)
        time.sleep(4)
        search_result_url=driver.current_url
        # p=1
        while next_button_status=='false':
            if page_number>1:
                if search_result_url == 'NULL':
                    search_result_url=driver.current_url
                # Modify the URL to include the page number
                modified_url = f"{search_result_url}&page={page_number}"
                driver.get(modified_url)
                time.sleep(4)
                close_modal_dialog(driver)
                WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'plp__products-grid-container')))
                productGrid=driver.find_element(By.CLASS_NAME, 'plp__products-grid-container')
            
            # get relevant div and extract links in href_list
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            div_elements=[]
            div_elements = soup.find_all('div', {'class': 'plp-product'})
            
            #Print the div_element to see its content
            # print(div_elements) 
            # i=1
            if div_elements:
                
                for div_element in div_elements:

                    print("image image")
                    image_element = div_element.find('img', {'class': 'products-carousel__card-image'})

                    if image_element is not None:
                        print("image image image image")
                        image2 = image_element.get('src')
                        print("image image image image")
                    else:
                        print("Image element not found.")

                    # Rest of your code...






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
                    data.append(image2)

                    print('-------------------')
                    print('description', title_element_text)
                    print('price', price_element_text)
                    print('condition', condition_element_text)
                    print('image', image2)
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
        save_to_csv_rebag(scraped_data_list)
    print("  for loop ends for query")
    print("Data to be saved:", scraped_data_list[1:])  # Print the data without headers

    return 

def start_process_madison(row, driver):
    print("search_queries",row)

    print("in madison view process function ")
    base_url="https://www.madisonavenuecouture.com/"
    scraped_data_list=[]
    
    csv_haeding = ['Description', 'Price', 'Condition']
    # scraped_data_list.append(csv_haeding)
    
    next_button_status=True
    searched_url=""

    search_madison(row, driver)
    searched_url=driver.current_url
    time.sleep(3)
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
                for div in div_elements[:5]:
                    if div:
                        search_result_url = div['href']
                        
                        full_url = urljoin(base_url, search_result_url)
                        scraped_data_list = scrapData(scraped_data_list,full_url,driver,base_url)
                print('Scrapped Data List',scraped_data_list)           
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

        next_button_status=False 
    next_button_status=True    
    driver.get(base_url)
    print("all data in while scrapped successfully...")
    print("  for loop ends for query", scraped_data_list)
    save_to_csv_madison(scraped_data_list)
    file_path = ''
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
            try:
                chrome_options = uc.ChromeOptions()
                
                driver = webdriver.Chrome(ChromeDriverManager().install())
                driver.maximize_window()
                # driver = uc.Chrome(service=Service(ChromeDriverManager().install()))
                print('function calling')
                time.sleep(5)
                file_path = start_process_madison(row, driver)

                driver.quit()
                print('File Path',file_path)
                file_path = "/" + file_path
                continue
            except Exception as e:
                print('<------ Access Denied ------>',e)
                driver.quit()
                continue
          
        return render(request, 'madison.html',context={'csv_file':file_path})
    return render(request, 'madison.html')


def rebag(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr = []
        base_url = "https://shop.rebag.com/search"

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
        csv_heading = ['Description', 'Product Price', 'Discount Price', 'Status', 'Condition']
        scrapped_list.append(csv_heading)
        
        for desc in description_arr:
            # Split the search query into words and take the first three words
            search_query_words = desc.split()[:3]
            search_query = ' '.join(search_query_words)
            
            encoded_query = quote_plus(search_query)
            full_url = f"{base_url}?type=product&page=1&q={encoded_query}"


            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(full_url)

            time.sleep(10)

            # Find elements with class containing "plp__card"
            product_infos = driver.find_elements(By.CSS_SELECTOR, 'a.plp__card')

            if not product_infos:
                print("No product information found.")
                driver.quit()
            else:
                scrapped_list = []
                for product_detail in product_infos[:5]:

                    try:
                        print("working")

                        scrapped_data = []


                        title = product_detail.find_element(By.CSS_SELECTOR, 'span.products-carousel__card-designer')
                        title_text = title.text.strip() if title else ''

                        title_complete = product_detail.find_element(By.CSS_SELECTOR, 'span.products-carousel__card-title')
                        title_complete_number = title_complete.text.strip() if title_complete else ''

                        title_condition = product_detail.find_element(By.CSS_SELECTOR, 'span.products-carousel__card-condition')
                        condition_text = title_condition.text.strip() if title_condition else ''

                        price_element = product_detail.find_element(By.CSS_SELECTOR, 'span.products-carousel__card-price')
                        title_text_price = price_element.text.strip() if price_element else ''

                        image_tag = product_detail.find_element(By.CSS_SELECTOR, 'div.products-carousel__image-wrapper img')
                        print("image tag found",image_tag)
                        image_link = image_tag.get_attribute("src")
                        print("Image Link:", image_link)
                        
                        

                        combined_variable = title_text + " " + title_complete_number
                        print("hello i found data",image_link, combined_variable ,condition_text,title_text_price,)

                        scrapped_data.append(combined_variable)
                        scrapped_data.append(title_text_price)
                        scrapped_data.append(condition_text)
                        scrapped_data.append(image_link)
                        scrapped_list.append(scrapped_data)

                    except Exception as e :
                        print("Product Not Found",e)
                        continue
                driver.quit()
        for scrapped_data in scrapped_list:  # Skip the header row
            try:
                name = scrapped_data[0]
                price = scrapped_data[1]

                try:
                    price = price.replace("$", "").replace(",", "")  # Remove dollar sign and commas

                    if price.strip():  # Check if the string is not empty or whitespace
                        price = float(price)
                    else:
                        price = 0.0

                except Exception as e:
                    print(e)
                    price = 0.0


                if price > 0.0:

                    condition = scrapped_data[2]
                    image = scrapped_data[3]
                    
                    print(name,price,condition,"https:"+image)
                    json_data = {
                        'product': {
                            'name': name,
                            'productType': 'physical',
                            'priceData': {
                                'price': price,
                            },
                            'condition': condition,
                        },
                    }
                    
                    response = requests.post('https://www.wixapis.com/stores/v1/products', headers=headers, json=json_data)
                    
                    if response.status_code == 200:

                        response_data1 = response.json()
                        extracted_product_id1 = response_data1['product']['id']
                        json_data = {
                            'media': [
                                {
                                    'mediaId': '19620272_1687322489998.jpg',
                                },
                                {
                                    'url':image,
                                },
                                {
                                    'mediaId': '19620272_1687322489998',
                                },
                            ],
                        }
                        response11 = requests.post(
                            f'https://www.wixapis.com/stores/v1/products/{extracted_product_id1}/media',
                            headers=headers,
                            json=json_data,
                        )
                    

                    else:
                        print(f"Failed to add product '{name}'. Status code: {response.status_code}")
                else:
                    print("Product not added to Wix due to zero price:", desc)
            except Exception as e :
                print(e)
                continue

        csv_file_path = 'output_data1-Rebag.csv'  # Change to your desired CSV file path

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Image', 'Title', 'Price'])  # Write header row

            for scrapped_data in scrapped_list:  # Skip the header row
                image = scrapped_data[3]
                Condition = scrapped_data[2]
                title = scrapped_data[0]
                price = scrapped_data[1]
                writer.writerow([image, title, price,Condition])


        return render(request, 'rebag.html')
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

        file_paths = []
        print(description_arr)
        for query in description_arr:
            try:
                print(query)
                chrome_options = uc.ChromeOptions()
                driver = webdriver.Chrome(ChromeDriverManager().install())
                driver.maximize_window()

                file_path = start_process_firstdibs([query], driver)  # Pass query as a list
                driver.quit()

                file_paths.append(file_path)
            except Exception as e:
                print('<------ Exception occurred in main firstdibs ------>', e)
                driver.quit()
                time.sleep(2)

        return render(request, 'firstdibs.html', context={'csv_files': file_paths})
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
import requests
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, InvalidSelectorException
from webdriver_manager.chrome import ChromeDriverManager
from django.shortcuts import render  # Assuming you're using Django for rendering

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

            driver = webdriver.Chrome(ChromeDriverManager().install())

            scraped_data_array = []
            updated_product_ids = set()
            
            for product_data in products_array:
                product_name = product_data['name']
                product_id = product_data['product_id']

                if product_id in updated_product_ids:
                    print(f"Product already updated: {product_name}")
                    continue

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
                        price_int = int(float(price_numeric[0]) * 100)
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

                    response = requests.post('https://www.wixapis.com/stores/v1/products', headers=headers, json=scraped_product_data)

                    if response.status_code == 200:
                        response_data = response.json()

                        extracted_product_id = response_data['product']['id']
                        json_data = {
                            'media': [
                                {
                                    'mediaId': '19620272_1687322489998.jpg',
                                },
                                {
                                    'url': image,
                                },
                                {
                                    'mediaId': '19620272_1687322489998',
                                },
                            ],
                        }
                        response = requests.post(
                            f'https://www.wixapis.com/stores/v1/products/{extracted_product_id}/media',
                            headers=headers,
                            json=json_data,
                        )

                        scraped_data_array.append({
                            'Image': image,
                            'Title': title,
                            'Price': price
                        })

                        print(f"Product Added successfully: {product_name}")
                except (NoSuchElementException, InvalidSelectorException) as e:
                    print(f"Element not found or invalid selector for product: {product_name}. Retrying... Error: {str(e)}")

                else:
                    print(f"Could not scrape data for product: {product_name} even after retries. Skipping...")
                    continue
            driver.quit()

            # Save scraped data to a CSV file
            csv_file_path = 'output_data.csv'  # Change to your desired CSV file path

            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ['Image', 'Title', 'Price']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(scraped_data_array)

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
from collections import defaultdict

# Import necessary libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from collections import defaultdict
from django.shortcuts import render
from requests.exceptions import RequestException


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
from collections import defaultdict






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
        csv_heading = ['Description', 'Product Price', 'Discount Price', 'Status', 'Condition']
        scrapped_list.append(csv_heading)

        for desc in description_arr:

            search_query = desc
            encoded_query = quote_plus(search_query)
            full_url = f"{base_url}?type=product&page=1&q={encoded_query}"

            response = requests.get(full_url)
            soup = BeautifulSoup(response.content, "html.parser")

            product_details = soup.find_all('div', class_='block-inner')
            product_infos = soup.find_all('div', class_='product-info')

            for product_detail in product_details:
                try:

                    scrapped_data = []

                    title_element = product_detail.find(class_="title")
                    if title_element:
                        title_text = title_element.get_text(strip=True)
                    else:
                        title_text = ''

                    price_element = product_detail.find(class_="amount")
                    if price_element is None:
                        price_element = product_detail.find(class_="price")
                        
                    if price_element:
                        price_text = price_element.get_text(strip=True)
                    else:
                        price_text = ''

                    condition_element = product_detail.find(class_='collection-listing__product-info__brand-new')
                    if condition_element:
                        condition_text = condition_element.get_text(strip=True)
                    else:
                        condition_text = ''

                    image_tag = product_detail.find(class_="image-label-wrap").find('img')
                    if image_tag:
                        image_src = image_tag['src']
                    else:
                        image_src = ''

                    print(title_text,image_src)

                    scrapped_data.append(title_text)
                    scrapped_data.append(price_text)
                    scrapped_data.append(condition_text)
                    scrapped_data.append(image_src)
                    scrapped_list.append(scrapped_data)

                except:

                    print("--- Products not Found ---")
                    continue

        for scrapped_data in scrapped_list[1:]:  # Skip the header row
            name = scrapped_data[0]
            price = scrapped_data[1]

            try:
                price = price.replace("$", "").replace(",", "")  # Remove dollar sign and commas
                price = float(price)
            except:
                price = 0.0

            if price > 0.0:

                condition = scrapped_data[2]
                image = scrapped_data[3]
                
                print(name,price,condition,"https:"+image)
                json_data = {
                    'product': {
                        'name': name,
                        'productType': 'physical',
                        'priceData': {
                            'price': price,
                        },
                        'condition': condition,
                    },
                }
                
                response = requests.post('https://www.wixapis.com/stores/v1/products', headers=headers, json=json_data)
                
                if response.status_code == 200:

                    response_data1 = response.json()
                    extracted_product_id1 = response_data1['product']['id']
                    json_data = {
                        'media': [
                            {
                                'mediaId': '19620272_1687322489998.jpg',
                            },
                            {
                                'url': "https:"+image,
                            },
                            {
                                'mediaId': '19620272_1687322489998',
                            },
                        ],
                    }
                    response11 = requests.post(
                        f'https://www.wixapis.com/stores/v1/products/{extracted_product_id1}/media',
                        headers=headers,
                        json=json_data,
                    )
                

                else:
                    print(f"Failed to add product '{name}'. Status code: {response.status_code}")
            else:
                print("Product not added to Wix due to zero price:", desc)

        csv_file_path = 'output_data.csv'  # Change to your desired CSV file path

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Image', 'Title', 'Price'])  # Write header row

            for scrapped_data in scrapped_list[1:]:  # Skip the header row
                image = scrapped_data[3]
                Condition = scrapped_data[2]
                title = scrapped_data[0]
                price = scrapped_data[1]
                writer.writerow([image, title, price,Condition])

        return render(request, 'maisondeluxe.html')
    
    return render(request, 'maisondeluxe.html')


  






def main_page(request):
    return render(request, 'index.html')
