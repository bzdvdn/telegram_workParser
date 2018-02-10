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
class HHruParser(Parser):

	def get_total_pages(self, html):
		soup = BeautifulSoup(html, "lxml")
		pages = soup.find('div', class_='paging').find_all('a',class_='paging-item')[-2].get('href')
		total_pages = int(pages.split('=')[-1]) + 1
		return int(total_pages)



	def get_pages_data(self, html):
		soup = BeautifulSoup(html, "lxml")
		ads = soup.find_all('li', class_='vacancy-short')

		for index, iterator in enumerate(ads):
			name = iterator.find('div', class_='vacancy-short__name').text.strip().lower()

			if str(self.message).lower() in name:
				try:
					title = iterator.find('div', class_='vacancy-short__name').text.strip().lower()
					publicated = iterator.find('div', class_='vacancy-short-footer').find('div', class_='vacancy-short-footer-item').find('div', class_="vacancy-short__pubdate").text.strip()
					city = iterator.find('span', class_='vacancy-short__city').text
					company = iterator.find('div', class_='vacancy-short__company').text.strip()
					url = iterator.find('a', class_='vacancy-short__link-overlay').get('href')
					print('{} - index, url - {}'.format(index,url))
				except Exception as e:
					print(e)
					continue

				try:
					page = self.get_html(url, useragent)
					desc_soup = BeautifulSoup(page, 'lxml')
					exp = desc_soup.find('div', class_="vacancy__info").find_all('div')[-2].text.strip()
					employment = desc_soup.find('div', class_="vacancy__info").find_all('div')[-1].text.strip()
				except Exception as e:
					print(e)
					continue
				try:
					skills = desc_soup.find('div', class_='vacancy__description usergenerate').find_all('ul')[1].get_text()
				except:
					skills = ''

				try:
					mb_skills = desc_soup.find('div', class_='vacancy__description usergenerate').find_all('ul')[0].get_text()
				except:
					mb_skills = ''	


				data = {
						'title': title + '--' + publicated + '--' + exp,
						'company': company,
						'city': city,
						'employment': employment,
						'skills': skills,
						'mb_skills': mb_skills,
						'url': url										
				}
			
				self.write_csv(data, str(self.message), str(self.chat_id))
			else:
				continue


class RabotauaParser(Parser):

	def get_total_pages(self, html):
		soup = BeautifulSoup(html, "lxml")
		page = soup.find_all('tr')[-1].find('td').find('dl').find_all('dd')[-2].find('a').get('href')
		total_pages = page.split('=')[-1]
		return int(total_pages)

	def get_pages_data(self, html):
		soup = BeautifulSoup(html, "lxml")
		ads = soup.find('table', class_='f-vacancylist-tablewrap').find_all('tr')[0:-1]

		for index, iterator in enumerate(ads, start=1):
			name = soup.find('tr').find('td').find('article', class_='f-vacancylist-vacancyblock').find('div',class_='fd-f-left').find('div', class_='fd-f1').find('h3').text.strip()

			try:
				title = iterator.find('td').find('article', class_='f-vacancylist-vacancyblock').find('div',class_='fd-f-left').find('div', class_='fd-f1').find('h3').text.strip()
				company = iterator.find('td').find('article', class_='f-vacancylist-vacancyblock').find('div',class_='fd-f-left').find('div', class_='fd-f1').find('a', class_='f-text-dark-bluegray f-visited-enable').text.strip()
				city = iterator.find('td').find('article', class_='f-vacancylist-vacancyblock').find('div',class_='fd-f-left').find('div', class_='fd-f1').find('div', class_='f-vacancylist-characs-block fd-f-left-middle').find('p', class_='fd-merchant').text.strip()
				url = iterator.find('td').find('article', class_='f-vacancylist-vacancyblock').find('div',class_='fd-f-left').find('div', class_='fd-f1').find('h3').find('a').get('href')
				print('{} - index, url - {}'.format(index,url))
			except Exception as e:
				print('{} - index'.format(index))
				print(e)				
			try:
				page = self.get_html('https://rabota.ua' + url, useragent)
				desc_soup = BeautifulSoup(page, "lxml")
			except Exception as e:
				print(e)
			try:
				employment = desc_soup.find('div', class_='d_content').find('div', class_='d_des').find_all('ul')[2].text
			except:
				print('employment')
				employment = '----'

			try:
				skills = desc_soup.find('div', class_='d_content').find('div', class_='d_des').find_all('ul')[4].text
			except:
				print('skill')
				skills = ''

			try:
				mb_skills = skills = desc_soup.find('div', class_='d_content').find('div', class_='d_des').find_all('ul')[5].text
			except:
				print('mb_skill')
				mb_skills = ''

			data = {
					'title': title,
					'company': company,
					'city': city,
					'employment': employment,
					'skills': skills,
					'mb_skills': mb_skills,
					'url': url	
																
				}

			self.write_csv(data, str(self.message), str(self.chat_id))
			#print(json.dumps(data,indent=2, ensure_ascii=False))
	
			

def read_file(filename):
	with open(filename, 'r') as f:
		return f.read().split('\n')


useragent = {'User-Agent': choice(read_file('useragent.txt'))}

def workparse(msg,chat_id):
		p = Parser(msg,chat_id)
		url = 'https://www.work.ua/jobs-' + p.message + '/'
		base_url = 'https://www.work.ua/jobs-' + p.message + '/?'
		page = 'page='
		total_pages = p.get_total_pages(p.get_html(url))
		

		for i in range(1, total_pages+1):
			url_gen = base_url + page + str(i)
			html = p.get_html(url_gen, useragent)
			p.get_pages_data(html)
	


def hhru_parse(msg, chat_id):
		p = HHruParser(msg,chat_id)
		url = 'https://m.hh.ru/vacancies?text=' + str(p.message)
		base_url = 'https://m.hh.ru/vacancies?text=' + str(p.message) 
		page = '&page='
		total_pages = p.get_total_pages(p.get_html(url,useragent))
		

		for i in range(1, total_pages+1):
			url_gen = base_url + page + str(i)
			html = p.get_html(url_gen, useragent)
			p.get_pages_data(html)




def rabotaua_parser(msg, chat_id):
		p = RabotauaParser(msg,chat_id)
		url = 'https://rabota.ua/jobsearch/vacancy_list?keyWords=' + str(p.message)
		base_url = 'https://rabota.ua/jobsearch/vacancy_list?keyWords=' + str(p.message) 
		page = '&pg='
		total_pages = p.get_total_pages(p.get_html(url,useragent))
		

		for i in range(1, 5):
			url_gen = base_url + page + str(i)
			html = p.get_html(url_gen, useragent)
			p.get_pages_data(html)


if __name__ == '__main__':
	rabotaua_parser('python', '2335345')