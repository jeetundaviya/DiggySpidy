import os
import joblib
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
#Colors codes defined for logo
BLUE, RED, WHITE, YELLOW, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[32m', '\033[0m'

#region Chrome and ChromeDriver Path

if os.name == 'nt':
    CHROME_BINARY_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    CHROME_DRIVER_PATH = os.path.join('DS_CORE',os.path.join("Required_Binaries","win_chromedriver.exe"))
else:
    CHROME_BINARY_PATH = "/usr/bin/google-chrome"
    CHROME_DRIVER_PATH = os.path.join('DS_CORE',os.path.join("Required_Binaries","linux_chromedriver"))
#endregion

#region Proxy Configuration
PROXY_TYPE = 'socks5'
PROXY_IP = '127.0.0.1'
PROXY_PORT = '9050'
#Tor socks5 proxy
TOR_PROXY = f"{PROXY_TYPE}://{PROXY_IP}:{PROXY_PORT}"
#endregion

#region Important URLs
CHECK_TOR_URL = 'http://check.torproject.org'
FETCH_IP_DETAILS_URL = 'http://ip-api.com/json'
URL_FOR_CHECKING_INTERNET_CONNECTIVITY = 'example.com'
#endregion

#region RE Pattens
URL_DOMAIN_PATTEN = r'://([\w.]*)'
#endregion

#region Verbose Mode Configuration
TABLE_ROW_NUMBER = 25
#endregion

#region Crawling options
'''Crawler should or should not stay in same domain while crawling.'''
CRAWL_IN_DOMAIN = False

'''CRAWL_DEPTH decides much deeper you wish to crawl for seed website should it crawl.'''
CRAWL_DEPTH = 3

'''After crawling MAX_CRAWL_COUNT count it should stop crawling and exit.'''
MAX_CRAWL_COUNT = 10000

'''MAX_THREAD_COUNT parallel scrapping websites.'''
MAX_THREAD_COUNT = 30
#endregion

#region Scraping options
'''
Use fake user-agent by calling get_random_fake_user_agent() from fake_user_agent.py .

It will randomly choose fake User-Agent before every new request and then copy it in header before sending get request.
'''

USE_FAKE_USER_AGENT = True

'''For MAX_RESPONSE_TIME seconds it should wait for website to load or respond.'''
MAX_RESPONSE_TIME = 5

'''It will start crawling every new website after SCRAPE_PAUSE_AFTER_EVERY_URL seconds.'''
SCRAPE_PAUSE_AFTER_EVERY_URL = 0
#endregion

#region Slow Mode Configuration
KEYWORD_PROOF_REQUIRED = False
#endregion

#region Output folder
'''At OUTPUT_SAVING_PATH location the scrapped files will be saved.'''
OUTPUT_SAVING_PATH = os.path.join(os.path.join("DS_CORE",'saved_data'))
#endregion

#region File locations
'''STOPWORDS_IN_LINK_FILE contains words which you don't want in your scraped links for further scraping.'''
STOPWORDS_IN_LINK_FILE = os.path.join('DS_CORE',os.path.join('Wordlist','stopwords_in_link_file.txt'))

'''MUST_HAVE_WORDS_IN_LINK_FILE contains words which you want in your scraped links for further scraping.'''
MUST_HAVE_WORDS_IN_LINK_FILE = os.path.join('DS_CORE',os.path.join('Wordlist','must_have_words_in_link_file.txt'))

'''MUST_HAVE_WORDS_IN_WEBSITE_TEXT_FILE contains words which you want in website visable text for further scraping.'''
MUST_HAVE_WORDS_IN_WEBSITE_TEXT_FILE = os.path.join('DS_CORE',os.path.join('Wordlist','must_have_words_in_website_text_file.txt'))

'''FAKE_USERAGENT_LIST_FILE conatains bunch of the supported user-agents of diffrent browsers by which we cna fake the identity'''
FAKE_USERAGENT_LIST_FILE = os.path.join(os.path.join("DS_CORE",'UserAgentList'),'fake_user_agent_list.txt')
#endregion

#region How to enable TOR Controller Port.

#----------------------------------------------[CONTROL PORT CONFIGRATION STEPS AND ITS BASED FEATURES]------------------------------------------
'''

This functionality of changing ip using contoller will only work if you have configured your torrc file !

[+] Configuration Steps !

0. Please turn OFF your tor sevice. (ONLY IF STARTED !)
[FOR LINUX] command :- sudo service tor stop
[FOR WINDOWS] Find tor.exe from your Task Manager and End Task it. 

1. Make hash-password for your password you want using follow command !
command :- tor --hash-password yourpassword (Don't forget to replace 'yourpassword' with your desired password !)
output :- 16:45FB27EED43E230E60BB9D1F5D47ECD26B11778226C9BE4C6C038D06B4 (Your output might be different !)

2. Copy this hash-password (16:45FB...D06B4) to your clipboard or save somewhere.

3. Open your torrc file.

Default location for torrc file  :-

[PATH FOR LINUX] /etc/tor/torrc
[PATH FOR WINDOWS]  [installation directory]/Browser/TorBrowser/Data/Tor 

4. Edit torrc file.

Find the following lines in torrc file :-

<Some commented text>
#ControlPort 9051
<Some commented text>
#HashedControlPassword 16:6BE02981163AFB9660DD5E15609A7D5DE979D1DBF9A1044F7112A77CF4
<Some commented text>

Now just uncomment this 2 lines and replace hash-password with your generated hash-password.

Afterwards it should be looking like :- 

<Some commented text>
ControlPort 9051
<Some commented text>
HashedControlPassword 16:45FB27EED43E230E60BB9D1F5D47ECD26B11778226C9BE4C6C038D06B4 (Don't forget to change it your own gernerated hash-password.)
<Some commented text>

Now save file and exit.

5. Now start tor service and fire-up tor and check logs in terminal.

Once you see the following text in logs :-

<Some more logs>
Jan 26 14:01:28.402 [notice] Opening Control listener on 127.0.0.1:9051
Jan 26 14:01:28.402 [notice] Opened Control listener connection (ready) on 127.0.0.1:9051
<Some more logs>

Hurray ! you have successfully configured your tor with control port !

'''
#endregion

#region TOR Controller Port Configuration (if enabled)

'''Enter your TOR control port password here !'''
CONTROL_PORT_PASSWORD = 'p@5s30R6' 

'''Change IP after every CHANGE_IP_AFTER_SCRAPPING_NUMBER_OF_WEBSITES of scrapped websites.'''
CHANGE_IP_AFTER_SCRAPPING_NUMBER_OF_WEBSITES = 25

'''Change IP after every CHANGE_IP_AFTER_MINUTES of minutes.'''
CHANGE_IP_AFTER_MINUTES = 5
#endregion

#Loading Website Category Detection Model
WEBSITE_CATEGORY_MODEL = joblib.load(os.path.join(os.path.join("DS_CORE",'NLP'),'website_category_detection_model.joblib'))
