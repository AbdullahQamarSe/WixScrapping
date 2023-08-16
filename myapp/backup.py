from django.shortcuts import render
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
    # ---- Reading the description of products ------
    # file = open('description.csv')
    # type(file)
    # csvreader = csv.reader(file)
    # ------ Opening the url ---------
    driver.execute_script('''window.open("https://www.fashionphile.com/");''')
    # ------ Switching to the opened website ------
    # Get all window handles
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
        print('Product --->>',row[0])
        desc = row[0]
        while 1:
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="search-input"]')))               
            search_bar = driver.find_element(By.XPATH,'//*[@id="search-input"]')
            try:
                # ---- Removing text from search field
                driver.find_element(By.XPATH,'//*[@id="__next"]/header/div/div[2]/div[2]/div/div[2]/div/div/div/div/span[1]/div/button/div').click()
            except:
                pass
            search_bar.send_keys(desc)
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="__next"]/header/div/div[2]/div[2]/div/div[2]/div/div/div/div/span[2]/button').click()
            time.sleep(1)
            driver.find_element(By.XPATH,'//*[@id="__next"]/header/div/div[2]/div[2]/div/div[2]/div/div/div/div/span[2]/button').click()
            time.sleep(3)
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
        description_arr=[]
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('iso-8859-1').splitlines()
        reader = csv.reader(decoded_file)
        for row in reader:
            print('Product --->>',row[0])
            description_arr.append(row)
        file_path = ''
        while 1:
            try:
                print('function calling')
                file_path = main(description_arr) 
                break
            except Exception as e:
                print('<------ Access Denied ------>',e)
                time.sleep(10)
          
        return render(request, 'fashionphile.html',context={'csv_file':file_path})
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

def search_rebag(search_query, driver):
    search_query = search_query.replace(',',' ')
    print('--- Search Function ---', search_query)
    
    driver.get("https://shop.rebag.com/search?")
    #search
    time.sleep(10)
    body_element = driver.find_element(By.TAG_NAME, 'body')
    body_element.click()
    time.sleep(5)
    close_modal_dialog(driver)
    # time.sleep(10) 
    while 1:
        try:   
            time.sleep(10)
            # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/div/div/div[2]/div/div/div[1]/div/form/div/input')))
            try:
                input_element = driver.find_element(By.XPATH, '/html/body/header/div/div/div[2]/div/div/div[1]/div/form/div/input')
            except:
                input_element = driver.find_element(By.CSS_SELECTOR, '[placeholder="Try searching \\"Louis Vuitton\\" or \\"Black Tote\\""]')

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
    random_number = random.randint(1, 10000)
    file_path = f'static/firstdibs{random_number}.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write each row of data to the CSV file
        for row in scraped_list:
            try:
                writer.writerow(row)
            except:
                print(row)
    return file_path

def save_to_csv_madison(scraped_list):
    # Open CSV file for writing
    random_number = random.randint(1, 10000)
    file_path = f'static/madison{random_number}.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write each row of data to the CSV file
        for row in scraped_list:
            try:
                writer.writerow(row)
            except:
                print(row)
    return file_path

def save_to_csv_rebag(scraped_list):
    # Open CSV file for writing
    random_number = random.randint(1, 10000)
    file_path = f'static/rebag{random_number}.csv'
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write each row of data to the CSV file
        for row in scraped_list:
            try:
                writer.writerow(row)
            except:
                print(row)
    return file_path

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
    scraped_data_list=[]
    csv_haeding = ['Description', 'Price', 'Condition']
    scraped_data_list.append(csv_haeding)
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
            save_to_csv_rebag(scraped_data_list)
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

def read_search_queries(csv_content):
    # Parse the CSV content
    concatenated_rows =[]
    reader = csv.DictReader(csv_content.splitlines())
    # Skip the header row
    next(reader)
    for row in reader:
        item = row.get('Item')
        color = row.get('Color')
        size = row.get('Size')
        leather = row.get('Leather')
        if item or color or size or leather:
            concatenated_row = ','.join([item, color, size, leather])
            concatenated_rows.append(concatenated_row)
        
    # Display the concatenated column
    # for value in concatenated_rows:
    #     print(value)
    return concatenated_rows


    
