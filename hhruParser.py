from Parser import *

__author__ = 'bzdvdn'

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

useragent = {'User-Agent': choice(read_file('useragent.txt'))}

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

	

	
if __name__ == '__main__':
	hhru_parse('python', '123453564')

