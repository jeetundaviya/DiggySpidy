#region  DiggySpidy Imports
from DS_CORE.DS_Config import *
from DS_CORE.fake_user_agent import FakeUserAgent
# from DS_Core.keyword_box_in_image import KeywordBox
#endregion

#region DS_APIs Imports
import sys
import os
from DS_CORE.models import *
#endregion

#region Generic and 3rd Party Libraries Imports
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
import base64
import json
import os
import re
import socket
import subprocess
import sys
import threading
import time
from argparse import ArgumentParser
from threading import Thread
from urllib.parse import urljoin
import pandas as pd
import requests as req
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from stem import Signal
from stem.control import Controller
from tqdm import tqdm

#endregion

def is_connected_to_internet():
	try:
		s = socket.create_connection((URL_FOR_CHECKING_INTERNET_CONNECTIVITY, 80), 2)
		s.close()
		return True
	except Exception as e:
		print(f'[-] Unable to connect to internet due to {e} !\n[-] Please check your internet connection !')
		return False

def clear_screen():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')

def print_small_logo():
	sys.stdout.write(RED +'''
    █▀▄ █ █▀▀ █▀▀ █▄█   █▀ █▀█ █ █▀▄ █▄█
    █▄▀ █ █▄█ █▄█ ░█░   ▄█ █▀▀ █ █▄▀ ░█░ v2.0'''+ END+'\n\n')

def print_logo():
	clear_screen()

	sys.stdout.write(RED +'''
		
  ██████╗░██╗░██████╗░░██████╗░██╗░░░██╗  ░██████╗██████╗░██╗██████╗░██╗░░░██╗
  ██╔══██╗██║██╔════╝░██╔════╝░╚██╗░██╔╝  ██╔════╝██╔══██╗██║██╔══██╗╚██╗░██╔╝
  ██║░░██║██║██║░░██╗░██║░░██╗░░╚████╔╝░  ╚█████╗░██████╔╝██║██║░░██║░╚████╔╝░
  ██║░░██║██║██║░░╚██╗██║░░╚██╗░░╚██╔╝░░  ░╚═══██╗██╔═══╝░██║██║░░██║░░╚██╔╝░░
  ██████╔╝██║╚██████╔╝╚██████╔╝░░░██║░░░  ██████╔╝██║░░░░░██║██████╔╝░░░██║░░░
  ╚═════╝░╚═╝░╚═════╝░░╚═════╝░░░░╚═╝░░░  ╚═════╝░╚═╝░░░░░╚═╝╚═════╝░░░░╚═╝░░░ v2.0
	'''+ END + BLUE +

             '\n' + '{}Surface and Dark Web Crawler tool ({}Diggy Spidy{}){}'.format(YELLOW, RED, YELLOW,
                                                                                        BLUE).center(100) +
             '\n' + 'Made with {}<3{} by: Jeet Undaviya ({}0.<{}) and Dhaiwat Mehta ({}1.<{}) {}'.format(RED,YELLOW, RED, YELLOW,RED, YELLOW, BLUE).center(115) +
             '\n' + 'Version: {}2.0{}'.format(YELLOW, END).center(85)+
             '\n\n' + 'Type python diggy_spidy.py -h or --help for help'.format(YELLOW, END).center(80) + '\n\n')

def get_list_from_file(file):
		with open(file,'r') as f:
			return [link.replace('\n','') for link in f.readlines() if len(link) > 1]