def madison(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr=[]
        csv_file = request.FILES['csv_file']
        csv_content = csv_file.read().decode('iso-8859-1')
        description_arr=read_search_queries(csv_content)
        # reader = csv.reader(decoded_file)
        for row in description_arr:
            print('Product --->>',row)
        file_path = ''
        while 1:
            try:
                chrome_options = uc.ChromeOptions()
                
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),  options=chrome_options)
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
        description_arr=[]
        csv_file = request.FILES['csv_file']
        csv_content = csv_file.read().decode('iso-8859-1')  # Adjust the decoding if necessary
        description_arr=read_search_queries(csv_content)
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
                file_path = start_process_rebag(description_arr, driver)

                driver.quit()
                print('File Path',file_path)
                file_path = "/" + file_path
                break
            except Exception as e:
                print('<------ Access Denied ------>',e)
                driver.quit()
                time.sleep(10)
          
        return render(request, 'rebag.html',context={'csv_file':file_path})
    return render(request, 'rebag.html')

    
def firstdibs(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr=[]
        csv_file = request.FILES['csv_file']
        csv_content = csv_file.read().decode('iso-8859-1')  # Adjust the decoding if necessary
        description_arr=read_search_queries(csv_content)
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
import requests
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def add_product_to_wix(product_data):
    # Replace <AUTH_TOKEN> and <SITE_ID> with the actual authorization token and site ID
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjNhMzBjODhjLWVlMmQtNDc4NS04MmZhLTIzN2Q3ZWZlYjcwMlwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcIjA0YjczNjllLTZkYzEtNDllNC1hNGQ1LTY5ZTljZDFmMjYyMVwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCJhZTUyOWYyZC0yYzI0LTRhNDUtYWE2MC01NTY1NDljNWExMDRcIn19IiwiaWF0IjoxNjg5MjEzODg3fQ.EOozDYwOAMTwHeByFEbu8h860-9WL47su2spEy1Cfg_xb7j-lYa5ldDiWVD5GHJE5axpq2L0SVH2uJbEHF6HE6svsDSrlh1g13PraqVYwpQLr0sgksMHWWYE_vWdQruwI0b9IrnBZCCu8ULV0hHs4UTfNfigdyZ18TSZSx6oBWuIPKAAoXWLttuvpV1AJqxlsC1mQI3ArUPwo71znAoWecnVPNiR1RgMZph0_wpkbn6hCGUxiT30Azho_ZESOEJGUg9juhsc5BauBzDDXjDslgYiiLhYQ9Hq6bPRVtaTGQqL6MxdJy129mIjqvW-I9xsTC3lNBMWPJBbviUDnjCncw',  # Replace <AUTH_TOKEN> with the actual authorization token
    'wix-site-id': 'c04db714-1e86-449e-811f-87e75c66dae5',  # Replace with the actual site ID
    }

    response = requests.post('https://www.wixapis.com/stores/v1/products', headers=headers, json=product_data)
    return response.status_code, response.json()

def search_and_add_to_wix(key_word, driver):
    print('--- Search and Add Function ---', key_word)
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
            if len(details_list) >= 4:
                description = details_list[0]

                # Try converting the current price to float, handle "Opens in a new window or tab" case
                try:
                    current_price = float(details_list[1].replace('$', '').replace(',', ''))
                except ValueError:
                    current_price = None

                before_discount = details_list[2]
                condition = details_list[3]

            # Prepare the product data to add to Wix only if current_price is a valid float
            if current_price is not None:
                product_data = {
                    'product': {
                        'name': description,
                        'productType': 'physical',
                        'priceData': {
                            'price': current_price,
                        },
                        'description': description,
                        'visible': False,
                    }
                }

                # Add the product to Wix
                status_code, response_json = add_product_to_wix(product_data)
                print(f"Status Code: {status_code}, Response: {response_json}")

    except Exception as e:
        print("Error while collecting data:", e)


