import os
from KeywordBasedSearch.SearchEngines import *
from DS_CORE.DS_Config import *
from fake_user_agent import LATEST_CHROME_USERAGENT
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from googlesearch import search

from bs4 import BeautifulSoup

import pandas as pd
import re

SEARCH_ENGINE_RESULTS_SAVE_TO_PATH = os.path.join(OUTPUT_SAVING_PATH,'search_engines_results')

if not os.path.isdir(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH):
    os.makedirs(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH)

all_links = []

option = Options()
option.add_argument(f'-headless')
option.add_argument(f'user-agent={LATEST_CHROME_USERAGENT}')
option.add_argument(f'--proxy-server={TOR_PROXY}')

driver = Chrome(options=option)

def search_by_google(keywords):
    print(f'[+] Getting result for {keywords} from Google.')
    results = [result for result in search(keywords)]
    pd.DataFrame({'results':results}).to_csv(os.path.join(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH,f'{keywords}_google.csv'),index=False)
    print(f'[-] Fetched {len(results)} unique results fetch by Google')

def keywords_to_url_parameters(keywords):
    return keywords.replace(' ','+')

def set_max_scroll_size():
    #Maxmizing window size to scrollable content to take full screenshot !
    window_size = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    driver.set_window_size(window_size('Width'),window_size('Height'))

def search_by_ahmia(keywords):

    params = keywords_to_url_parameters(keywords)
    
    print(f'[+] Getting result for {keywords} from Ahmia.')

    driver.get(f'{DW_AHMIA_URL}{params}')

    set_max_scroll_size()

    result_links = driver.find_element(By.CLASS_NAME,'searchResults')

    a_titles = []
    a_links = []
    filtered_links = []

    a_tags = result_links.find_elements(By.TAG_NAME,'a')

    filter_patten = r'.*url=([\w:/.?=&+%-]*)'

    for a in a_tags:
        if a.get_attribute('href') not in a_links:
            a_links.append(a.get_attribute('href')) 
            filtered_links.append(re.findall(filter_patten,a_links[-1])[-1])
            a_titles.append(a.text)

    pd.DataFrame({'a_title':a_titles,'a_links':a_links,'filtered_links':filtered_links}).to_csv(os.path.join(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH,f'{keywords.replace("+","_")}_ahmia.csv'),index=False)
    print(f'[-] Fetched {len(a_links)} unique results fetch by Ahmia')

    return filtered_links
    
def search_by_duck_duck_go(keywords):

    params = keywords_to_url_parameters(keywords)

    print(f'[+] Getting result for {keywords} from DuckDuckgo.')

    driver.get(f'{DW_DUCK_DUCK_GO_URL}{params}')

    set_max_scroll_size()

    result_links = driver.find_element(By.ID,'links')

    a_tags = []
    a_titles = []
    a_links = []

    a_tags = result_links.find_elements(By.TAG_NAME,'a')

    if a_tags:
        #For Loading all the possible results !
        while 'javascript' in a_tags[-1].get_attribute('href'):
            print('[+] Please wait we are getting more results !')
            a_tags[-1].click()
            links = driver.find_element(By.ID,'links')
            a_tags = links.find_elements(By.TAG_NAME,'a')
 
            
    for a in a_tags:
        try:
            if a.get_attribute('href') not in a_links:
                a_links.append(a.get_attribute('href')) 
                a_titles.append(a.text)
        except:
            continue

    pd.DataFrame({'a_title':a_titles,'a_links':a_links}).to_csv(os.path.join(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH,f'{keywords.replace("+","_")}_duckduckgo.csv'),index=False)

    print(f'[-] Fetched {len(a_links)} unique results fetch by DuckDuckgo')

    return a_links
   
def search_by_deep_search(keywords):

    params = keywords_to_url_parameters(keywords)
    
    print(f'[+] Getting result for {keywords} from Deep Search.')

    driver.get(f'{DW_DEEP_SEARCH_URL}{params}')

    set_max_scroll_size()

    # result_links = driver.find_element(By.CLASS_NAME,'title')

    a_titles =[]
    a_links = []
    filtered_links = []

    a_tags = driver.find_elements(By.CLASS_NAME,'title')

    filter_patten = r'.*url=([\w:/.?=&+%-]*)'

    for a in a_tags:
        if a.get_attribute("href") not in a_links:
            a_links.append(a.get_attribute("href")) 
            a_titles.append(a.text)
            filtered_links.append(re.findall(filter_patten,a_links[-1])[-1])
            
    pd.DataFrame({'a_title':a_titles,'a_links':a_links,'filtered_links':filtered_links}).to_csv(os.path.join(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH,f'{keywords.replace("+","_")}_deep_search.csv'),index=False)
    print(f'[-] Fetched {len(a_links)} unique results fetch by Deep Search')
    
    return filtered_links

