#!/usr/bin/python3.6
import pdb
import bs4
import requests
import csv
import os
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
args=parser.parse_args()
from time import sleep

#Global variables
os.system('clear')
duplicate_holdings=[]
portfolio_link=[]
time_delay=1


if args.verbose:
    print("verbosity turned on")
#data = data from lookup
data=[]
portfolio_link=[]

def understand_api_data(soupin):

    #this function will convert <class 'bs4.BeautifulSoup'> into a string and a dictonary
    loopcount=0
    print ("Raw data Length-",len(soupin))
    #pdb.set_trace()
    if type(soupin) is not dict:
        soupin_string = str(soupin)
        soupin_json = json.loads(soupin_string)
    else:
        soupin_json = soupin
    print ("Dictionary Length-",len(soupin_json))

    print("Dictonary looks like this...")
    print()
    #pdb.set_trace()
    for i,j in soupin_json.items():
        loopcount=loopcount+1
        print (loopcount," ",i,"=",j)
        print()

def api_get_fund_holdings(fundname):

    #the data we want is deeply burried within the data , these variables help us find it
    apiurl_in=portfolio_link['fportfolio']
    intrestedin="holdings"
    intresedin2="portfolioHoldings"

    #any incoming request use api to get data into a dict
    res=requests.get(apiurl_in)
    res.raise_for_status()
    soup =bs4.BeautifulSoup(res.text,'html.parser')
    string_soup=str(soup)
    json_soup=json.loads(string_soup)
    #understand_api_data(json_soup)
    # narrow down dict to just what we need
    json_intrested_in=json_soup[intrestedin]
    json_intrested_in=json_intrested_in[intresedin2]

    global duplicate_holdings
    #duplicate_holdings.append([Secuirty_name,fundname])

    #print ()
    for i in json_intrested_in:
        dicti=dict(i)
        duplicate_holdings.append([dicti['securityName'],fundname])
        #print (dicti['securityName']," ",float(dicti['weighting']))
    #return(json_intrested_in)

def sort_out_duplicates():

    global duplicate_holdings
    duplicate_holdings.sort()
    lastitem=""
    lastitem_fund=""
    rebuild_list=[]

    for i in duplicate_holdings:
        #if i[1]=="Fundsmith":
        #    print (i[0])
        #    pdb.set_trace()

        if (i[0]==lastitem) and (i[1]==lastitem_fund):
                pdb.set_trace()
        if i[0] ==lastitem:
            rebuild_list.append([lastitem,lastitem_fund])
            rebuild_list.append([i[0],i[1]])
            lastitem=i[0]
            lastitem_fund=i[1]
        lastitem=i[0]
        lastitem_fund=i[1]
    if not rebuild_list:
        print ("You don't have any overlap in your portfolio...")
    else:
        print ("Here is what is duplicated in the portfolio...")
        #i seem to have some edge cases where duplicates are sneaking through
        #lets do a final remove duplicate
        new_rebuild_list=[]
        for elem in rebuild_list:
            if elem not in new_rebuild_list:
                new_rebuild_list.append(elem)
        for j in new_rebuild_list:
            print (j[0].ljust(25), end='')
            print (j[1].ljust(25), end='')
            print ()

def strip_chars(input1):

    # to deal with occsional odd input
    if "/" in input1:
        # the only case i have seen this is marlbourugh if another one has the same slash and is in pounds this is going to error
        hacked=input1.split("/")
        hacked=hacked[0]
        hacked=hacked.replace('p','')
        hacked=hacked.replace('£','')
        hacked=hacked.replace(',','')
        hacked=int(float(hacked))/100
    elif "p" in input1:
        #converting pence into pounds
        hacked=input1.replace('p','')
        hacked=int(float(hacked))/100
    else:
        hacked=input1.replace('p','')
        hacked=hacked.replace('£','')
        hacked=hacked.replace(',','')

    return hacked