class DiggySpidy:

	def get_driver(self):
		try:
			self.driver_options = webdriver.ChromeOptions()

			if self.must_torrify:
				if self.is_tor_connected():
					self.driver_options.add_argument(f'--proxy-server={TOR_PROXY}')
			
			# Opening Chrome in Headless mode (in background)
			self.driver_options.add_argument('--headless')
			self.driver_options.add_argument('--no-sandbox')
			
			# Disabling the logging from chrome-driver
			self.driver_options.add_experimental_option('excludeSwitches', ['enable-logging'])

			self.driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH),options=self.driver_options)
			
			self.driver.maximize_window() # Maximizing window by default
			print('[+] Successfully got access to driver')
			return self.driver
		except Exception as ex:
			print(f'[-] Failed to get the driver due to {ex}')

	def load_url_in_driver(self,url,current_url_model):
		try:
			# self.driver.quit()
			print(f'[+] Trying to render {url} in driver')
			if self.use_random_fake_user_agent:
				self.driver_options.add_argument(f'user-agent={self.fake_user_agent.get_random_fake_user_agent()}')

			self.get_driver()

			if 'http' not in url:
				url='http://'+url

			self.driver.implicitly_wait(self.max_response_time) #It will at max wait for 30 seconds for loading website.
			
			self.driver.delete_all_cookies()

			self.driver.get(f'{url}')

			self.capture_screenshot(current_url_model)
			print(f'[+] Successfully renered {url} in driver')
			return self.driver.page_source
		except Exception as ex:
			print(f'[-] Failed to load the {url} in driver due to {ex}')

	def capture_screenshot(self,current_url_model):

		current_url_model.screenshot = self.driver.get_screenshot_as_png()

		#Maxmizing window size to scrollable content to take full screenshot !
		window_size = lambda X: self.driver.execute_script('return document.body.parentNode.scroll'+X)
		self.driver.set_window_size(window_size('Width'),window_size('Height'))
		current_url_model.full_screenshot = self.driver.get_screenshot_as_png()

		current_url_model.page_pdf = base64.b64decode(self.driver.print_page()) # This b64 encoded string so when you use it decode it with b64 and then save it to .pdf file. 

		current_url_model.save()

		#Reseting to max screen size window .
		self.driver.maximize_window()
	
	def exit_driver(self):
		#Exiting
		self.driver.quit()

	# This function can only work if Control Port is open at port 9051 by tor
	def change_tor_exit_node(self):
		try:
			with Controller.from_port(port=9051) as controller:
				controller.authenticate(password=self.controller_port_password)
				controller.signal(Signal.NEWNYM)

			# Fetching new  Tor end-point connected proxy Connection details
			self.session = req.session()
			self.session.proxies = self.tor_proxy
			
			print(f'[+] Success in getting new tor end-node !')
			tor_ip_res = self.session.get('http://ip-api.com/json')

			if tor_ip_res.status_code ==200: 
				print('[+] Your Tor exit node\'s IP location. \n')
				tor_json_data = json.loads(tor_ip_res.text)
				self.print_ip_desc_table(tor_json_data)
	       
		except Exception as e:
			# Recheck your tor auth password for controller and re-try again !
			print('[!] Failed to get new tor end-node !')
			
	def print_ip_desc_table(self):
		
		your_ip_res = self.session.get(FETCH_IP_DETAILS_URL)

		if your_ip_res.status_code ==200: 
			your_ip_json_data = json.loads(your_ip_res.text)
			if your_ip_json_data['status'] == 'success':
				ip_detail_table = PrettyTable(header=True,
				field_names=['IP','Country','Region','City','Latitude','Longitude','Timezone','ISP','ORG','AS Number'])
				ip_detail_table.add_row([
					your_ip_json_data['query'],
					your_ip_json_data['country'],
					your_ip_json_data['regionName'],
					your_ip_json_data['city'],
					your_ip_json_data['lat'],
					your_ip_json_data['lon'],
					your_ip_json_data['timezone'],
					your_ip_json_data['isp'],
					your_ip_json_data['org'],
					your_ip_json_data['as']])
				print(ip_detail_table,end='\n\n')
			else:
				print('[-] Sorry, we are not able to fetch your IP details.\n')
		else:
			print('[-] Sorry, we are not able to recive response!\n')

	def is_tor_connected(self):
		if self.must_torrify:
			try:
				res = req.get(CHECK_TOR_URL,proxies=self.tor_proxy)

				if res.status_code == 200:
					if 'Sorry. You are not using Tor.'.lower() not in res.text.lower():
						print('[+] Successfully connected to tor !\n')
						return True
					else:
						print('[-] Sorry, you are not using tor. !\n')
						# wish = str(input('[?] Do you wish to scrap web without tor ? [y/n]')).lower()[0]
						# if wish == 'y':
						# 	return False #Returning true just to allow scraping without tor.
						# else:
						# 	print('[-] Exiting ... ')
						# 	exit(0)
			except Exception as e:
				print(f'[-] Failed to verify tor status due to {e} !\n')
				# wish = str(input('[?] Do you wish to scrap web without tor ? [y/n]')).lower()[0]
				# if wish == 'y':
				# 	return False #Returning true just to allow scraping without tor.
				# else:
				# 	print('[-] Exiting ... ')
				# 	exit(0)
		
		return False

	def get_session(self):

		self.session = req.session()
	
		if self.must_torrify:
			print('[+] Please be patient we are performing secure connection !')
			if self.is_tor_connected():
				self.session.proxies = self.tor_proxy
			else:
				print('[+] Continuing without tor !')

		return self.session

	def get_res(self,url):

		if 'http' not in url:
			url='http://'+url
		# try:
		if self.use_random_fake_user_agent:
			self.session.headers = {'User-Agent': self.fake_user_agent.get_random_fake_user_agent()}
		
		res = self.session.get(url,timeout=self.max_response_time)
		
		if res.status_code == 200:
			return res.content
		# 	else:
		# 		self.failed_scraped_links.append(url)
		# 		print(f'[-] Unable to scrape {url} ({res.status_code})')
		# except Exception as e:
		# 	self.failed_scraped_links.append(url)
		# 	print(f'[-] Unable to scrape {url} [{e}]')
		return False
		
	
	def get_current_scraped_dict(self): #wrote this function for avoid code repetation everytime for gettin only links!
		scraped_links_dict = {}
		scraped_links_dict['URL'] = [link.url for link in self.successful_scraped_links]
		scraped_links_dict['title'] = [link.title for link in self.successful_scraped_links]
		scraped_links_dict['a'] = [link.a_tags for link in self.successful_scraped_links]
		scraped_links_dict['img'] = [link.img_tags for link in self.successful_scraped_links]
		scraped_links_dict['p'] = [link.p_tags for link in self.successful_scraped_links]
		scraped_links_dict['hi'] = [link.h_tags for link in self.successful_scraped_links]
		scraped_links_dict['html_text'] = [link.html_text for link in self.successful_scraped_links]
		scraped_links_dict['website_category'] = [link.website_category for link in self.successful_scraped_links]
		return scraped_links_dict
	
	def purify_links(self,base_url,links):
		purified_links = []
		for link in links:
			if 'http' in link:
				purified_links.append(link)
			else:
				purified_links.append(urljoin(base_url,link))
		return purified_links

	def get_url_folder(self,url,save_to):
		only_url = url.replace('http://','').replace('https://','').replace('/', '_')
		return os.path.join(save_to,only_url)
	
	def create_url_folder(self,url,save_to):

		url_folder_name = self.get_url_folder(url,save_to)
		
		if not os.path.isdir(url_folder_name):			
			os.mkdir(f'{url_folder_name}')
				
	def scrap(self,url,save_to=None):

		# Inlizing the ScapedURL Model

		# Deleting the older details for the same url
		scrapped_URL_Table.objects.filter(base_url=url).delete()

		current_url_model = scrapped_URL_Table(base_url=url)
		current_url_model.url_rendered = self.is_slow_mode
		current_url_model.save()
		
		# keeping at least some mins duration for changing ip
		if ((time.time()-self.ip_changed_last_time)/60) > self.changing_ip_after_minutes:
			if self.controller_port_password and len(self.successful_scraped_links) % self.changing_ip_after_number_scarpped_website == 0 and len(self.successful_scraped_links) > 0:
				print('\n[+] Trying for new exit node IP.')
				self.change_tor_exit_node()
				self.ip_changed_last_time = time.time()

		if save_to == None:
			save_to = self.default_output_folder_location
		
		self.create_url_folder(url,save_to)

		only_url = url.replace('http://','').replace('https://','').replace('/', '_').replace('?', '_')

		try:

			if not self.is_slow_mode:
				html_content = self.get_res(url)
			else:
				html_content = self.load_url_in_driver(url,current_url_model)
			
			if html_content:
				
				html = html_content
				
				soup = BeautifulSoup(html,'html.parser')

				raw_html = soup.prettify()
				current_url_model.html = raw_html
				
				all_text = soup.get_text()
				current_url_model.text = all_text

				website_category = WEBSITE_CATEGORY_MODEL.predict([all_text])[0]
				current_url_model.website_category = website_category

				try:
					title_text = soup.title.text
				except AttributeError as e:
					title_text = ''
				
				current_url_model.title = title_text
				current_url_model.save()
				#region Insert all parsed tag in the model Tables

				for tag in soup.find_all():
					try:
						tag_table = html_Tag_Table(scrapped_URL_Table=current_url_model)
						
						tag_table.tag_name = tag.name
						tag_table.tag_inner_text = tag.text
						tag_table.raw_tag = str(tag)
						
						tag_table.save()
						
						for arg_key,arg_value in tag.attrs.items():
							arg_table = html_Tag_Arg_Table(scrapped_URL_Table=current_url_model,html_Tag_Table=tag_table)
							arg_table.arg_name = arg_key
							arg_table.arg_value = str(arg_value)
							arg_table.save()
					except Exception as ex:
						print(f'[-] Execption occured in saving table due to {ex}')
				#endregion
				
				if self.must_have_words:
					if self.is_must_have_words_in_textual_data(only_url=only_url,data=all_text):
						self.must_have_words_filtered_links.append(url)

				return current_url_model

		except Exception as e:
			print(f'[-] Failed in scrap due to {e}')

	def are_any_words_in_link(self,link,words):
		if words:
			link=link.lower()
			for word in words:
				if (word.lower().replace('\n','') in link) or (link in word.lower()): 	
					return True
			return False
		
	def is_must_have_words_in_textual_data(self,only_url,data,must_have_words=None):
		if not must_have_words:
			must_have_words = self.must_have_words
		data=data.lower()
		for word in must_have_words:
			if (word.lower() in data) or (data in word.lower()):  
				try:
					print('[-] Currently KEYWORD_PROOF_REQUIRED with OCR is disabled (due to easy-ocr dependency -> torch have no dependency for py11) !')
					# if KEYWORD_PROOF_REQUIRED and self.is_slow_mode and self.screenshot_folder:
					# 	with open(os.path.join(self.screenshot_folder,'screenshot_full.png'),'rb') as f:
					# 		screenshot = f.read()
							
					# 		must_have_words_proof_name = f'{word}_found_in_{only_url.replace("/","_")}.png'

					# 		must_have_words_proof_folder = os.path.join(self.extra_data_folder,'must_have_words_proof')

					# 		if not os.path.isdir(must_have_words_proof_folder):
					# 			os.makedirs(must_have_words_proof_folder)
							

					# 		with open(os.path.join(must_have_words_proof_folder,must_have_words_proof_name),'wb') as f2:
					# 			f2.write(screenshot)

					# 		if (len(threading.enumerate())-1) > MAX_THREAD_COUNT:
					# 			#KeywordBox(input_image_folder,input_image,keyword,all_matches=False)
					# 			Thread(target=KeywordBox,args=[must_have_words_proof_folder,must_have_words_proof_name,word,True]).start()
					# 		else:
					# 			KeywordBox(input_image_folder=must_have_words_proof_folder,input_image=must_have_words_proof_name,keyword=word,all_matches=True)

				
				except Exception as e:
					print(f'[-] Unable to save screenshot of {only_url} for word {word} due to {e} error.')
				
				return True
		return False	

	def get_links_from_a_tags(self,base_url_model):
		hrefs = []
		for arg in html_Tag_Arg_Table.objects.filter(scrapped_URL_Table=base_url_model,arg_name='href'):
			hrefs.append(arg.arg_value)
		return hrefs

	def is_link_scraped(self,link:str):
		return False if scrapped_URL_Table.objects.filter(base_url=link).count() == 0 or scrapped_URL_Table.objects.filter(base_url=f'{link}/').count() == 0 else True


	def crawl(self,start_url,crawl_depth=0):
		if crawl_depth > self.crawl_depth: 
			return

		self.current_crawl_depth = crawl_depth

		if len(self.successful_scraped_links) >= self.max_crawl_count:
			print('\n[-] Reached to max crawl count!')
			print('[-] Stopping ...')
			return

		start_url_model = self.scrap(start_url)
		
		start_url_model_base_url = start_url_model.base_url

		if start_url_model_base_url:
			
			links = self.get_links_from_a_tags(start_url_model)

			filterd_links = []

			for link in links:
				if '.' in link:
					if not self.is_link_scraped(link):
						if link not in self.unique_links:
							if not self.includes_stop_words(link):
								if self.includes_must_have_words(link):
									if CRAWL_IN_DOMAIN and '.onion' not in link: # Don't apply crawl in domain for onion links
										if self.base_url_domain not in link:
											continue
									filterd_links.append(link)
		
			self.unique_links += filterd_links
			print(filterd_links)
			for link in filterd_links:
				try:
					if (len(threading.enumerate())-1) > MAX_THREAD_COUNT:
						Thread(target=self.crawl,args=(link,crawl_depth+1,)).start()
					else:
						self.crawl(link,crawl_depth=crawl_depth+1)
					
					time.sleep(self.pause_crawl_duration)
				except Exception as e:
					print(f"[-] Unable to crawl {link} (E:{e})")
					self.failed_scraped_links.append(start_url)	

	def __init__(self):

		#base url
		self.base_url = ''
		self.base_url_domain = ''

		# options
		self.is_slow_mode = False
		self.must_torrify = False
		self.use_random_fake_user_agent = False
		self.fake_user_agent = FakeUserAgent()
		self.max_response_time = 30
		self.tor_proxy = {'http':f'{TOR_PROXY}','https':f'{TOR_PROXY}'}
		
		#Session and drivers
		self.session = req.session()		
		self.driver = None
		self.driver_options = None
		self.screenshot_folder = ''

		#crawling settings
		self.crawl_depth = 5
		self.current_crawl_depth = 0

		#crawling time settings
		self.changing_ip_after_minutes = 25
		self.max_crawl_count = 1000
		self.pause_crawl_duration = 0
		self.changing_ip_after_number_scarpped_website = 25
		self.changing_ip_after_minutes = 5
		self.ip_changed_last_time = time.time()
		
		#for tor
		self.controller_port_password = None 
		
		#filtering links options
		self.includes_stop_words = lambda link : (self.are_any_words_in_link(link,self.stopwords_in_link) if self.stopwords_in_link else False) # If stop words list is empty it will return False by default to by-pass this filter
		self.includes_must_have_words = lambda link: (self.are_any_words_in_link(link,self.must_have_words_in_link) if self.must_have_words_in_link else True) # If must have words in link list is empty it will return True by default to by-pass this filter
		self.stopwords_in_link = []
		self.must_have_words_in_link = []
		self.must_have_words = []
		self.must_have_words_filtered_links = []
		
		#progress keeping options
		self.errors = []
		self.failed_scraped_links = []
		self.successful_scraped_links = []		
		self.unique_links = []
		
		#verbose table settings
		self.analysis_table = PrettyTable()
		self.verbose_output = False

		#folder settings
		self.default_output_folder_location = OUTPUT_SAVING_PATH
		if OUTPUT_SAVING_PATH:
				if not os.path.isdir(OUTPUT_SAVING_PATH):
					os.mkdir(OUTPUT_SAVING_PATH)
		self.extra_data_folder = os.path.join(self.default_output_folder_location,"extra_data")
		if self.extra_data_folder:
				if not os.path.isdir(self.extra_data_folder):
					os.mkdir(self.extra_data_folder)

