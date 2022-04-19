from dg_config import *
from fake_user_agent import FakeUserAgent
import joblib
from distutils.log import error
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from argparse import ArgumentParser
from prettytable import PrettyTable
import time
from stem import Signal
from stem.control import Controller
import sys
from urllib.parse import urljoin
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
import socket
import re
from threading import Thread
import threading
from keyword_box_in_image import KeywordBox

#Loading Website Category Detection Model
WEBSITE_CATEGORY_MODEL = joblib.load('./NLP/website_category_detection_model.pkl')

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
             '\n' + 'Made with {}<3{} by: Jeet Undaviya ({}0.<{}) and Dhaiwat Mehta ({}1.<{}) {}'.format(RED,YELLOW, RED, YELLOW,RED, YELLOW, BLUE).center(115) +
             '\n' + 'Version: {}2.0{}'.format(YELLOW, END).center(85)+
             '\n\n' + 'Type python diggy_spidy.py -h or --help for help'.format(YELLOW, END).center(80) + '\n\n')

def get_list_from_file(file):
		with open(file,'r') as f:
			return [link.replace('\n','') for link in f.readlines() if len(link) > 1]
			# return f.readlines()

class ScrapedLink:
	def __init__(self,url):
		self.url = url
		self.title = ''
		self.a_tags = 0
		self.img_tags = 0
		self.p_tags = 0
		self.h_tags = 0
		self.html_text = ''
		self.website_category = ''

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
		
		self.driver.quit()

		if self.use_random_fake_user_agent:
			self.driver_options.add_argument(f'user-agent={self.fake_user_agent.get_random_fake_user_agent()}')

		self.driver = webdriver.Chrome(options=self.driver_options)
		
		self.driver.maximize_window() # Maximizing window by default

		if 'http' not in url:
			url='http://'+url

		self.driver.implicitly_wait(self.max_response_time) #It will at max wait for 30 seconds for loading website.
		
		self.driver.delete_all_cookies()

		self.driver.get(f'{url}')

		self.capture_screenshot(url,save_to)

		return self.driver.page_source
		
	def capture_screenshot(self,url,save_to):

		url_folder = self.get_url_folder(url,save_to)

		self.screenshot_folder = os.path.join(url_folder,'screenshots')

		if not os.path.isdir(self.screenshot_folder):
			os.mkdir(f'{self.screenshot_folder}')

		self.driver.get_screenshot_as_file(os.path.join(self.screenshot_folder,'screenshot.png'))

		#Maxmizing window size to scrollable content to take full screenshot !
		window_size = lambda X: self.driver.execute_script('return document.body.parentNode.scroll'+X)
		self.driver.set_window_size(window_size('Width'),window_size('Height'))
		self.driver.get_screenshot_as_file(os.path.join(self.screenshot_folder,'screenshot_full.png'))

		with open(os.path.join(self.screenshot_folder,'full_page.pdf'),'wb') as f:
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
		# try:
		if self.use_random_fake_user_agent:
			self.session.headers = {'User-Agent': self.fake_user_agent.get_random_fake_user_agent()}
		
		res = self.session.get(url,timeout=self.max_response_time)
		
		if res.status_code == 200:
			return res.content
		# 	else:
		# 		self.failed_scraped_links.append(url)
		# 		self.errors.append(f'[-] Unable to scrape {url} ({res.status_code})')
		# except Exception as e:
		# 	self.failed_scraped_links.append(url)
		# 	self.errors.append(f'[-] Unable to scrape {url} [{e}]')
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
			folder_location = self.default_output_folder_location

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
				
	def scarp(self,url,save_to=None):
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
				html_content = self.load_url_in_driver(url,save_to)
			
			if html_content:

				html = html_content

				soup = BeautifulSoup(html,'lxml')

				raw_html = soup.prettify()
				try:
					title_text = soup.title.text
				except AttributeError as e:
					title_text = ''

				heading_tags = []
				p_tags = []
				a_tags = []
				a_links = []
				img_tags = []
				img_links = []	

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

				website_category = WEBSITE_CATEGORY_MODEL.predict([all_text])[0]

				data_dict = {
				'url':url,
				'folder_location':url_folder_name,
				'text':all_text,
				'html':raw_html,
				'title': title_text,
				'headings': heading_tags,
				'p':p_tags,
				'a_links':a_links,
				'img_links':img_links,
				'website_category':website_category
				}

				current_scraped_url = ScrapedLink(data_dict['url'])
				current_scraped_url.title = data_dict['title']
				current_scraped_url.a_tags = data_dict['a_links']
				current_scraped_url.h_tags = data_dict['headings']
				current_scraped_url.p_tags = data_dict['p']
				current_scraped_url.html_text = data_dict['text']
				current_scraped_url.website_category = data_dict['website_category']

				self.successful_scraped_links.append(current_scraped_url)

				self.update_analysis_table()

				self.print_live_updates()

				pd.DataFrame().from_dict(data_dict,orient='index').transpose().to_csv(os.path.join(url_folder_name,only_url+'.csv'),index=False)

				if self.must_have_words:
					if self.is_must_have_words_in_textual_data(only_url=only_url,data=all_text):
						self.must_have_words_filtered_links.append(url)

				#Saving all data in a csv format for scrapped link.
				pd.DataFrame().from_dict(obj.get_current_scraped_dict(),orient='index').transpose().to_csv(os.path.join(self.extra_data_folder,f'Last_Session_All_Scrapped_Links_Data.csv'),index=False)

				self.save_file(file_name='successful_scraped_links.txt',folder_location=self.extra_data_folder,data_list=self.get_current_scraped_list())
				self.save_file(file_name='unique_links.txt',folder_location=self.extra_data_folder,data_list=self.unique_links)
				self.save_file(file_name='must_have_words_links.txt',folder_location=self.extra_data_folder,data_list=self.must_have_words_filtered_links)
				self.save_file(file_name='error.txt',folder_location=self.extra_data_folder,data_list=self.errors)

				return data_dict
		except Exception as e:
			self.failed_scraped_links.append(url)

			if len(os.listdir(self.get_url_folder(url,save_to))) == 0: #Deleting folder if empty !
				os.rmdir(self.get_url_folder(url,save_to))

			self.errors.append(f'[-] Unable to scrape {url} [{e}]')
			self.save_file(file_name='error.txt',folder_location=self.extra_data_folder,data_list=self.errors)

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
					if self.is_slow_mode and self.screenshot_folder:
						with open(os.path.join(self.screenshot_folder,'screenshot_full.png'),'rb') as f:
							screenshot = f.read()
							
							must_have_words_proof_name = f'{word}_found_in_{only_url.replace("/","_")}.png'

							must_have_words_proof_folder = os.path.join(self.extra_data_folder,'must_have_words_proof')

							if not os.path.isdir(must_have_words_proof_folder):
								os.makedirs(must_have_words_proof_folder)
							

							with open(os.path.join(must_have_words_proof_folder,must_have_words_proof_name),'wb') as f2:
								f2.write(screenshot)

							#KeywordBox(input_image=,output_image=,keyword=,all_matches=)
							Thread(target=KeywordBox,args=[os.path.join(must_have_words_proof_folder,must_have_words_proof_name),os.path.join(must_have_words_proof_folder,must_have_words_proof_name),word,True]).start()
							

				
				except Exception as e:
					self.errors.append(f'[-] Unable to save screenshot of {only_url} for word {word} due to {e} error.')
				
				return True
		return False	

	def print_live_updates(self):
		
		minify_url = lambda url : url if len(url) < 50 else url[:50]+'...'
		success_count = f'[+] Success count : {len(self.successful_scraped_links)}'
		fail_count = f'[+] Fail count : {len(self.failed_scraped_links)}'
		link_count = f'[+] Links found : {len(self.unique_links)}'
		latest_website = f'[+] Latest website : {minify_url(self.successful_scraped_links[-1].url)}'
		website_category = f'[+] Website Category : {self.successful_scraped_links[-1].website_category}'

		if self.verbose_output:
			clear_screen()

			print_logo()

			print(f'{success_count} {fail_count} {link_count}',end='\n\n')
			if self.must_have_words_filtered_links:
				print(f'[+] Desired links count : {len(self.must_have_words_filtered_links)}',end='\n\n')
			print(f'[+] Current crawling depth : {self.current_crawl_depth}',end='\n\n')
			
			print(f'{latest_website}',end='\n\n')
			
			print(f'{website_category}',end='\n\n')

			if self.errors:	
				print(f'[+] Last error : {self.errors[-1]}',end='\n\n')
			
			print(self.analysis_table)
		else:
			live_updates = f' {success_count} {fail_count} {link_count} {latest_website}'
			
			print(live_updates,end='\r')

	def update_analysis_table(self):
		
		minify_url = lambda url: url if len(url) < 50 else url[:50]+'...'

		self.analysis_table = PrettyTable(field_names=['URL','Links Found','Website Category'])
			
		for link in self.successful_scraped_links[-TABLE_ROW_NUMBER:]:
			self.analysis_table.add_row([minify_url(link.url),len(link.a_tags),link.website_category])

	def crawl(self,start_url,crawl_depth=0,save_to=None):

		if crawl_depth > self.crawl_depth: 
			return

		self.current_crawl_depth = crawl_depth

		if len(self.successful_scraped_links) >= self.max_crawl_count:
			self.save_file(file_name='successful_scraped_links.txt',folder_location=self.extra_data_folder,data_list=self.get_current_scraped_list())
			self.save_file(file_name='unique_links.txt',folder_location=self.extra_data_folder,data_list=self.unique_links)
			print('\n[-] Reached to max crawl count!')
			print('[-] Exiting ...')
			exit(0)

		if save_to == None:
			save_to = self.default_output_folder_location

		start_data_dic = self.scarp(start_url,save_to)
		
		if start_data_dic:
			
			links = start_data_dic['a_links']
			
			folder_location = start_data_dic['folder_location']

			filterd_links = []

			for link in links:
				if ('.' in link):
					if link not in self.get_current_scraped_list() or link+'/' not in self.get_current_scraped_list():
						if (link not in self.unique_links):
							if not self.includes_stop_words(link):
								if self.includes_must_have_words(link):
									if CRAWL_IN_DOMAIN:
										if self.base_url_domain not in link:
											continue
									filterd_links.append(link)
		
			self.unique_links += filterd_links
			
			for link in filterd_links:
				try:
					if (len(threading.enumerate())-1) > MAX_THREAD_COUNT:
						Thread(target=self.crawl,args=(link,crawl_depth+1,folder_location,)).start()
					else:
						self.crawl(link,crawl_depth=crawl_depth+1,save_to=folder_location)
					
					time.sleep(self.pause_crawl_duration)
				except Exception as e:
					self.errors.append(f"[-] Unable to crawl {link} (E:{e})")
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
		self.includes_stop_words = lambda link : (self.are_any_words_in_link(link,self.stopwords_in_link) if self.stopwords_in_link else False)
		self.includes_must_have_words = lambda link: (self.are_any_words_in_link(link,self.must_have_words_in_link) if self.must_have_words_in_link else True) 
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
		self.default_output_folder_location = os.getcwd()
		self.extra_data_folder = os.path.join(self.default_output_folder_location,"extra_data")

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

	try:
		if is_connected_to_internet():
			if len(sys.argv) == 1:
				print_logo()
			else:
				print_small_logo()

				obj = DiggySpidy()
				
				if args.print_ip_details:
					print('[+] Your current IP location.\n')
					obj.print_ip_desc_table()		

				url = args.url

				obj.base_url = url

				if obj.base_url:
					obj.base_url_domain = re.search(URL_DOMAIN_PATTEN,obj.base_url).group(1)

				obj.is_slow_mode = args.slow

				obj.crawl_depth = CRAWL_DEPTH

				obj.use_random_fake_user_agent = USE_FAKE_USER_AGENT

				if OUTPUT_SAVING_PATH:
					if not os.path.isdir(OUTPUT_SAVING_PATH):
						os.mkdir(OUTPUT_SAVING_PATH)

				obj.default_output_folder_location = OUTPUT_SAVING_PATH

				obj.create_url_folder(url=obj.base_url,save_to=obj.default_output_folder_location)

				obj.extra_data_folder = os.path.join(obj.get_url_folder(url=obj.base_url,save_to=obj.default_output_folder_location),"extra_data")
				
				if not os.path.isdir(obj.extra_data_folder):
					os.mkdir(obj.extra_data_folder)

				obj.verbose_output = args.verbose

				obj.must_torrify = args.torrify

				if 'onion' in url and not args.torrify:
					print('[+] Entered link is an onion link hence automatically using tor proxy.')
					obj.must_torrify = True

				obj.max_crawl_count = MAX_CRAWL_COUNT

				obj.max_response_time = MAX_RESPONSE_TIME

				obj.pause_crawl_duration = SCRAPE_PAUSE_AFTER_EVERY_URL

				obj.stopwords_in_link = get_list_from_file(STOPWORDS_IN_LINK_FILE)

				obj.must_have_words_in_link = get_list_from_file(MUST_HAVE_WORDS_IN_LINK_FILE)

				obj.must_have_words = get_list_from_file(MUST_HAVE_WORDS_IN_WEBSITE_TEXT_FILE)	

				obj.controller_port_password = CONTROL_PORT_PASSWORD

				obj.changing_ip_after_number_scarpped_website = CHANGE_IP_AFTER_SCRAPPING_NUMBER_OF_WEBSITES

				obj.changing_ip_after_minutes = CHANGE_IP_AFTER_MINUTES
		
		
				if obj.is_slow_mode:
					obj.get_driver()
				else:
					obj.get_session()
				
	#------------------------------------------------------------------------------------------------------------------------------------------------
				if args.crawl and args.file:
					with open(args.file,'r') as f:
						links = f.readlines()
						for link in links:
							link = link.replace('\n', '')
							if link:
								obj.crawl(link)
				elif args.file:
					with open(args.file,'r') as f:
						links = f.readlines()
						for link in links:
							link = link.replace('\n', '')
							if link:
								obj.scarp(link)
				elif args.crawl:
					obj.crawl(url)
				else:
					obj.scarp(url)
	except KeyboardInterrupt:
		obj.save_file(file_name='successful_scraped_links.txt',folder_location=obj.extra_data_folder,data_list=obj.get_current_scraped_list())
		obj.save_file(file_name='unique_links.txt',folder_location=obj.extra_data_folder,data_list=obj.unique_links)

		obj.print_live_updates()

		#Saving all data in a csv format for scrapped link.
		pd.DataFrame().from_dict(obj.get_current_scraped_dict(),orient='index').transpose().to_csv(os.path.join(obj.extra_data_folder,f'All_Scrapped_Data_{round(time.time())}.csv'),index=False)
			
		print('\n[-] Quiting ...')
		exit(0)
	except Exception as e:
		print(f'[-] Something went wrong due to {e}.')
		print('\n[-] Quiting ...')
		exit(0)
