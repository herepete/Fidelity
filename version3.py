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
parser.add_argument("-t", "--timer", help="add timer to output to help troubleshoot",action="store_true")
parser.add_argument("-tt", "--etimer", help="a much more in depth add timer to output to help troubleshoot",action="store_true")
args=parser.parse_args()
from time import sleep

#Global variables
os.system('clear')
duplicate_holdings=[]
portfolio_link=[]
time_delay=0
large_fund_builder=[]

import time



if args.verbose:
    print("verbosity turned on")
#data = data from lookup
if args.timer:
    print("Timer turned on")
if args.etimer:
    print("Extreme Timer turned on")
data=[]
portfolio_link=[]


timer_stop=0
timer_start=0
timer_diffenence=0

etimer_stop=0
etimer_start=0
etimer_diffenence=0

def time_events(stop,start,stage):


    if args.timer:
        global timer_start,timer_stop,timer_diffenence
        if start==1:
            timer_start=time.perf_counter()
            timer_stop=0
            timer_diffenence=0
        if stop ==1:
            timer_stop=time.perf_counter()
            timer_diffenence=timer_stop-timer_start
            timer_diffenence_r=round(timer_diffenence,1)
            print ("***TIMER - ",stage," Took ",timer_diffenence_r)
            #pdb.set_trace()


            timer_start=0
            timer_diffenence=0



def e_time_events(stop,start,stage):

    if args.etimer:
        global etimer_start,etimer_stop,etimer_diffenence
        if start==1:
            etimer_start=time.perf_counter()
            etimer_stop=0
            etimer_diffenence=0
        if stop ==1:
            etimer_stop=time.perf_counter()
            etimer_diffenence=etimer_stop-etimer_start
            etimer_diffenence_r=round(etimer_diffenence,1)
            print ("***ETIMER - ",stage," Took ",etimer_diffenence_r)

            etimer_start=0
            etimer_diffenence=0


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
        print (loopcount," ",i)
        print()
    loopcount=0
    answer=input("check data, press i for interactive or anything else to continue")
    if answer=="i":
        pdb.set_trace()
        


    for i,j in soupin_json.items():
        loopcount=loopcount+1
        print (loopcount," ",i,"=",j)
        print()

def get_morning_star_rating(urlfund):
    #again getting hacky , i am searching for the term alhpa, the easy approach might be to
    #get the whole table in a list and then i can loop through it
    res=requests.get(urlfund)
    try:
        res.raise_for_status()
    except:
        #print ("the")
        if args.verbose:
            print ("urlfund=",urlfund," Errored") 
        return(0)

    soup =bs4.BeautifulSoup(res.text,'html.parser')
    test1=soup.find_all('td')

    #approach2 more manual map each field
    #in use
    #new approach get everything tables and go through it
    #pdb.set_trace()
    #3 and 5 year morning star return and risk values
    ty_ms_return=strip_html(str(soup.find_all('td')[1]))
    ty_ms_risk=strip_html(str(soup.find_all('td')[3]))
    fy_ms_return=strip_html(str(soup.find_all('td')[7]))
    fy_ms_risk=strip_html(str(soup.find_all('td')[9]))


    #clear up text
    #convert numbers into words
    #pdb.set_trace()
    #if (ty_ms_return =="Above Average" or ty_ms_return =="Average") and (fy_ms_return =="Above Average" or fy_ms_return =="Average"):
    if (ty_ms_return =="Above Average" or ty_ms_return =="High") and (fy_ms_return =="Above Average" or fy_ms_return =="High"):
        return(1)
    else:
        return(0)


def risk_measures_analysis(Alpha,Ir):

   pdb.set_trace() 

def api_get_fund_five_year_annualised(ofyears=5):

    api_tosearch=portfolio_link['fperformance']
    search1="timeFrameData"
    res=requests.get(api_tosearch)
    try:
        res.raise_for_status()
    except:
        return (0)
    soup =bs4.BeautifulSoup(res.text,'html.parser')
    string_soup=str(soup)
    json_soup=json.loads(string_soup)
    json_intrested_in=json_soup[search1]
    beat_index_score=0
    try:
        annual_performance=(json_intrested_in[10])['trailingReturnsValue']
        annual_performanceBenchmarkValue=(json_intrested_in[10])['trailingReturnsBenchmarkValue']
        beat_index_score=int(float(annual_performance)-float(annual_performanceBenchmarkValue))
        return (beat_index_score)
    except: 
        return (beat_index_score)
        


            



