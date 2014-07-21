'''
Download a list of all papers/stocks on finanse.wp.pl. 
Output stocks.csv
'''
from xml.dom import minidom
import urllib2
import csv
from itertools import izip

urlToVisit = 'http://finanse.wp.pl/isin,PLOPTTC00011,stocks.xml'
xml = urllib2.urlopen(urlToVisit)
dom = minidom.parse(xml)
childNodes = dom.childNodes
stocks = dom.getElementsByTagName('item')

values = []
names = []

for name in stocks:
	names.append(str(name.getAttribute('name')))
	values.append(str(name.getAttribute('value')))

with open('stocks.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(izip(names, values))

