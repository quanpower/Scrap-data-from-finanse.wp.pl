from Tkinter import *
import csv

nameAr = []
codeAr = []

with open('stocks.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
    	nameAr.append(row[0])
    	codeAr.append(row[1])

def select():
	# wywolanie wykresu dla danego codeAr
	print 'nothing yet'

master = Tk()
master.geometry("%dx%d+%d+%d" % (400, 480, 600, 600))

scrollbar = Scrollbar(master)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(master, yscrollcommand=scrollbar.set)
for i in range(1000):
    listbox.insert(END, nameAr[i])
listbox.pack(side=LEFT, fill=BOTH)

scrollbar.config(command=listbox.yview)

mainloop()