def api_get_fund_annual_performace(ofyears=5):

    beat_index=0

    #the data we want is deeply burried within the data , these variables help us find it
    api_tosearch=portfolio_link['fperformance']
    search1="yearlyData"

    #any incoming request use api to get data into a dict
    res=requests.get(api_tosearch)
    try:
        res.raise_for_status()
    except:
        #print("i have errored")
        #pdb.set_trace()
        return (0)

    soup =bs4.BeautifulSoup(res.text,'html.parser')
    string_soup=str(soup)
    json_soup=json.loads(string_soup)
    #understand_api_data(json_soup)
    #pdb.set_trace()
    
    # narrow down dict to just what we need
    json_intrested_in=json_soup[search1]
    
    startcount=0
    score_above_index=0
    for i in range(ofyears): 
        #pdb.set_trace()
        startcount=startcount-1
        tempitem=json_intrested_in[startcount:]
        annual_performance=(tempitem[0])['annualPerformanceValue']
        annual_performanceBenchmarkValue=(tempitem[0])['annualPerformanceBenchmarkValue']
        #pdb.set_trace()
        annual_difference_between_values=int(float(annual_performance)-float(annual_performanceBenchmarkValue))
        score_above_index=score_above_index+annual_difference_between_values

        if "-" in annual_performance and "-" in annual_performanceBenchmarkValue:
            pass
            #if args.verbose:
            #    print ("2 negative values found")
        elif "-" in annual_performance and  "-" not in annual_performanceBenchmarkValue:
            #the funs annual performance is negative and becnhamrk is positive
            pass
        elif "-" not in annual_performance and  "-" in annual_performanceBenchmarkValue:
            #becnhamrk negative and und positive
            beat_index=beat_index+1

        elif  annual_performance > annual_performanceBenchmarkValue:
            if args.verbose:
                print ("Api call-",api_tosearch)
                print ("record-",startcount,annual_performance," is bigger than  ",annual_performanceBenchmarkValue)
                print ("the full record looks like this")
                print (tempitem)

            beat_index=beat_index+1
        else:
            # not sure what this covers
            pass
            #if args.verbose:
            #    print ("performance is worse")
    #return(score_above_index)


    #pdb.set_trace()


    return (beat_index)


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

