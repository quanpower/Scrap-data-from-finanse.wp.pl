import requests
import csv
import re
import os
import time
from bs4 import BeautifulSoup
import download_names_wp 

stock_names, stock_ids = download_names_wp.downloadNames()

try:
	os.remove('indicators.csv')
	print 'Old file removed.'
except Exception:
	pass

for name in stock_ids:
	try:
		skip = False
		url_base = 'http://finanse.wp.pl/isin,'+name+',notowania-podsumowanie.html'
		r = requests.get(url_base)
		data = r.text
		soup = BeautifulSoup(data)
		print name, 'URL captured. Parsing...'
	except Exception, err:
		print 'Could not connect to URL', err
	try:
		for ul in soup.find_all("ul", { "class" : "zmiany" }):
			zmiany_raw = ul.get_text().encode('utf-8').replace(",",".").replace('%','').replace('+','')
			t1 = zmiany_raw.split('\n')[2].split(': ')[1]
			m1 = zmiany_raw.split('\n')[3].split(': ')[1]
			m3 = zmiany_raw.split('\n')[4].split(': ')[1]
			m6 = zmiany_raw.split('\n')[5].split(': ')[1]
			r1 = zmiany_raw.split('\n')[6].split(': ')[1]
			r3 = zmiany_raw.split('\n')[7].split(': ')[1]
			print t1, m1, m3, m6, r1, r3, '(%)'

			if t1 == '0.00' or m1 == '0.00':
				print 'No time % change. Skipping...'
				skip = True
		if not skip:		
			for elem in soup(text=re.compile(r'C/Z')):
				cz = elem.parent.parent.get_text().replace(' ','').replace(',','.').split(':')[1]
				print 'Cena / Zysk', cz
			for elem in soup(text=re.compile(r'C/Wk')):
				print elem.parent.parent.get_text()
				cwk = elem.parent.parent.get_text().replace(' ','').replace(',','.').split(':')[1]
				print 'Cena / Wartosc ksiegowa:', cwk
			for elem in soup(text=re.compile(r'C/EBITDA')):
				cebitda = elem.parent.parent.get_text().replace(' ','').replace(',','.').split(':')[1]
				print 'Cena / EBITDA:', cebitda
			for elem in soup(text=re.compile(r'Kapitalizacja')):
				kapitalizacja = elem.parent.encode('utf-8').replace('<div>', '').replace('</div>', '').replace(' ','').split('m')[0].split(':')[1].replace(',', '.')
				print 'Kapitalizacja:', kapitalizacja, '(mln PLN)'

			if cz and cwk and cebitda == '-':
					print 'No indicators. Skipping...'
					skip = True
			else:
				print 'Row seems ok. Writing...'

	except Exception as e:
		print 'sth went wrong during parsing text.', e

	print 'Done', stock_ids.index(name)*100/len(stock_ids),'%'
  	time.sleep(0.1)

	if not skip:
		with open('indicators.csv', 'ab') as indicators:
			writer = csv.writer(indicators, delimiter=";")
			#writer.writerow("name; 1t; 1m; 3m; 6m; 1r; 3r; cz; cwk; cebitda; kapitalizacja")
			writer.writerow([stock_names[stock_ids.index(name)], name, t1, m1, m3, m6, r1, r3, cz, cwk, cebitda, kapitalizacja])
