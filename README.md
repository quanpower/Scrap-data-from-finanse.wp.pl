Simple Python Stock Analysis Tool (for Polish GPW)
=============================

Python script, which gets stocks data from finanse.wp.pl and draws a chart with matplotlib. Based on sentdex tutorial series (http://www.youtube.com/watch?v=u6Xd3kRHhJI), adapted to polish stock market.

Files:
- stocks.csv - list of stocks and papers possible to download.
- download_names_wp.py - script, which downloads a list of names of stocks. Produces 'stocks.csv'
- yahoo_financy.py - code written based on tutorial series, downloads data from yahoo API
- finanse_wp.py - code responsible for downloading data, drawing a chart and counting all indicators.

TODO:
- fix the code to make it reusable and clear. The scraper should be easily adapted to be used on other financial websites.
- translate comments to english
- add the code done with sentdex pattern recognition series and adapt it to this data.
- enchance GUI - add some parameters to allow some changes in graphs.
- ...

I'd be happy to cooperate on this project. PM me if you're interested. 