def get_allfidelityfunds():
    #api_test="https://lt.morningstar.com/api/rest.svc/9vehuxllxs/security/screener?page=1&pageSize=5000&sortOrder=LegalName%20asc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=FOGBR%24%24ALL_3521&securityDataPoints=SecId%7CName%7CTenforeId%7CholdingTypeId%7Cisin%7Csedol%7CCustomAttributes1%7CCustomAttributes2%7CCustomExternalURL1%7CCustomExternalURL2%7CCustomExternalURL3%7CCustomIsClosed%7CCustomIsFavourite%7CCustomIsRecommended%7CCustomMarketCommentary%7CQR_MonthDate%7CExchangeId%7CExchangeCode%7CCurrency%7CLegalName%7CCustomBuyFee%7CYield_M12%7COngoingCostEstimated%7CCustomCategoryId3Name%7CStarRatingM255%7CQR_GBRReturnM12_5%7CQR_GBRReturnM12_4%7CQR_GBRReturnM12_3%7CQR_GBRReturnM12_2%7CQR_GBRReturnM12_1%7CCustomMinimumPurchaseAmount%7CCustomAdditionalBuyFee%7CCustomSellFee%7CTransactionFeeEstimated%7CPerformanceFee%7CGBRReturnM0%7CGBRReturnM12%7CGBRReturnM36%7CGBRReturnM60%7CGBRReturnM120%7CTrackRecordExtension&filters=&term=&subUniverseId=MFEI"
    api_test="https://lt.morningstar.com/api/rest.svc/9vehuxllxs/security/screener?page=1&pageSize=5000&sortOrder=LegalName%20asc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=FOGBR%24%24ALL_3521&securityDataPoints=SecId%7CName%7CTenforeId%7CholdingTypeId%7Cisin%7Csedol%7CCustomAttributes1%7CCustomAttributes2%7CCustomExternalURL1%7CCustomExternalURL2%7CCustomExternalURL3%7CCustomIsClosed%7CCustomIsFavourite%7CCustomIsRecommended%7CCustomMarketCommentary%7CQR_MonthDate%7CExchangeId%7CExchangeCode%7CCurrency%7CLegalName%7CCustomBuyFee%7CYield_M12%7COngoingCostEstimated%7CCustomCategoryId3Name%7CStarRatingM255%7CQR_GBRReturnM12_5%7CQR_GBRReturnM12_4%7CQR_GBRReturnM12_3%7CQR_GBRReturnM12_2%7CQR_GBRReturnM12_1%7CCustomMinimumPurchaseAmount%7CCustomAdditionalBuyFee%7CCustomSellFee%7CTransactionFeeEstimated%7CPerformanceFee%7CGBRReturnM0%7CGBRReturnM12%7CGBRReturnM36%7CGBRReturnM60%7CGBRReturnM120%7CTrackRecordExtension&filters=&term=&subUniverseId=MFEI"
    #res=requests.get("https://www.fidelity.co.uk/planning-guidance/investment-finder/#?investmentType=funds&universeId=FOGBR$$ALL_3521&filtersSelectedValue=%7B%7D&page=1&perPage=10&sortField=legalName&sortOrder=asc&subUniverseId=MFEI")
    res=requests.get(api_test)
    res.raise_for_status()
    soup =bs4.BeautifulSoup(res.text,'html.parser')
    #understand_api_data(soupin=soup)
    links_with_text = []
    #for a in soup.find_all('a', href=True): 
    #    if a.text: 
    #        links_with_text.append(a['href'])
    string_soup=str(soup)
    json_soup=json.loads(string_soup)
    #count=0
    #for key,val in json_soup.items():
    #    count+=1
    #    print (count,key)
    just_rows=json_soup['rows']
    for funds in just_rows:
        fundname=funds['Name']
        isin_number=funds['isin']
        templist=[fundname,isin_number]
        large_fund_builder.append(templist)
    #for masslist in large_fund_builder:
    #    print (masslist)
    #pdb.set_trace()

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


def strip_html(input1):

    hacked=input1.replace('<td>','')
    hacked=hacked.replace('</td>','')
    hacked=hacked.replace('<td class="text-right">','')
    return (hacked)


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
    #sleep(time_delay)
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
    #sleep(time_delay)
    #pdb.set_trace()
    url_to_check=portfolio_link['fkeystatitics']
    res=requests.get(url_to_check)
    res.raise_for_status()
    soup =bs4.BeautifulSoup(res.text,'html.parser')
    name_box = soup.find('h3', attrs={'class': 'detail_value'})
    #the above line is taken from inspecting (in browser right click object > inspect) the webpage, as "detail value" is unique its an easy way to strip data down
    #beating_score=api_get_fund_annual_performace(ofyears)
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

def write_fidelty_funds_to_file(filename):

    import csv
    out_file = open(filename, 'w+', newline ='') 
    with out_file:
        write = csv.writer(out_file) 
        write.writerows(large_fund_builder) 
    len_list=len(large_fund_builder)
    print ("All done I have written out %s records to fidelity_funds.csv" % len_list)
    input("press a button to continue")
    os.system('clear')

def read_in_all_fidelity_funds_csv():

    import csv
    global all_funds_readin_master
    with open('fidelity_funds.csv', newline='') as f:
        reader = csv.reader(f)
        all_funds_readin_master = list(reader)

def status_of_funds(stage):

    number_of_funds=len(all_funds_readin_master)
    print ("")
    print (number_of_funds," Funds at this stage -",stage)
    #if int(number_of_funds < 10):
    #    for i in all_funds_readin_master:
    #        print (i)


