from Parser import *

__author__ = 'bzdvdn'

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



useragent = {'User-Agent': choice(read_file('useragent.txt'))}

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



					


#https://rabota.ua/jobsearch/vacancy_list?keyWords=python
















		
