from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

URL = 'https://start.me/p/b56G5Q/search-engines'

options = Options()
options.add_argument('-headless')

d = Chrome(options=options)

d.get(URL)

#Maxmizing window size to scrollable content to take full screenshot !
window_size = lambda X: d.execute_script('return document.body.parentNode.scroll'+X)
d.set_window_size(window_size('Width'),window_size('Height'))

d.implicitly_wait(30)

articles = d.find_elements(By.TAG_NAME,'h2')

print(len(articles))

for h2 in d.find_elements(By.TAG_NAME,'h2'):
    print(h2.text)
    with open('source_title.txt','a') as f:
        f.write(h2.text+'\n')

d.quit()