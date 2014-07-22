'''
Download a list of all papers/stocks on finanse.wp.pl. 
'''
from xml.dom import minidom
import urllib2
import csv

def downloadNames():
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

	return names, values


