import urllib2
import numpy as np
import matplotlib
import pylab
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick #zobaczyc candlestick2
matplotlib.rcParams.update({'font.size': 10})

def RsiFunc(prices, n=14):
    ''' Funkcja odpowiedzialna za kalkulacje RSI '''
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)
    return rsi

def movingAverage(values, window):
    ''' Funkcja odpowiedzialna za kalkulacje srednich kroczacych '''    
    weights = np.repeat(1.0, window)/ window
    smas = np.convolve(values, weights, 'valid')
    return smas

def expMovingAverage(values, window):
    ''' Funkcja odpowiedzialna za kalkulacje wykladniczej sredniej kroczacej'''
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a

def computeMACD(x, slow=26, fast=12):
    ''' Funkcja odpowiedzialna za kalkulacje MACD '''
    emaslow = expMovingAverage(x, slow)
    emafast = expMovingAverage(x, fast)
    return emaslow, emafast, emafast-emaslow

def graphData(stock, MA1, MA2):
    ''' Funkcja odpowiedzialna za wygenerowanie wykresu '''   
    try:
        ''' Pobranie danych z API Yahoo '''
        try:
            print('pulling data on',  stock)
            urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=3y/csv'
            stockFile = []
            try:
                sourceCode = urllib2.urlopen(urlToVisit).read()
                splitSource = sourceCode.split('\n')
                for eachLine in splitSource:
                    splitLine = eachLine.split(',')
                    if len(splitLine) == 6:
                        if 'values' not in eachLine:
                            stockFile.append(eachLine)
            except Exception, e:
                print(e, 'failed to organize data.')
        except Exception, e:
            print(e, 'failed to pull data.')
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile, delimiter=",", unpack=True, converters={0: mdates.strpdate2num("%Y%m%d")})
        x = 0
        y = len(date)
        candleAr = []
        while x<y:
            appendLine = date[x], openp[x], closep[x], highp[x], lowp[x], volume[x]
            candleAr.append(appendLine)
            x += 1

        av1 = movingAverage(closep, MA1)
        av2 = movingAverage(closep, MA2)
        sp = len(date[MA2 - 1:])

        fig = plt.figure(facecolor='#07000d')

        ''' Kod odpowiedzialny za wykres Price '''
        ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4, axisbg="#07000d")
        ax1.yaxis.label.set_color('w')
        ax1.spines['bottom'].set_color("#5998ff")
        ax1.spines['top'].set_color("#5998ff")
        ax1.spines['left'].set_color("#5998ff")
        ax1.spines['right'].set_color("#5998ff")
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='both'))
        ax1.tick_params(axis='y', colors='w')
        ax1.tick_params(axis='x', colors='w')
        ax1.grid(True, color='w')
        plt.ylabel("Stock Price & Volume")
        candlestick(ax1, candleAr[-sp:], width=.7, colorup='#53c156', colordown='#ff1717')

        ''' Kod odpowiedzialny za wyrysowanie srednich kroczacych '''
        label1 = str(MA1) + ' SMA'
        label2 = str(MA2) + ' SMA'
        ax1.plot(date[-sp:], av1[-sp:], '#e1edf9', label=label1, linewidth=1.3)
        ax1.plot(date[-sp:], av2[-sp:], '#4ee6fd', label=label2, linewidth=1.3)

        ''' Legenda '''
        maLeg = ax1.legend(loc=9, ncol=2, fancybox=True, prop={'size': 8})
        maLeg.get_frame().set_alpha(0.4)

        textEd = pylab.gca().get_legend().get_texts()
        pylab.setp(textEd[0:5], color='w')

        ''' Kod odpowiedzialny za wykres RSI '''
        ax0 = plt.subplot2grid((6,4), (0,0), rowspan=1, colspan=4, sharex=ax1, axisbg='#07000d')
        rsi = RsiFunc(closep)
        rsiCol = '#c1f9f7'
        posCol = '#386d13'
        negCol = '#8f2020'
        ax0.plot(date[-sp:], rsi[-sp:], rsiCol, linewidth=1.5)
        ax0.axhline(70, color=negCol)
        ax0.axhline(30, color=posCol)
        ax0.fill_between(date[-sp:], rsi[-sp:], 70 , where=(rsi[-sp:]>=70), facecolor=negCol, edgecolor=negCol)
        ax0.fill_between(date[-sp:], rsi[-sp:], 30 , where=(rsi[-sp:]<=30), facecolor=posCol, edgecolor=posCol)
        ax0.spines['bottom'].set_color("#5998ff")
        ax0.spines['top'].set_color("#5998ff")
        ax0.spines['left'].set_color("#5998ff")
        ax0.spines['right'].set_color("#5998ff")
        ax0.yaxis.label.set_color('w')
        ax0.tick_params(axis='y', colors='w')
        ax0.set_yticks([30, 70])
        plt.ylabel('RSI')

        ''' Kod odpowiedzialny za wykres Volume '''
        ax1v = ax1.twinx()
        volumeMin = 0
        ax1v.fill_between(date[-sp:], volumeMin, volume[-sp:], facecolor='#00ffe8', alpha='.4')
        ax1v.spines['bottom'].set_color("#5998ff")
        ax1v.spines['top'].set_color("#5998ff")
        ax1v.spines['left'].set_color("#5998ff")
        ax1v.spines['right'].set_color("#5998ff")
        ax1v.tick_params(axis='x', colors='w')
        ax1v.tick_params(axis='y', colors='w') 
        ax1v.grid(False)
        ax1v.axes.yaxis.set_ticklabels([])
        ax1v.set_ylim(0, 2*volume.max()) 

        ''' Kod odpowiedzialny za wykres MACD '''
        ax2 = plt.subplot2grid((6,4), (5,0), sharex=ax1, rowspan=1, colspan=4, axisbg='#07000d')
        nslow = 26
        nfast = 12
        nema = 9
        fillcolor = '#00ffe8'

        [emaslow, emafast, macd] = computeMACD(closep)
        ema9 = expMovingAverage(macd, nema)

        ax2.plot(date[-sp:], macd[-sp:], color='#4ee6fd', linewidth=2)
        ax2.plot(date[-sp:], ema9[-sp:], color='#e1edf9', linewidth=1)
        ax2.fill_between(date[-sp:], macd[-sp:]-ema9[-sp:], 0, alpha=.5, facecolor=fillcolor, edgecolor=fillcolor)
        plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
        plt.ylabel('MACD', color='w')
        ax2.tick_params(axis='y', colors='w')
        ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))

        ax2.spines['bottom'].set_color("#5998ff")
        ax2.spines['top'].set_color("#5998ff")
        ax2.spines['left'].set_color("#5998ff")
        ax2.spines['right'].set_color("#5998ff")
        ax2.tick_params(axis='x', colors='w')
        ax2.tick_params(axis='y', colors='w') 

        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)

        ''' Ogolne ustawienia koncowe ''' 
        plt.subplots_adjust(left=.09, bottom=.18, right=.94, top=.95, wspace=.20, hspace=0)
        plt.suptitle(stock + " Stock Price", color='w')
        plt.setp(ax0.get_xticklabels(), visible=False)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.show()

    except Exception, e:
        print "Failed main loop" + str(e)

''' Rysowanie '''
while True:
    stockToUse = raw_input('Stock to chart (YAHOO SYMBOL): ')
    graphData(stockToUse, 20, 200)