ds_obj = DiggySpidy()

#Main Driver Code
if __name__ == '__main__':
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------

	parser = ArgumentParser()

	parser.add_argument('--url','-u',default='',help='Enter url to scrape or crawl.')
	parser.add_argument('--print-ip-details','-pid',action='store_true',help='It will dump your current external ip , geo location and other related information.Use it for conformation if connected to proxy and you are not leaking your external ip by accident.')
	parser.add_argument('--crawl','-c',action='store_true',help='Crawls whole website and scrapes all the links recursively.By default it will only scrape the url.')
	parser.add_argument('--slow',action='store_true',help='It this mode crawler will capture (normal and full) screenshot of website.And fail count might be decreased.')
	parser.add_argument('--file','-f',help='It will fetch link from the text file and only scrap or crawl the website.')
	parser.add_argument('--verbose','-v',action='store_true',help='See verbose output -> live scraped website details.')
	parser.add_argument('--torrify','-t',action='store_true',help='It must use through tor socks proxy via default port 9050 for scraping websites.')

	#------------------------------------------------------------------------------------------------------------------------------------------------------------

	args = parser.parse_args()

	i_args = {'url':False,'file':False,'print-ip-details':False,'crawl':False,'slow':False,'verbose':False,'torrify':False}

	try:
		if is_connected_to_internet():
			if len(sys.argv) == 1:
				print_logo()
				i_args['url'] = input('Enter url (Press enter if you want to enter url links.txt) : ')
				i_args['file'] = input('Enter url links.txt loaction : ') if len(i_args['url']) == 0 else None
				i_args['print-ip-details'] = True if 'y' in input('Print IP details (y/N) : ').lower() else False
				i_args['crawl'] = True if 'c' in input('To crawl/scrape (c/s) : ').lower() else False
				i_args['slow'] = True if 'y' in input('Enable slow mode (y/N) : ').lower() else False
				i_args['verbose'] = True if 'y' in input('Enable verbose output (y/N) : ').lower() else False
				i_args['torrify'] = True if 'y' in input('Enable tor as proxy (y/N) : ').lower() else False

			else:
				print_small_logo()
			
			ds_obj.must_torrify = args.torrify if len(sys.argv) != 1 else i_args['torrify']

			if ds_obj.must_torrify:
				print('[+] Starting Tor ...')
				subprocess.Popen('tor')
				# Waiting 1 minute for letting tor start properly
				for i in tqdm(range(60),desc='[+] Waiting for 1 minute ....'):
					time.sleep(1)

			if (args.print_ip_details and len(sys.argv) != 1) | i_args['print-ip-details']:
				print('[+] Your current IP location.\n')
				ds_obj.print_ip_desc_table()		

			url = args.url if len(sys.argv) != 1 else i_args['url']

			ds_obj.base_url = url

			if ds_obj.base_url:
				ds_obj.base_url_domain = re.search(URL_DOMAIN_PATTEN,ds_obj.base_url).group(1)

			ds_obj.is_slow_mode = args.slow if len(sys.argv) != 1 else i_args['slow']

			ds_obj.crawl_depth = CRAWL_DEPTH

			ds_obj.use_random_fake_user_agent = USE_FAKE_USER_AGENT

			if OUTPUT_SAVING_PATH:
				if not os.path.isdir(OUTPUT_SAVING_PATH):
					os.mkdir(OUTPUT_SAVING_PATH)

			ds_obj.default_output_folder_location = OUTPUT_SAVING_PATH

			ds_obj.create_url_folder(url=ds_obj.base_url,save_to=ds_obj.default_output_folder_location)

			ds_obj.extra_data_folder = os.path.join(ds_obj.get_url_folder(url=ds_obj.base_url,save_to=ds_obj.default_output_folder_location),"extra_data")
			
			if not os.path.isdir(ds_obj.extra_data_folder):
				os.mkdir(ds_obj.extra_data_folder)

			ds_obj.verbose_output = args.verbose if len(sys.argv) != 1 else i_args['verbose']

			if 'onion' in url and not ds_obj.must_torrify:
				print('[+] Entered link is an onion link hence automatically using tor proxy.')
				ds_obj.must_torrify = True

			ds_obj.max_crawl_count = MAX_CRAWL_COUNT

			ds_obj.max_response_time = MAX_RESPONSE_TIME

			ds_obj.pause_crawl_duration = SCRAPE_PAUSE_AFTER_EVERY_URL

			ds_obj.stopwords_in_link = get_list_from_file(STOPWORDS_IN_LINK_FILE)

			ds_obj.must_have_words_in_link = get_list_from_file(MUST_HAVE_WORDS_IN_LINK_FILE)

			ds_obj.must_have_words = get_list_from_file(MUST_HAVE_WORDS_IN_WEBSITE_TEXT_FILE)	

			ds_obj.controller_port_password = CONTROL_PORT_PASSWORD

			ds_obj.changing_ip_after_number_scarpped_website = CHANGE_IP_AFTER_SCRAPPING_NUMBER_OF_WEBSITES

			ds_obj.changing_ip_after_minutes = CHANGE_IP_AFTER_MINUTES
	
	
			if ds_obj.is_slow_mode:
				ds_obj.get_driver()
			else:
				ds_obj.get_session()
			
