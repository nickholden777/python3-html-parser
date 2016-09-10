from urllib.request import urlopen
from bs4 import BeautifulSoup


def data_url(link, f):
	url = urlopen(link)
	data_parse = url.read()
	data_parse = data_parse.decode('windows-1251', 'ignore')
	url.close()

	soup = BeautifulSoup(data_parse, 'html.parser')
	table_string = soup.find('table', id='tab_main1')

	massive = list(table_string.findAll('tr'))
	len_massive = len(massive)

	i = int(2)
	while i < len_massive:
		td = list()
		td.append(massive[i].select_one('td:nth-of-type(1)'))
		td.append(massive[i].select_one('td:nth-of-type(2)'))
		td.append(massive[i].select_one('td:nth-of-type(4)'))
		td.append(massive[i].select_one('td:nth-of-type(8)'))

		data_list = ''
		data_list += str('<tr>')
		for item in td:
			data_list += str(item)
		data_list += str('</tr>')

		success = f.write(data_list)
		i = i + 1
	print('Has been written ' + str(len_massive) + 'string')	


def parse_count_page(count_page):
	massive = list(count_page.findAll('a'))
	len_massive = len(massive)
	if len_massive > 0:
		f = open('main.xls', 'w', encoding='utf-8')
		f.write(str("""<table>
			<thead>
			<tr>
				<td>Name</td>
				<td>R1</td>
				<td>Long</td>
				<td>Price</td>
			</tr>
			</thead>
			<tbody>"""))
		for page in massive:
			link = host_name + page.get('href')
			data_url(link, f)
		f.write(str('</tbody></table>'))	
		f.close()	
	else:
		print('No goods for this address')
		return False	


def check_url(url):
	open_url = urlopen(url)
	data_parse = open_url.read()
	data_parse = data_parse.decode('windows-1251', 'ignore')
	open_url.close()
	soup = BeautifulSoup(data_parse, 'html.parser')
	count_page = soup.find('div', id='products_nav_list')
	if not count_page:
		print('Such address doesn`t exist')
		return False
	parse_count_page(count_page)


url = 'http://mc.ru/page.asp/region/speterburg/metalloprokat/ugolok_ravn'
host_name = 'http://mc.ru'
check_url(url)