def fidelity_api(isin):
    #read in isin number and format API urls
    #isin=123456789
    #not sure if this is the best approach espically for large inputs
    sleep(time_delay)
    fkeystatitics=(f"https://www.fidelity.co.uk/factsheet-data/factsheet/{isin}/key-statistics")
    fgrowth=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/growthChart")
    finsight=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/filInsight")
    fperformance=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/performance")
    fportfolio=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/portfolio")
    friskandrating=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/riskAndRating")
    global portfolio_link
    portfolio_link={}
    portfolio_link.update({'fgrowth':fgrowth,'finsight':finsight,'fperformance':fperformance,'fportfolio':fportfolio,'friskandrating':friskandrating,'fkeystatitics':fkeystatitics})

    if args.verbose:
        print("***From  > 'fidelity_api()***'")
        print ("***",fkeystatitics,"***")
        print ("***",fgrowth,"***")
        print ("***",finsight,"***")
        print ("***",fperformance,"***")
        print ("***",fportfolio,"***")
        print ("***",friskandrating,"***")
        print ("")


def getprice_soup():
    sleep(time_delay)
    url_to_check=portfolio_link['fkeystatitics']
    res=requests.get(url_to_check)
    res.raise_for_status()
    soup =bs4.BeautifulSoup(res.text,'html.parser')
    name_box = soup.find('h3', attrs={'class': 'detail_value'})
    #the above line is taken from inspecting (in browser right click object > inspect) the webpage, as "detail value" is unique its an easy way to strip data down
    name_box1=list(name_box)
    res = ' '.join(map(str, name_box1))
    #convert to list and then string , hackey =yes
    return res



def read_in_lookup():
    #readin in lookup
    global data
    with open('stockstocheck.txt', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    if args.verbose:
        print("***From incoming data  > 'read_in_lookup()***'")
        for i in data:
            print ("***",i,"***")
            #if i[0][0] is not "#":
            #    fidelity_api(isin=i[1])

        print()


def price_movement(current_price,historic_price):
    # rather messey but input is reverting to string
    # below hack convert say 322.18 (string) to 322 (int)
    cprice=float(current_price)
    hprice=float(historic_price)
    #strip out any chars like p or £
    if (cprice==hprice):
        return (0)
    else:
        price_diff=cprice-hprice
        percent_diff=(price_diff/hprice)*100
        percent_diff=round(percent_diff,1)
        return(percent_diff)

def doing_stuff():

    print ("Ok i am going to start but due to rate limiting each request will wait {} second before running ".format(time_delay))

    

def menu_choice():
    # offer users choice

    print ("Enter your options:")
    print ("1) For current % change in Fidelity Pension")
    print ("2) Overlapping portfolio")
    #print ("3) Analysis Funds")
    #print ("4) Performance v Index")
    #print ("5) Overall Summary")
    response=input("")
    return (response)


read_in_lookup()
choice=menu_choice()

if choice =="1":

    doing_stuff()

    #get data in the right format
    build_list=[]
    for i in data:
        fidelity_api(isin=i[1])
        if i[0][0] is not "#":

            price = getprice_soup()
            price = strip_chars(price)

            #pdb.set_trace()

            hist_price=i[2]
            hist_price=strip_chars(hist_price)

            try:
                movement=price_movement(price,hist_price)
                build_list.append([i[0],price,hist_price,movement])
            except:
                build_list.append(i[0],hist_price,price,"error")


    #lets print it all
    build_list_header=["Fund","Current Price","Historic Price","% Change"]
    for header in build_list_header:
        print (header.ljust(25), end='')
    print()

    for lineitem in build_list:
        for detailitem in lineitem:
            dt=str(detailitem)
            print (dt.ljust(25), end='')
        print()


elif choice =="2":
    #build database of holdings
    doing_stuff()
    for i in data:
        if i[0][0] is not "#":
            fidelity_api(isin=i[1])
            api_get_fund_holdings(fundname=i[0])
    #sort duplicates and print
    sort_out_duplicates()

elif choice =="3":
    pass
elif choice =="4":
    pass
elif choice =="5":
    pass
else:
    print ("I am not programmed for this...")