#------------------------------------------------------------------------------------------------------------------------------------------------
			
			links_file_location = args.file if len(sys.argv) != 1 else i_args['file']

			if ((args.crawl and len(sys.argv) != 1) | i_args['crawl']) and links_file_location:		
				with open(links_file_location,'r') as f:
					links = f.readlines()
					for link in links:
						link = link.replace('\n', '')
						if link:
							ds_obj.crawl(link)
			elif links_file_location:
				with open(links_file_location,'r') as f:
					links = f.readlines()
					for link in links:
						link = link.replace('\n', '')
						if link:
							ds_obj.scrap(link)
			elif (args.crawl and len(sys.argv) != 1) | i_args['crawl']:
				ds_obj.crawl(url)
			else:
				ds_obj.scrap(url)
	except KeyboardInterrupt:
		#Saving all data in a excel format for scrapped link.
		pd.DataFrame().from_dict(ds_obj.get_current_scraped_dict(),orient='index').transpose().to_excel(os.path.join(ds_obj.extra_data_folder,f'All_Scrapped_Data_{round(time.time())}.xlsx'),index=False)
			
		print('\n[-] Quiting ...')
		exit(0)
	except Exception as e:
		print(f'[-] Something went wrong due to {e}.')
		print('\n[-] Quiting ...')
		exit(0)
