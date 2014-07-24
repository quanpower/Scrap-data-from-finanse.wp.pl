'''
Script counts the average turnover on all stocks on GPW and compares it to the yesterday turnover. If it's bigger than the parameter-critical value,
it saves the stock id to the turnover_check file.
Code needs a lot of work - it's just made to work.
'''

from xml.dom import minidom
import urllib2
import numpy as np
import matplotlib.dates as mdates
import csv
import download_names_wp

stock_names, stock_ids = download_names_wp.downloadNames()

def turnoverAlert(stock, crit_value):
	'''Pobranie xml z finanse.wp.pl i zapisanie go do list - takiej samej jak w Yahoo API'''
	turnover = []
	try:
		urlToVisit = 'http://finanse.wp.pl/isin,' + stock + ',range,3L,split,1,int,1day,graphdata.xml' 
		xml = urllib2.urlopen(urlToVisit)
		dom = minidom.parse(xml)
		childNodes = dom.childNodes
		days = dom.getElementsByTagName('item')
		'''Przepisanie danych z XMLa do list'''
		for day in days:
			turnover.append(float(day.getAttribute('obr')))
	except Exception, err:
		print str(err)

	av_turnover = reduce(lambda x, y: x + y, turnover) / len(turnover)
	last_turnover = turnover[-2]
	crit_turnover = av_turnover * crit_value
	print 'Last turnover', last_turnover
	print 'Average turnover', av_turnover
	if last_turnover > crit_turnover:
		percent_change = int(((last_turnover - av_turnover)/av_turnover) * 100)
		print 'Detected big movement!', stock, percent_change, '%'
		with open('turnover_check.txt', 'ab') as turnover_file:
			turnover_file.write(stock + ' ' + stock_names[stock_ids.index(stock)] + ' ' + str(percent_change) + '%\n')
	else:
		print 'No big movement detected.'

for stock in stock_ids:
	turnoverAlert(stock, 5)