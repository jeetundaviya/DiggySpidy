from distutils.log import error
import re
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from argparse import ArgumentParser
import datetime
from prettytable import PrettyTable
from fake_useragent import UserAgent
import time
from stem import Signal
from stem.control import Controller
import sys
from urllib.parse import urljoin
from threading import Thread
import selenium as se
from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
import socket

BLUE, RED, WHITE, YELLOW, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[32m', '\033[0m'

TOR_PROXY = "socks5://127.0.0.1:9050"

CHECK_TOR_URL = 'http://check.torproject.org'

FETCH_IP_DETAILS_URL = 'http://ip-api.com/json'

URL_FOR_CHECKING_INTERNET_CONNECTIVITY = 'example.com'

CONTROL_PORT_PASSWORD = 'p@5s30R6' #Enter your control port password here !

def is_connected_to_internet():
	try:
		s = socket.create_connection((URL_FOR_CHECKING_INTERNET_CONNECTIVITY, 80), 2)
		s.close()
		return True
	except Exception as e:
		print(f'[-] Unable to connect to internet due to {e} !\n[-] Please check your internet connection !')
		print('[-] Exiting ...')
		exit(0)	
	
	
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
             '\n' + 'Made with {}<3{} by: Jeet Undaviya ({}0.<{}){}'.format(RED,YELLOW, RED, YELLOW, BLUE).center(100) +
             '\n' + 'Version: {}2.0{}'.format(YELLOW, END).center(85)+
             '\n\n' + 'Type python diggy_spidy.py -h or --help for help'.format(YELLOW, END).center(80) + '\n\n')

def get_list_from_file(file):
		with open(file,'r') as f:
			return f.readlines()

class ScrapedLink:
	def __init__(self,url):
		self.url = url
		self.a_tag_count = 0
		self.img_tag_count = 0
		self.p_tag_count = 0
		self.h_tag_count = 0

class DiggySpidy:

	def get_driver(self):

		self.driver_options = webdriver.ChromeOptions()

		if self.must_torrify:
			if self.is_tor_connected():
				self.driver_options.add_argument(f'--proxy-server={TOR_PROXY}')
		
		self.driver_options.add_argument('--headless')

		self.driver = webdriver.Chrome(options=self.driver_options)
		self.driver.maximize_window() # Maximizing window by default
	
	def load_url_in_driver(self,url,save_to):

		if self.use_random_fake_user_agent:
			self.driver_options.add_argument(f'user-agent={UserAgent().random}')

		self.driver = webdriver.Chrome(options=self.driver_options)
		
		self.driver.maximize_window() # Maximizing window by default

		if 'http' not in url:
			url='http://'+url

		self.driver.implicitly_wait(self.max_response_time) #It will at max wait for 30 seconds for loading website.
		
		self.driver.get(f'{url}')

		self.capture_screenshot(url,save_to)

		return self.driver.page_source
	
	def capture_screenshot(self,url,save_to):

		url_folder = self.get_url_folder(url,save_to)

		screenshot_folder = os.path.join(url_folder,'screenshots')

		if not os.path.isdir(screenshot_folder):
			os.mkdir(f'{screenshot_folder}')

		self.driver.get_screenshot_as_file(os.path.join(screenshot_folder,'screenshot.png'))

		#Maxmizing window size to scrollable content to take full screenshot !
		window_size = lambda X: self.driver.execute_script('return document.body.parentNode.scroll'+X)
		self.driver.set_window_size(window_size('Width'),window_size('Height'))
		self.driver.get_screenshot_as_file(os.path.join(screenshot_folder,'screenshot_full.png'))

		with open(os.path.join(screenshot_folder,'full_page.pdf'),'wb') as f:
			b64_encoded_str = self.driver.print_page()
			f.write(base64.b64decode(b64_encoded_str))

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
						wish = str(input('[?] Do you wish to scrap web without tor ? [y/n]')).lower()[0]
						if wish == 'y':
							return False #Returning true just to allow scraping without tor.
						else:
							print('[-] Exiting ... ')
							exit(0)
			except Exception as e:
				print(f'[-] Failed to verify tor status due to {e} !\n')
				wish = str(input('[?] Do you wish to scrap web without tor ? [y/n]')).lower()[0]
				if wish == 'y':
					return False #Returning true just to allow scraping without tor.
				else:
					print('[-] Exiting ... ')
					exit(0)
		
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
		try:
			if self.use_random_fake_user_agent:
				self.session.headers = {'User-Agent': UserAgent().random}
			
			res = self.session.get(url)
			
			if res.status_code == 200:
				return res.content
			else:
				self.failed_scraped_links.append(url)
				self.errors.append(f'[-] Unable to scrape {url} ({res.status_code})')
		except Exception as e:
			self.failed_scraped_links.append(url)
			self.errors.append(f'[-] Unable to scrape {url} [{e}]')
		return False
		
	def extract_links_from_tag_attribute(self,tag_list,attribute):
		
		links = []

		fetch_link = lambda tag,attribute: tag[attribute]
		
		for tag in tag_list:
			try:
				links.append(fetch_link(tag, attribute))
			except Exception as e:
				continue

		return links

	def save_file(self,file_name,folder_location=None,data=None,data_list=None):

		if folder_location == None:
			folder_location = self.default_folder_location

		file = os.path.join(folder_location,file_name)

		if data != None:
			with open(file,'wb') as f:
				f.write(data)
			return True
		elif data_list != None:
			with open(file,'w') as f:
				f.writelines([data+'\n' for data in data_list])
			return True
		else:
			print('[-] Data or DataList not provided !')
			return False

	def get_current_scraped_list(self): #wrote this function for avoid code repetation everytime for gettin only links!
		return [link.url for link in self.successful_scraped_links]

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
	
	def create_folders(self,url,save_to):

		url_folder_name = self.get_url_folder(url,save_to)
		
		if not os.path.isdir(url_folder_name):			
			os.mkdir(f'{url_folder_name}')

		html_folder = os.path.join(url_folder_name,'html')
		if not os.path.isdir(html_folder):
			os.mkdir(f'{html_folder}')

		links_folder = os.path.join(url_folder_name,'links')
		if not os.path.isdir(links_folder):
			os.mkdir(f'{links_folder}')

	def scarp(self,url,save_to=None):
		# keeping at least some mins duration for changing ip
		if ((time.time()-self.ip_changed_last_time)/60) > self.changing_ip_after_minutes:
			if self.controller_port_password and len(self.successful_scraped_links) % self.changing_ip_after_number_scarpped_website == 0 and len(self.successful_scraped_links) > 0:
				print('\n[+] Trying for new exit node IP.')
				self.change_tor_exit_node()
				self.ip_changed_last_time = time.time()

		if save_to == None:
			save_to = self.default_folder_location

		self.create_folders(url,save_to) #Empty folder means it was unable to scrap !

		only_url = url.replace('http://','').replace('https://','').replace('/', '_').replace('?', '_')

		if not self.is_slow_mode:
			html_content = self.get_res(url)
		else:
			html_content = self.load_url_in_driver(url,save_to)
		

		if html_content:

			html = html_content

			soup = BeautifulSoup(html,'lxml')

			raw_html = soup.prettify()
			try:
				title_text = soup.title.text
			except AttributeError as e:
				title_text = ''

			heading_tags = p_tags = a_tags = a_links = img_tags = img_links = []	

			try:
				h_lists = [soup.find_all('h'+str(i)) for i in range(1,7)] #Recursive list including all html headings.
				heading_tags = [h.text for h_list in h_lists for h in h_list] 
				p_tags = [p.text for p in soup.find_all('p')]
				a_tags = soup.find_all('a')
				a_links = self.purify_links(base_url=url,links=self.extract_links_from_tag_attribute(a_tags, 'href')) 	
				img_tags = soup.find_all('img')
				img_links = self.purify_links(base_url=url,links=self.extract_links_from_tag_attribute(img_tags, 'src'))	
			except TypeError:
				pass

			all_text = soup.get_text()
			
			url_folder_name = self.get_url_folder(url,save_to)
			html_folder = os.path.join(url_folder_name,'html')
			links_folder = os.path.join(url_folder_name,'links')


			data_dict = {
			'url':url,
			'folder_location':url_folder_name,
			'text':all_text,
			'html':raw_html,
			'title': title_text,
			'headings': heading_tags,
			'p':p_tags,
			'a_links':a_links,
			'img_links':img_links
			}

			if self.must_have_words:
				if self.is_must_have_words_in_data(data=all_text):
					self.must_have_words_filtered_links.append(url)

			current_scraped_url = ScrapedLink(data_dict['url'])
			current_scraped_url.img_tag_count = len(data_dict['img_links'])
			current_scraped_url.a_tag_count = len(data_dict['a_links'])
			current_scraped_url.h_tag_count = len(data_dict['headings'])
			current_scraped_url.p_tag_count = len(data_dict['p'])

			self.successful_scraped_links.append(current_scraped_url)

			self.update_analysis_table()

			self.print_live_updates()

			data_json = json.dumps(data_dict,indent=4)

			pd.DataFrame().from_dict(data_dict,orient='index').transpose().to_csv(os.path.join(url_folder_name,only_url+'.csv'))

			self.save_file(file_name='analysis_table.txt',folder_location=self.default_folder_location,data=self.analysis_table.get_string().encode())
			self.save_file(file_name='successful_scraped_links.txt',data_list=self.get_current_scraped_list())
			self.save_file(file_name='unique_links.txt',data_list=self.unique_links)
			self.save_file(file_name='must_have_words_links.txt',data_list=self.must_have_words_filtered_links)
			self.save_file(file_name=only_url+'.json',folder_location=url_folder_name,data=data_json.encode())
			self.save_file(file_name=only_url+'.html',folder_location=html_folder,data=raw_html.encode())
			self.save_file(file_name=only_url+'.txt',folder_location=html_folder,data=all_text.encode())
			self.save_file(file_name='error.txt',folder_location=self.default_folder_location,data_list=self.errors)
			self.save_file(file_name='a_links.txt',folder_location=links_folder,data_list=a_links) if len(data_dict['a_links']) > 0 else None
			self.save_file(file_name='img_links.txt',folder_location=links_folder,data_list=img_links) if len(data_dict['img_links']) > 0 else None

			return data_dict

	def get_unique_but_remaining_to_scrap_links(self):
		
		'''This will be baised on old linked taking refrence from unique_link.txt and scraped_link.txt'''
		
		self.load_old_scraped_and_unique_links()

		self.save_file(file_name='remaining_links.txt',data_list=[link for link in self.old_unique_links if link not in self.old_successful_scraped_links])

	def are_any_words_in_link(self,link,words):
		if words:
			link=link.lower()
			for word in words:
				if (word.lower() in link) or (link in word.lower()): 	
					return True
			return False
		
	def is_must_have_words_in_data(self,data,must_have_words=None):
		if not must_have_words:
			must_have_words = self.must_have_words
		data=data.lower()
		for word in must_have_words:
			if (word.lower() in data) or (data in word.lower()): 
				return True
		return False	

	def print_live_updates(self):
		
		minify_url = lambda url: url if len(url) < 50 else url[:50]+'...'

		if self.verbose_output:
			clear_screen()

			print_logo()
			print(f'[+] Success count : {len(self.successful_scraped_links)}/{self.max_crawl_count}  [+] Fail count : {len(self.failed_scraped_links)}/{len(self.unique_links)} [+] Links found : {len(self.unique_links)}',end='\n\n')
			if self.must_have_words_filtered_links:
				print(f'[+] Desired links count : {len(self.must_have_words_filtered_links)}',end='\n\n')
			print(f'[+] Current crawling depth : {self.current_crawl_depth}',end='\n\n')
			print(f'[+] Latest website : {self.successful_scraped_links[-1].url}',end='\n\n')
			if self.errors:
				print(f'[+] Last error : {self.errors[-1]}',end='\n\n')
			
			print(self.analysis_table)
		else:
			live_updates = f'[+] Progress : {len(self.successful_scraped_links)}/{self.max_crawl_count} [+] Fail count : {len(self.failed_scraped_links)}/{len(self.unique_links)} [+] Links found : {len(self.unique_links)} [+] Latest website : {minify_url(self.successful_scraped_links[-1].url)}'
			
			print(live_updates,end='\r')

	def update_analysis_table(self):
		
		minify_url = lambda url: url if len(url) < 50 else url[:50]+'...'

		self.analysis_table = PrettyTable(field_names=['URL','<a> tag count','<img> tag count','<p> tag count','<hi> heading tags count'])
			
		for link in self.successful_scraped_links:
			self.analysis_table.add_row([minify_url(link.url),link.a_tag_count,link.img_tag_count,link.p_tag_count,link.h_tag_count])

	def load_old_scraped_and_unique_links(self):
		file = os.path.join(self.default_folder_location,f'successful_scraped_links.txt')
		if os.path.isfile(file):
			with open(file,'r') as f:
				s_links = f.readlines()
				self.old_unique_links = s_links

		file = os.path.join(self.default_folder_location,f'unique_links.txt')
		if os.path.isfile(file):
			with open(file,'r') as f:
				u_links = f.readlines()
				self.old_unique_links = u_links 

	def crawl(self,start_url,crawl_depth=0,save_to=None):

		if crawl_depth > self.crawl_depth: 
			return

		self.current_crawl_depth = crawl_depth

		if len(self.successful_scraped_links) >= self.max_crawl_count:
			self.save_file(file_name='successful_scraped_links.txt',data_list=self.get_current_scraped_list())
			self.save_file(file_name='unique_links.txt',data_list=self.unique_links)
			self.get_unique_but_remaining_to_scrap_links()
			print('\n[-] Reached to max crawl count!')
			print('[-] Exiting ...')
			exit(0)

		if save_to == None:
			save_to = self.default_folder_location

		start_data_dic = self.scarp(start_url,save_to)
		
		if start_data_dic:
			
			links = start_data_dic['a_links']
			
			folder_location = start_data_dic['folder_location']

			filterd_links = []

			for link in links:
				if ('.' in link):
					 if (link not in self.unique_links):
						 if not self.includes_stop_words(link):
							 if self.includes_must_have_words(link):
									filterd_links.append(link)
		
			self.unique_links += filterd_links
			
			for link in filterd_links:
				try:
					self.crawl(link,crawl_depth=crawl_depth+1,save_to=folder_location)
					time.sleep(self.pause_crawl_duration)
				except Exception as e:
					self.errors.append(f"[-] Unable to crawl {link} (E:{e})")
					self.failed_scraped_links.append(start_url)	

	def __init__(self):
		self.errors = []
		self.must_torrify = False
		self.driver = None
		self.driver_options = None
		self.use_random_fake_user_agent = False
		self.max_response_time = 30
		self.tor_proxy = {'http':f'{TOR_PROXY}','https':f'{TOR_PROXY}'}
		self.session = req.session()
		self.is_slow_mode = False
		self.controller_port_password = None 
		self.changing_ip_after_minutes = 25
		self.max_crawl_count = 1000
		self.crawl_depth = 5
		self.current_crawl_depth = 0
		self.pause_crawl_duration = 0
		self.failed_scraped_links = []
		self.successful_scraped_links = []
		self.includes_stop_words = lambda link : (self.are_any_words_in_link(link,self.stopwords_in_link) if self.stopwords_in_link else False)
		self.includes_must_have_words = lambda link: (self.are_any_words_in_link(link,self.must_have_words_in_link) if self.must_have_words_in_link else True) 
		self.analysis_table = PrettyTable(field_names=['URL','<a> tag count','<img> tag count','<p> tag count','<hi> heading tags count'])
		self.unique_links = []
		self.old_unique_links = []
		self.old_successful_scraped_links = []
		self.stopwords_in_link = []
		self.must_have_words_in_link = []
		self.must_have_words = []
		self.default_folder_location = os.getcwd()
		self.verbose_output = False
		self.must_have_words_filtered_links = []
		self.changing_ip_after_number_scarpped_website = 25
		self.changing_ip_after_minutes = 5
		self.ip_changed_last_time = time.time()

if __name__ == '__main__':
	
	#------------------------------------------------------------------------------------------------------------------------------------------------------------

	parser = ArgumentParser()

	parser.add_argument('--url','-u',default='',help='Enter url to scrape or crawl.')
	parser.add_argument('--print-ip-details',action='store_true',help='It will dump your current external ip , geo location and other related information.Use it for conformation if connected to proxy and you are not leaking your external ip by accident.')
	parser.add_argument('--crawl','-c',action='store_true',help='Crawls whole website and scrapes all the links recursively.')
	parser.add_argument('--crawl-depth','-cd',default=5,help='How much deeper should it crawl.')
	parser.add_argument('--fast',action='store_true',help='In this mode will not capture screenshot of website. And fail count might be more.')
	parser.add_argument('--slow',action='store_true',help='It this mode crawler will capture (normal and full) screenshot of website.And fail count might be decreased.')
	parser.add_argument('--use-random-fake-user-agent',action='store_true',help='It will randomly choose fake User-Agent and copy it in header before sending every get request.')
	parser.add_argument('--max-response-time','-mrt',default=30,help='For given amount of seconds it should wait for website to load or respond.')
	parser.add_argument('--pause','-cp',default=0,help='It will start crawling every new website after provided number of seconds.')
	parser.add_argument('--stopcount','-cs',default=1000,help='After crawling this much count it should stop')
	parser.add_argument('--scrap','-s',action='store_true',help='Only scrap the website.')
	parser.add_argument('--text-file','-tf',help='It will fetch link from file and only scrap the website.')
	parser.add_argument('--output','-o',default=os.getcwd(),help='At this location files will be saved.')
	parser.add_argument('--verbose','-v',action='store_true',help='See verbose output -> live scraped website details.')
	parser.add_argument('--must-torrify','-mt',action='store_true',help='It must use through tor socks proxy via default port 9050 for scraping websites.')
	# ['github','facebook','instagram','mailto','torproject','mozilla','firefox','bootstrap','signin','signup','login','microsoft']
	parser.add_argument('--stopwords-in-link',nargs='*',default=[],help='Enter words which you don\'t want in your scraped links for further scraping.')
	parser.add_argument('--stopwords-in-link-file',help='Enter path of your stopwords file. You can also enter stop-links to avoid repeatation of scraping.')
	parser.add_argument('--must-have-words-in-link',nargs='*',help='Enter words which you don\'t want in your scraped links for further scraping.')
	parser.add_argument('--must-have-words-in-link-file',help='Enter path of your stopwords file. You can also enter stop-links to avoid repeatation of scraping.')
	parser.add_argument('--must-have-words',nargs='*',help='Enter words which you must to have inside text of scraped links HTML for further scraping.')
	parser.add_argument('--must-have-words-file',help='Enter path of your stopwords file. You can also enter stop-links to avoid repeatation of scraping.')		
	parser.add_argument('--changing-ip-after-number-scarpped-website',default=25,help='Change IP after every provided number of scrapped websites.')
	parser.add_argument('--changing-ip-after-minutes',default=5,help='Change IP after every provided number of minutes.')

	#------------------------------------------------------------------------------------------------------------------------------------------------------------

	args = parser.parse_args()

	try:
		if is_connected_to_internet():
			if len(sys.argv) == 1:
				print_logo()
			else:

				print_small_logo()

				obj = DiggySpidy()
				
				url = args.url

				obj.current_crawled_url = url

				obj.is_slow_mode = args.slow

				obj.crawl_depth = int(args.crawl_depth)

				obj.use_random_fake_user_agent = args.use_random_fake_user_agent

				if args.output:
					if not os.path.isdir(args.output):
						os.mkdir(args.output)

				obj.default_folder_location = args.output

				obj.verbose_output = args.verbose

				

				obj.must_torrify = args.must_torrify

				if 'onion' in url and not args.must_torrify:
					wish = input('[+] Entered link is an onion link hence automatically using tor proxy.')
					obj.must_torrify = True

				obj.max_crawl_count = int(args.stopcount)

				obj.max_response_time = int(args.max_response_time)

				obj.pause_crawl_duration = int(args.pause)

				if args.stopwords_in_link:
					obj.stopwords_in_link = args.stopwords_in_link
				else:
					if args.stopwords_in_link_file:
						obj.stopwords_in_link = get_list_from_file(args.stopwords_in_link_file)

				if args.must_have_words_in_link:
					obj.must_have_words_in_link = args.must_have_words_in_link
				else:
					if args.must_have_words_in_link_file:
						obj.must_have_words_in_link = get_list_from_file(args.must_have_words_in_link_file)


				if args.must_have_words:
					obj.must_have_words = args.must_have_words
				else:
					if args.must_have_words_file:
						obj.must_have_words = get_list_from_file(args.must_have_words_file)	

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
				obj.controller_port_password = CONTROL_PORT_PASSWORD

				obj.changing_ip_after_number_scarpped_website = int(args.changing_ip_after_number_scarpped_website)

				obj.changing_ip_after_minutes = int(args.changing_ip_after_minutes)

				obj.load_old_scraped_and_unique_links()
		
				obj.get_unique_but_remaining_to_scrap_links()
		
				if obj.is_slow_mode:
					obj.get_driver()
				else:
					obj.get_session()
				

	#------------------------------------------------------------------------------------------------------------------------------------------------
				if args.crawl and args.text_file:
					with open(args.text_file,'r') as f:
						links = f.readlines()
						for link in links:
							link = link.replace('\n', '')
							if link:
								obj.crawl(link)
				elif args.text_file:
					with open(args.text_file,'r') as f:
						links = f.readlines()
						for link in links:
							link = link.replace('\n', '')
							if link:
								obj.scarp(link)
				elif args.crawl:
					obj.crawl(url)
				else:
					obj.scarp(url)
				
				if args.print_ip_details:
					print('[+] Your current IP location.\n')
					obj.print_ip_desc_table()		

	except KeyboardInterrupt:
		obj.save_file(file_name='successful_scraped_links.txt',data_list=obj.get_current_scraped_list())
		obj.save_file(file_name='unique_links.txt',data_list=obj.unique_links)
		obj.get_unique_but_remaining_to_scrap_links()
		obj.print_live_updates()
		print('\n[-] Quiting ...')
		exit(0)