def beating_index(beat=3,ofyears=5):
    #if you want a record of beating the index in 4 of the last 5  years use beat=4,ofyears=5
    #global number_of_funds
    #sleep(time_delay)
    global all_funds_readin_master
    new_all_funds_readin_master=[]
    countfunds=0
    beating_index_count=0
    global five_year_annualizedlist
    five_year_annualizedlist=[]
    num_funds_to_check=len(all_funds_readin_master)
    progress_bar=100/num_funds_to_check


    for i in all_funds_readin_master:
        fund_number=i[1]
        countfunds=countfunds+1
        #999
        if args.verbose:
            print ("****Working on fundnumber-",countfunds)
        
        #get api address
        if args.etimer:
            e_time_events(stop=0,start=1,stage="Beating index - read through records ")
        #998
        fidelity_api(isin=fund_number)
        #get score of times index has been in $last
        #api_get_fund_annual_performace(ofyears) was an approach to beat benchmark in 3 of 4 yerars but annualized return is probable a better becnhmark 
        #beating_score=api_get_fund_annual_performace(ofyears)
        beating_score=api_get_fund_five_year_annualised()
        #pdb.set_trace()
        if int(beating_score) > 3:
            new_all_funds_readin_master.append(fund_number)
            templistfive=(fund_number,beating_score)
            five_year_annualizedlist.append(templistfive)
            beating_index_count=beating_index_count+beating_score
            #print (fund_number,"yeh something positive found ",beating_score)
        else:
            pass
            #print (fund_number,"has a score of ",beating_score)
        if args.etimer:
            e_time_events(stop=1,start=0,stage="Beating index - read through records ")
        progress_count=round(progress_bar*countfunds,2)
        #print (progress_count,"% complete")
        #pdb.set_trace()
        if (countfunds==10) or (countfunds==25)  or (countfunds==50) or (countfunds==75) or (countfunds==100) or (countfunds==175) or (countfunds==250) or (countfunds==375) or (countfunds==500)  or(countfunds==750) or (countfunds==1000)  or (countfunds==1500) or (countfunds==2000)  or (countfunds==2500):
            print (progress_count,"% done")
    #pdb.set_trace()
    #global all_funds_readin_master
    #pdb.set_trace()
    all_funds_readin_master = new_all_funds_readin_master
    
    #pdb.set_trace()




        #pdb.set_trace()

def beating_morning_star_score(scoretobeat=4):
    #sleep(time_delay)
    global all_funds_readin_master
    beating_morning_star_score_list=[]
    num_funds_to_check=len(all_funds_readin_master)
    countfunds=0
    progress_bar=100/num_funds_to_check


    for i in all_funds_readin_master:
        countfunds=countfunds+1
        progress_count=round(progress_bar*countfunds,2)
        fund_number=i
        fidelity_api(isin=fund_number)
        urlfund=(f"https://www.fidelity.co.uk/factsheet-data/factsheet/{fund_number}/risk-and-rating")
        return_value=get_morning_star_rating(urlfund)
        if return_value==1:
             beating_morning_star_score_list.append(fund_number)
        if (countfunds==10) or (countfunds==25)  or (countfunds==50) or (countfunds==75) or (countfunds==100) or (countfunds==175) or (countfunds==250) or (countfunds==375) or (countfunds==500)  or(countfunds==750) or (countfunds==1000)  or (countfunds==1500) or (countfunds==2000)  or (countfunds==2500):
            print (progress_count,"% done")
    all_funds_readin_master=beating_morning_star_score_list


