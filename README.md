Simple Python Stock Analysis Tool (for Polish GPW)
=============================

Python script, which gets stocks data from finanse.wp.pl and draws a chart with matplotlib. Based on sentdex tutorial series (http://www.youtube.com/watch?v=u6Xd3kRHhJI), adapted to polish stock market. The project is being extended.

Files:
- indicators.csv - list of stocks and papers possible to download, the file also contains some indicators for each stock (P/E, P/EBITDA etc.) This data is scrapped from wp.pl websites.
- finanse_wp.py - code responsible for downloading data, drawing a chart and counting all indicators.
- get_indicators.py - launches a scrapper, which runs through all stocks on finanse.wp.pl and collects the most important indicators. Outputs a CSV file, which may be later used for example in MS Excel.
- download_names_wp.py - function, which downloads a list of stocks. Returns a list.


TODO:
- fix the code to make it reusable and clear. The scraper should be easily adapted to be used on other financial websites.
- optimize the get_indicators.py script
- translate comments to english
- add the code done with sentdex pattern recognition series and adapt it to this data.
- enchance GUI - add some parameters to allow some changes in graphs.
- ...

I'd be happy to cooperate on this project. PM me if you're interested. 
