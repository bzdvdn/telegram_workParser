from Parser import *

__author__ = 'bzdvdn'

class WorkParser(Parser):
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
					page = self.get_html(url, useragent)
					desc_soup = BeautifulSoup(page, 'lxml')
					company = desc_soup.find('dl', class_='dl-horizontal').find('a').find('b').get_text().strip()
					city = desc_soup.find('dl', class_='dl-horizontal').findAll('dd')[-2].get_text().strip()
					employment = desc_soup.find('dl', class_='dl-horizontal').findAll('dd')[-1].get_text().strip()
					description = desc_soup.find('div', class_='wordwrap').get_text().strip()
				except Exception as e:
					print(e)
					continue


				data = {
						'title': title,
						'company': company,
						'city': city,
						'employment': employment,
						'url': url,
						'description': description
																
				}
			
				# result = []
				# result.append(data)
				# print(result)
				self.write_csv(data, str(self.message), str(self.chat_id))
				#print(json.dumps(data,indent=2, ensure_ascii=False))
			else:
				continue


useragent = {'User-Agent': choice(read_file('useragent.txt'))}



def workparse(msg,chat_id):
		p = WorkParser(msg,chat_id)
		url = 'https://www.work.ua/jobs-' + p.message + '/'
		base_url = 'https://www.work.ua/jobs-' + p.message + '/?'
		page = 'page='
		total_pages = p.get_total_pages(p.get_html(url))
		

		for i in range(1, total_pages+1):
			url_gen = base_url + page + str(i)
			html = p.get_html(url_gen, useragent)
			p.get_pages_data(html)

	

	
if __name__ == '__main__':
	workparse('python','12345')