def print_all():

    global five_year_annualizedlist
    global all_funds_readin_master
    five_year_annualizedlist.sort(reverse=True,key = lambda x: x[1])
    shortned_list=[]
    if len(all_funds_readin_master)==0:
        print ("No funds Found")
    else:
        print ("Here is a full list of funds which hit your parameters")
        #print ("Fund Name           Points above 5 year Annualized return")
        print ()
        print ("Fund Name".ljust(50), end='')
        print ("Points above 5 year Annualized return".ljust(50), end='')
        print ("ISIN".ljust(50), end='')
        print ()
        #pdb.set_trace()
        #hacky but combining results into list (merging 2 lists)
        for i in all_funds_readin_master:
            for j in five_year_annualizedlist:
                if i in j:
                    shortned_list.append(j)
                    #print (j[0],"     ",j[1])
    shortned_list.sort(reverse=True,key = lambda x: x[1])
    #pdb.set_trace()
    #readin in lookup
    with open('fidelity_funds.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    # matching up fund numers with fund names
    for x in shortned_list:
        fundname=""
        for y in data:
            if x[0] == y[1]:
                fundname=y[0]


        #print (fundname,"     ",x[1])
        #print (fundname,"     ",x[1])
        if fundname[-3:] !="Inc":
            print (fundname.ljust(50), end='')
            print (str(x[1]).ljust(50), end='')
            print (str(x[0]).ljust(40), end='')
            print()
    print()
    input("Press any button to continue")



def menu_choice():
    # offer users choice
    os.system('clear')
    print ("Enter your options:")
    print ("1) For current % change in Fidelity Pension")
    print ("2) Overlapping portfolio")
    print ("3) Search for funds (if you want up to date funds run step 9 first)") 
    print ("There are 3 tests:")
    print ("    A) Is the fund beating the 5 year annualized return of the fund ")
    print ("    B) Does the Fund have a 'Above Average' or 'High' 3 and 5 year Morningstar return values" )
    print ("    C) Is it an accumlation fund (i.e not an income fund)" )
    print ("9) Load all funds - (about 3,000)")
    print ("10) Load 2 finds - used in testing")
    print ("11) Load 100 funds - used in testing")
    print ("12) Load 500 funds - used in testing")
    #print ("4) Performance v Index")
    #print ("5) Overall Summary")
    response=input("")
    return (response)
        
while True:
    #os.system('clear')
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
        print()
        input("Press a button to continue")

    elif choice =="2":
        #build database of holdings
        doing_stuff()
        for i in data:
            if i[0][0] is not "#":
                fidelity_api(isin=i[1])
                api_get_fund_holdings(fundname=i[0])
        #sort duplicates and print
        sort_out_duplicates()
        print()
        input("Press a button to continue")

    elif choice =="3":
        # read in funds
        time_events(stop=0,start=1,stage="read in funds")
        read_in_all_fidelity_funds_csv()
        #sleep(60)
        time_events(stop=1,start=0,stage="read in funds")
        status_of_funds(stage="Read In")
        # test 1 beat index 4 out of 5 years
        time_events(stop=0,start=1,stage="beating index")
        beating_index(beat=3,ofyears=5)
        time_events(stop=1,start=0,stage="beating index")
        status_of_funds(stage="Beat Index")
        # test 2 morning star rating 5 star in last 3 and 5 years
        time_events(stop=0,start=1,stage="beating morning star score")
        beating_morning_star_score()
        time_events(stop=1,start=0,stage="beating morning star score")
        time_events(stop=0,start=1,stage="Status of funds")
        status_of_funds(stage="Beat Morning star rating")
        time_events(stop=1,start=0,stage="Status of funds")
        print ()
        print ("Summary")
        print ("======")
        print_all()
        # test 3 portfolio does not contain Tesla
        # print results
        #pdb.set_trace()
        #pass
    elif choice =="4":
        pass
    elif choice =="9":
        get_allfidelityfunds()
        write_fidelty_funds_to_file(filename="fidelity_funds.csv")

    elif choice =="10":
        #get_allfidelityfunds()
        #write_fidelty_funds_to_file(filename="two_funds.csv")
        os.system('cp ./sample_funds/2_funds.csv ./fidelity_funds.csv')
        print ("2 funds read in to fidelity_funds.csv")
        input("Press a button to continue")

    elif choice =="11":
        os.system('cp ./sample_funds/100_funds.csv ./fidelity_funds.csv')
        print ("100 funds read in to fidelity_funds.csv")
        input("Press a button to continue")
    elif choice =="12":
        os.system('cp ./sample_funds/500_funds.csv ./fidelity_funds.csv')
        print ("500 funds read in to fidelity_funds.csv")
        input("Press a button to continue")



    else:
        print ("I am not programmed for this...")


