from dataclasses import field
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_user_agent import *
from dg_config import *
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import os

FRESH_ONIONS_RESULTS_SAVE_TO_PATH = os.path.join(OUTPUT_SAVING_PATH,'fresh_onions_results')

if not os.path.isdir(FRESH_ONIONS_RESULTS_SAVE_TO_PATH):
    os.makedirs(FRESH_ONIONS_RESULTS_SAVE_TO_PATH)

URL = 'http://freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion/'
URL_WITH_QUERY = 'http://freshonifyfe4rmuh6qwpsexfhdrww7wnt5qmkoertwxmcuvm4woo4ad.onion/?query='

def parse_table(page_source):

    global pt

    soup  = BeautifulSoup(d.page_source,'lxml')

    table_trs = soup.find_all('tr')

    for tr in table_trs[1:]:    
        status = tr.attrs['class'][0]
        url,title,added,last_check = tr.find_all('td')
        pt.add_row([url.text,title.text,added.text,last_check.text,status])

options = Options()
options.add_argument('-headless')
options.add_argument(f'user-agent={LATEST_CHROME_USERAGENT}')
options.add_argument(f'--proxy-server={TOR_PROXY}')

d = Chrome(options=options)

d.get(URL)

flds = [th.text for th in d.find_elements(By.TAG_NAME,'th')]
flds.append('Status')

pt = PrettyTable(field_names=flds)

pages = d.find_element(By.CLASS_NAME,'pageslct').find_elements(By.TAG_NAME,'a')
pages = [page.get_attribute('href') for page in pages]
print(pages)

parse_table(d.page_source)

for page in pages[1:]:
    d.get(URL)
    parse_table(d.page_source)
    
    print(f'[+] {len(pt.rows)}')

d.quit()

# print(pt.get_csv_string())

with open(os.path.join(FRESH_ONIONS_RESULTS_SAVE_TO_PATH,'fresh_onions.csv'),'w') as f:
    f.write(pt.get_csv_string())