def ebay(request):
    if request.method == 'POST':
        print('POST Request')

        # Make a POST request to fetch the products from Wix API
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': 'IST.eyJraWQiOiJQb3pIX2FDMiIsImFsZyI6IlJTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjNhMzBjODhjLWVlMmQtNDc4NS04MmZhLTIzN2Q3ZWZlYjcwMlwiLFwiaWRlbnRpdHlcIjp7XCJ0eXBlXCI6XCJhcHBsaWNhdGlvblwiLFwiaWRcIjpcIjA0YjczNjllLTZkYzEtNDllNC1hNGQ1LTY5ZTljZDFmMjYyMVwifSxcInRlbmFudFwiOntcInR5cGVcIjpcImFjY291bnRcIixcImlkXCI6XCJhZTUyOWYyZC0yYzI0LTRhNDUtYWE2MC01NTY1NDljNWExMDRcIn19IiwiaWF0IjoxNjg5MjEzODg3fQ.EOozDYwOAMTwHeByFEbu8h860-9WL47su2spEy1Cfg_xb7j-lYa5ldDiWVD5GHJE5axpq2L0SVH2uJbEHF6HE6svsDSrlh1g13PraqVYwpQLr0sgksMHWWYE_vWdQruwI0b9IrnBZCCu8ULV0hHs4UTfNfigdyZ18TSZSx6oBWuIPKAAoXWLttuvpV1AJqxlsC1mQI3ArUPwo71znAoWecnVPNiR1RgMZph0_wpkbn6hCGUxiT30Azho_ZESOEJGUg9juhsc5BauBzDDXjDslgYiiLhYQ9Hq6bPRVtaTGQqL6MxdJy129mIjqvW-I9xsTC3lNBMWPJBbviUDnjCncw',  # Replace <AUTH_TOKEN> with the actual authorization token
            'wix-site-id': 'c04db714-1e86-449e-811f-87e75c66dae5',  # Replace with the actual site ID
        }

        response = requests.post('https://www.wixapis.com/stores/v1/products/query', headers=headers)

        if response.status_code == 200:
            data = response.json()
            products = data['products']

            # Function to perform the search and add products to Wix
            def process_search_and_add(key_word):
                try:
                    # Replace <CHROME_DRIVER_PATH> with the actual path to the downloaded ChromeDriver executable
                    chrome_options = webdriver.ChromeOptions()
                    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

                    driver.maximize_window()
                    time.sleep(5)
                    search_and_add_to_wix(key_word, driver)
                    driver.quit()
                except Exception as e:
                    print('<------ Access Denied ------>', e)
                    driver.quit()
                    time.sleep(10)

            # Create a list to store the threads
            threads = []

            # List of search keywords to be used in concurrent searches
            search_keywords = [product['name'] for product in products]

            # Start the threads for parallel searches
            for keyword in search_keywords:
                thread = threading.Thread(target=process_search_and_add, args=(keyword,))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            return render(request, 'ebay.html')

        else:
            # Handle the error when Wix API call fails
            print(f"Error: {response.status_code} - {response.text}")
            return render(request, 'error.html', context={'error_message': 'Wix API call failed'})

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



def maisondeluxe(request):
    if request.method == 'POST':
        print('POST Request')
        description_arr=[]
        # Define the base URL
        base_url = "https://www.maisondeluxeonline.com/search"
        # csv_file = request.FILES['csv_file']
        # decoded_file = csv_file.read().decode('iso-8859-1').splitlines()
        # reader = csv.reader(decoded_file)
        # for row in reader:
        #     print('Product --->>',row[0])
        #     description_arr.append(row)
        csv_file = request.FILES['csv_file']
        csv_content = csv_file.read().decode('iso-8859-1')  # Adjust the decoding if necessary
        description_arr=read_search_queries(csv_content)
        for row in description_arr:
            print('Product --->>',row)
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
        random_number = random.randint(1, 10000)
        file_path = f'static/maisondeluxe{random_number}.csv'
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write each row of data to the CSV file
            for row in scrapped_list:
                writer.writerow(row)
        
        
        
        file_path1 = "/" + file_path
        
          
        return render(request, 'maisondeluxe.html',context={'csv_file':file_path1})
    
    return render(request, 'maisondeluxe.html')

############################ Main Home Page

def main_page(request):
    return render(request, 'index.html')