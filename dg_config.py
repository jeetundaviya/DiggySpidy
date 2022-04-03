#Colors codes defined for logo
BLUE, RED, WHITE, YELLOW, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[32m', '\033[0m'

#Tor socks5 proxy
TOR_PROXY = "socks5://127.0.0.1:9050"

#Important URLs
CHECK_TOR_URL = 'http://check.torproject.org'
FETCH_IP_DETAILS_URL = 'http://ip-api.com/json'
URL_FOR_CHECKING_INTERNET_CONNECTIVITY = 'example.com'

# RE Pattens
URL_DOMAIN_PATTEN = r'://([\w.]*)'

#Verbose Mode
TABLE_ROW_NUMBER = 25

# Crawling options
'''Crawler should or should not stay in same domain while crawling.'''
CRAWL_IN_DOMAIN = False

'''CRAWL_DEPTH decides much deeper you wish to crawl for seed website should it crawl.'''
CRAWL_DEPTH = 3

'''After crawling MAX_CRAWL_COUNT count it should stop crawling and exit.'''
MAX_CRAWL_COUNT = 10000

'''MAX_THREAD_COUNT parallel scrapping websites.'''
MAX_THREAD_COUNT = 10

#Scraping options
'''
Use fake user-agent by calling get_random_fake_user_agent() from fake_user_agent.py .

It will randomly choose fake User-Agent before every new request and then copy it in header before sending get request.
'''

USE_FAKE_USER_AGENT = True

'''For MAX_RESPONSE_TIME seconds it should wait for website to load or respond.'''
MAX_RESPONSE_TIME = 5

'''It will start crawling every new website after SCRAPE_PAUSE_AFTER_EVERY_URL seconds.'''
SCRAPE_PAUSE_AFTER_EVERY_URL = 0

#Output folder
'''At OUTPUT_SAVING_PATH location the scrapped files will be saved.'''
OUTPUT_SAVING_PATH = 'saved_data'

#Wordlist file locations
'''STOPWORDS_IN_LINK_FILE contains words which you don't want in your scraped links for further scraping.'''
STOPWORDS_IN_LINK_FILE = './Wordlist/stopwords_in_link_file.txt'

'''MUST_HAVE_WORDS_IN_LINK_FILE contains words which you want in your scraped links for further scraping.'''
MUST_HAVE_WORDS_IN_LINK_FILE = './Wordlist/must_have_words_in_link_file.txt'

'''MUST_HAVE_WORDS_IN_WEBSITE_TEXT_FILE contains words which you want in website visable text for further scraping.'''
MUST_HAVE_WORDS_IN_WEBSITE_TEXT_FILE = './Wordlist/must_have_words_in_website_text_file.txt'

#How to enable TOR Controller Port.

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

# If TOR Controller Port is enabled !

'''Enter your TOR control port password here !'''
CONTROL_PORT_PASSWORD = 'p@5s30R6' 

'''Change IP after every CHANGE_IP_AFTER_SCRAPPING_NUMBER_OF_WEBSITES of scrapped websites.'''
CHANGE_IP_AFTER_SCRAPPING_NUMBER_OF_WEBSITES = 25

'''Change IP after every CHANGE_IP_AFTER_MINUTES of minutes.'''
CHANGE_IP_AFTER_MINUTES = 5
