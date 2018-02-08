from Parser import Parser, read_file
from random import choice

__author__ = 'bzdvdn'

class WorkParser(Parser):
	pass


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