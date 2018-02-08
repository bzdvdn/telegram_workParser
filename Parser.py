import requests
import csv
from bs4 import BeautifulSoup
from random import choice

__author__ = 'bzdvdn'

class Parser(object):
	def __init__(self, message, chat_id):
		self.message = message
		self.chat_id = chat_id

	def get_html(self, url, user=None):
		r = requests.get(url)

		return r.text

	def get_total_pages(self, html):
		soup = BeautifulSoup(html, "lxml")
		pages = soup.find('ul', class_='pagination' ).find_all('a')[-1].get('href')
		total_pages = int(pages.split('=')[1].split('&')[0]) + 1

		return int(total_pages)

	def write_csv(self, data,message,fileprefix):
		with open(str(self.chat_id) + '_-_' + str(self.message) + '.csv', 'a') as f:
			writer = csv.writer(f, dialect='excel', quotechar='"',  quoting=csv.QUOTE_ALL)
			writer.writerow((data['title'],
							 data['company'],
							 data['city'],
							 data['employment'],
							 data['url'],
							 data['skills'],
							 data['mb_skills'],
							 ))
			print(data['title'], ' parsed!')

	def get_pages_data(self, html):
		soup = BeautifulSoup(html, "lxml")
		ads = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link card-logotype')
		for index, iterator in enumerate(ads):
			name  = title = iterator.find('h2').find('a').get('title').strip().lower()

			if str(self.message).lower() in name:
				try:
					title = iterator.find('h2').find('a').get('title').strip().lower()
					url = 'https://www.work.ua' + iterator.find('h2').find('a').get('href')
					print('{} - index, url - {}'.format(index,url))
				except Exception as e:
					print(e)
					continue
				try:
					page = self.get_html(url)
					desc_soup = BeautifulSoup(page, 'lxml')
					company = desc_soup.find('dl', class_='dl-horizontal').find('a').find('b').get_text().strip()
					city = desc_soup.find('dl', class_='dl-horizontal').findAll('dd')[-2].get_text().strip()
					employment = desc_soup.find('dl', class_='dl-horizontal').findAll('dd')[-1].get_text().strip()	
				except Exception as e:
					print(e)
					continue
				try:
					skills = desc_soup.find('div', class_='wordwrap').find('ul').get_text()
				except:
					skills = ''
				try:
					mb_skills = desc_soup.find('div', class_='wordwrap').find_all('ul')[1].get_text()
				except:
					mb_skills = ''
					


				data = {
						'title': title,
						'company': company,
						'city': city,
						'employment': employment,
						'url': url,
						'skills': skills,
						'mb_skills':mb_skills,
																
				}
			
				# result = []
				# result.append(data)
				# print(result)
				self.write_csv(data, str(self.message), str(self.chat_id))
				#print(json.dumps(data,indent=2, ensure_ascii=False))
			else:
				continue


	
			

def read_file(filename):
	with open(filename, 'r') as f:
		return f.read().split('\n')
		