def search_by_tor66(keywords):

    params = keywords_to_url_parameters(keywords)
    
    print(f'[+] Getting result for {keywords} from Tor66.')

    driver.get(f'{DW_TOR66_URL}{params}')

    set_max_scroll_size()

    page_htmls = [driver.page_source]

    while '>>>' in driver.find_element(By.CLASS_NAME,'pagination').find_elements(By.TAG_NAME,'a')[-1].text:
        try:
            page_number = driver.current_url[int(driver.current_url.index('page=')+5):] if 'page=' in driver.current_url else 1
            print(f'[+] Fetching more links from {page_number} page.')
            driver.find_element(By.CLASS_NAME,'pagination').find_elements(By.TAG_NAME,'a')[-1].click() # Clicking >>> for visiting next page
            page_htmls.append(driver.page_source)
        except NoSuchElementException:
            continue
        except KeyboardInterrupt:
            print('[+] Stopping to fetch further more results.')
            break

    a_tags = []
    a_titles =[]
    a_links = []

    for html in page_htmls:

        soup = BeautifulSoup(html,'lxml')
 
        b_tags = soup.find_all('b')
  
        for b in b_tags:
                try:
                    if b.find('a'):
                        a = b.find('a')
                        a_links.append(a["href"]) 
                        a_titles.append(a.get_text())
                except:
                    continue
            
    pd.DataFrame({'a_title':a_titles,'a_links':a_links}).to_csv(os.path.join(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH,f'{keywords.replace("+","_")}_tor66.csv'),index=False)
    print(f'[-] Fetched {len(a_links)} unique results fetch by Tor66')
    
    return a_links

def search_by_torgle(keywords):

    params = keywords_to_url_parameters(keywords)
    
    print(f'[+] Getting result for {keywords} from Torgle.')

    driver.get(f'{DW_TORGLE_URL}{params}')

    set_max_scroll_size()

    page_htmls = [driver.page_source]

    # if current page number == total pages it breaks of from while loop ! 
    # while driver.find_element(By.XPATH,'/html/body/center[3]/div/span/strong').text not in driver.find_element(By.XPATH,'/html/body/center[9]/div/span/text()[2]').text:
    #     try:
    #         page_number = driver.find_element(By.XPATH,'/html/body/center[3]/div/span/strong').text
    #         print(f'[+] Fetching more links from {page_number} page.')
    #         driver.find_element(By.XPATH,'/html/body/center[9]/div/a[3]').click() # Clicking next_page>> for visiting next page
    #         page_htmls.append(driver.page_source)
    #     except NoSuchElementException:
    #         continue
    #     except KeyboardInterrupt:
    #         print('[+] Stopping to fetch further more results.')
    #         break

    a_tags = []
    a_titles =[]
    a_links = []

    for html in page_htmls:

        soup = BeautifulSoup(html,'lxml')
 
        table_results = soup.find_all('table')
  
        for table in table_results:
                try:
                    if table.find('a') and len(table.find_all('b')) > 1:
                        a = table.find('a')
                        a_title = table.find_all('b')[0].get_text().strip()
                        a_links.append(a["href"]) 
                        a_titles.append(a_title)
                except:
                    continue
            
    pd.DataFrame({'a_title':a_titles,'a_links':a_links}).to_csv(os.path.join(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH, f'{keywords.replace("+","_")}_torgle.csv'),index=False)
    print(f'[-] Fetched {len(a_links)} unique results fetch by Torgle')
    
    return a_links

Keyword = input('Enter keywords for searching : ')

def safe_search(search_engine,Keyword):

    global all_links

    try:
        links = search_engine(Keyword)

        if links:
            all_links += links

    except Exception as e:
        print(f'[-] Something went wrong on {e} for {search_engine.__name__}')

def DW_all_search(Keyword):

    global all_links
    
    safe_search(search_engine=search_by_tor66,Keyword=Keyword)

    safe_search(search_engine=search_by_deep_search,Keyword=Keyword)

    safe_search(search_engine=search_by_ahmia,Keyword=Keyword)

    safe_search(search_engine=search_by_torgle,Keyword=Keyword)

    safe_search(search_engine=search_by_deep_search,Keyword=Keyword)

    unique_links = []

    for link in all_links:
        if link not in unique_links:
            unique_links.append(link)

    unique_links = [link+'\n' for link in unique_links]

    with open(os.path.join(SEARCH_ENGINE_RESULTS_SAVE_TO_PATH,f'all_links_for_{Keyword}.txt'),'w') as f:
        f.writelines(unique_links)
    
DW_all_search(Keyword)
driver.quit()
