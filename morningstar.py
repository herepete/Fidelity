#!/usr/bin/python3.6
import pdb
import bs4
import requests
import csv
import os
import json

os.system('clear')


def read_in_lookup():
    #readin in lookup
    global data
    filetocheck='Fundperformance.txt'
    with open(filetocheck, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

read_in_lookup()

#urltotest="https://www.morningstar.co.uk/uk/funds/snapshot/snapshot.aspx?id=F0GBR04DTK&tab=1"


def grunge_and_print(urltotest):
    res=requests.get(urltotest)
    soup =bs4.BeautifulSoup(res.text,'html.parser')
    tables_from_site=soup.select('#returnsTrailingDiv > table  ')
    #pdb.set_trace()

    try:
        for i in tables_from_site[0]:
            #get into string
            templine=i.get_text(" ", strip=True)
            #get into list
            templist=[]
            templist=templine.split(" ")
            #show 3 months 1 year 3 year
            try:
                if ("Months" in templist[1]) and ("3" in templist[0]) :
                    # we are rebuilding the list here and formating the output to look nicer
                    rebuilt_list=templist[0]+" "+templist[1]
                    new_list=[]
                    new_list.append(rebuilt_list)
                    new_list.append(templist[2])
                    new_list.append(templist[3])
                    new_list.append(templist[4])
                    print (new_list[0].ljust(25), end='')
                    print (new_list[1].ljust(25), end='')
                    print (new_list[2].ljust(25), end='')
                    print (new_list[3].ljust(25))
                if (templist[1]=="Year") and ("1" in templist[0]) :

                    rebuilt_list=templist[0]+" "+templist[1]
                    new_list=[]
                    new_list.append(rebuilt_list)
                    new_list.append(templist[2])
                    new_list.append(templist[3])
                    new_list.append(templist[4])
                    print (new_list[0].ljust(25), end='')
                    print (new_list[1].ljust(25), end='')
                    print (new_list[2].ljust(25), end='')
                    print (new_list[3].ljust(25))
                if ("Years" in templist[1]) and ("3" in templist[0]) :
                    # we are rebuilding the list here and formating the output to look nicer
                    rebuilt_list=templist[0]+" "+templist[1]
                    new_list=[]
                    new_list.append(rebuilt_list)
                    new_list.append(templist[3])
                    new_list.append(templist[4])
                    new_list.append(templist[5])
                    print (new_list[0].ljust(25), end='')
                    print (new_list[1].ljust(25), end='')
                    print (new_list[2].ljust(25), end='')
                    print (new_list[3].ljust(25))

            except:
                #print ("Sorry i errored")
                pass
    except:
        print ("Sorry i errored")
        pass

read_in_lookup()
for i in data:
    #pdb.set_trace()
    print (i[0])
    print ("                         Total Returns            +/- Category             +/- Category Index")
    #grunge_and_print(i[1])
    try:
        grunge_and_print(i[1])
    except:
        print ("Sorry i errored")

