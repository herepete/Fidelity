#!/usr/bin/python3.9
import bs4
import requests
import csv
import os
import json
import time
import random
import pandas as pd
import config # config file for setting variables in the script
from datetime import datetime
from collections import deque
recent_inputs = deque(maxlen=10)
import openai
import insert_into_mariadb
import subprocess
import socket
import test_openai




# Get the current date
current_date = datetime.now()

# Format the date as ddmmyy
formatted_date = current_date.strftime("%d%m%y")


# Assign it to a variable
ddmmyy_variable = formatted_date
today_date = datetime.now().date()


#Global variables
duplicate_holdings=[]
portfolio_link=[]
time_delay=0
large_fund_builder=[]

#data = data from lookup
data=[]
data_sw=[]
portfolio_link=[]



def get_allfidelityfunds():
    api_test="https://lt.morningstar.com/api/rest.svc/9vehuxllxs/security/screener?page=1&pageSize=5000&sortOrder=LegalName%20asc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=FOGBR%24%24ALL_3521&securityDataPoints=SecId%7CName%7CTenforeId%7CholdingTypeId%7Cisin%7Csedol%7CCustomAttributes1%7CCustomAttributes2%7CCustomExternalURL1%7CCustomExternalURL2%7CCustomExternalURL3%7CCustomIsClosed%7CCustomIsFavourite%7CCustomIsRecommended%7CCustomMarketCommentary%7CQR_MonthDate%7CExchangeId%7CExchangeCode%7CCurrency%7CLegalName%7CCustomBuyFee%7CYield_M12%7COngoingCostEstimated%7CCustomCategoryId3Name%7CStarRatingM255%7CQR_GBRReturnM12_5%7CQR_GBRReturnM12_4%7CQR_GBRReturnM12_3%7CQR_GBRReturnM12_2%7CQR_GBRReturnM12_1%7CCustomMinimumPurchaseAmount%7CCustomAdditionalBuyFee%7CCustomSellFee%7CTransactionFeeEstimated%7CPerformanceFee%7CGBRReturnM0%7CGBRReturnM12%7CGBRReturnM36%7CGBRReturnM60%7CGBRReturnM120%7CTrackRecordExtension&filters=&term=&subUniverseId=MFEI"
    #res=requests.get("https://www.fidelity.co.uk/planning-guidance/investment-finder/#?investmentType=funds&universeId=FOGBR$$ALL_3521&filtersSelectedValue=%7B%7D&page=1&perPage=10&sortField=legalName&sortOrder=asc&subUniverseId=MFEI")
    res=requests.get(api_test)
    res.raise_for_status()
    soup =bs4.BeautifulSoup(res.text,'html.parser')
    #understand_api_data(soupin=soup)
    links_with_text = []
    string_soup=str(soup)
    json_soup=json.loads(string_soup)
    just_rows=json_soup['rows']
    for funds in just_rows:
        fundname=funds['Name']
        isin_number=funds['isin']
        templist=[fundname,isin_number]
        large_fund_builder.append(templist)


def fidelity_api(isin):
    #read in isin number and format API urls
    #isin=123456789
    #not sure if this is the best approach espically for large inputs
    fkeystatitics=(f"https://www.fidelity.co.uk/factsheet-data/factsheet/{isin}/key-statistics")
    fgrowth=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/growthChart")
    finsight=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/filInsight")
    fperformance=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/performance")
    fportfolio=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/portfolio")
    friskandrating=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/riskAndRating")
    global portfolio_link
    portfolio_link={}
    portfolio_link.update({'fgrowth':fgrowth,'finsight':finsight,'fperformance':fperformance,'fportfolio':fportfolio,'friskandrating':friskandrating,'fkeystatitics':fkeystatitics})
    out_file = open("apitotest", 'w+', newline ='')
    write = csv.writer(out_file)
    write.writerows(fperformance)


def write_fidelty_funds_to_file(filename):

    import csv
    out_file = open(filename, 'w+', newline ='') 
    with out_file:
        write = csv.writer(out_file) 
        write.writerows(large_fund_builder) 
    len_list=len(large_fund_builder)
    print ("All done I have written out %s records to fidelity_funds.csv" % len_list)
    input("press a button to continue")

def read_in_all_fidelity_funds_csv():

    import csv
    global all_funds_readin_master
    with open('fidelity_funds.csv', newline='') as f:
        reader = csv.reader(f)
        all_funds_readin_master = list(reader)

def write_out_failures(fund,reason):

# String to write to the file
    fundname=fund[0]
    isin=fund[1]
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    lines=[fundname,",",isin,",",reason," ",ddmmyy_variable,"\n"]
    insert_into_mariadb.insert_fund_record(date=today_date, time=current_time, fund=fundname, isin=isin, log=reason)

    # Open a file in write mode ('w') and write the string to it
    with open('failer_test_fund.txt', 'a') as file:
        file.writelines(lines)

def read_in_failures():

    import csv
    global failure_funds
    try:
        with open('failer_test_fund.txt', newline='') as f:
            reader = csv.reader(f)
            failure_funds = list(reader)
        count_failure_funds=len(failure_funds)
        #print(f"i have recently rejected  = {count_failure_funds} funds")
    except:
        failure_funds=["hi"]
        count_failure_funds=0

def menu_header(Income_Stocks_Found, Previously_checked , This_round_checking , This_Round_Rejected , This_Round_Suitable_Funds_found,verbose_message):

    os.system('clear')
    header = "Income Stocks Found , Previously checked , This round Checking , This Round Rejected , This Round Suitable Funds found"
    data = f"{Income_Stocks_Found}, {Previously_checked} , {This_round_checking} , {This_Round_Rejected} , {This_Round_Suitable_Funds_found}"
    # Define the width for each field
    column_width = 30

    # Split the header and data into lists
    header_list = header.split(',')
    data_list = data.split(',')

    # Print the formatted header
    formatted_header = ''.join(f"{item.strip():<{column_width}}" for item in header_list)
    print(formatted_header)

    # Print the formatted data
    formatted_data = ''.join(f"{item.strip():<{column_width}}" for item in data_list)
    print()
    print(formatted_data)

    recent_inputs.append(verbose_message)


    print("")
    print("Verbose Stuff...")
    for i in recent_inputs:
        print(i)





def extra_checks(funds_to_check_more):
    last_years_yield=1
    manager_tenure=2
    morning_star_rating=3
    for fund in funds_to_check_more:
        portfolio_link={}
        fund_name=fund[0]
        isin=fund[1]
        #print(f"total funds={number_of_funds_total} Funds Checked={funds_checked} Funds to consider={funds_to_consider} fund={isin}  {fund_name}")
        """Build Api """
        fkeystatitics=(f"https://www.fidelity.co.uk/factsheet-data/factsheet/{isin}/key-statistics")#not Json
        fgrowth=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/growthChart") # Json
        finsight=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/filInsight")
        fperformance=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/performance")#Json
        fportfolio=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/portfolio")#JSON
        friskandrating=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/riskAndRating")#JSON
        fdivdends=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/dividends")#JSON
        fmanagment=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/fund-management")#JSON
        portfolio_link.update({'fgrowth':fgrowth,'finsight':finsight,'fperformance':fperformance,'fportfolio':fportfolio,'friskandrating':friskandrating,'fkeystatitics':fkeystatitics,'fdivdends':fdivdends,'fmanagment':fmanagment})


        #last_years_yield = calculate_last_years_yield(fund)
        #last_years_yield = 1
        """Check last Years Dividends """
        url_to_check=portfolio_link['fdivdends']
        response = requests.get(url_to_check)
        data = response.json()
        # Extract the history of payments
        history = data["history"]

        # Get the current year
        current_year = datetime.now().year

        # Set variables to calculate previous year's yield
        previous_year = current_year - 1
        previous_year_total = 0.0

        # Extract all payments from the previous year
        for entry in history:
            payment_date = datetime.fromisoformat(entry["date"])
            if payment_date.year == previous_year:
                previous_year_total += float(entry["perShareAmount"])

        # Calculate the yield based on the last reinvestment price in the previous year
        # Assuming we use the reinvestment price from the latest date in the previous year
        previous_year_price = None
        for entry in history:
            payment_date = datetime.fromisoformat(entry["date"])
            if payment_date.year == previous_year:
                previous_year_price = float(entry["reInvPrice"])
                break

        # Calculate the yield if we have the price
        if previous_year_price:
            previous_year_yield = (previous_year_total / previous_year_price) * 100
            previous_year_yield = round(previous_year_yield, 2)
            #print(f"Previous Year's Yield: {previous_year_yield:.2f}%")
            #breakpoint()
        else:
            #print("No reinvestment price found for the previous year.")
            previous_year_yield = "Not Sure"

        
        last_years_yield = previous_year_yield
        #manager_tenure = determine_manager_tenure(fund)
        manager_tenure = 2

        #morning_star_rating = assign_morning_star_rating(fund)

        """ Morning Star Overall Rating"""
        url_to_check=portfolio_link['friskandrating']
        response = requests.get(url_to_check)
        data = response.json()
        
        if not data["riskAndRatingData"]:
            m255_rating_value = "No Data"
        else:
            m255_rating_value = next((item["ratingValue"] for item in data["riskAndRatingData"] if item["timePeriod"] == "M255"), None)

        morning_star_rating =  m255_rating_value



        fund.append(last_years_yield)
        #fund.append(manager_tenure)
        fund.append(morning_star_rating)
    return (funds_to_check_more)

def project_status():


    try:
        if  config.testing ==1:
            mode="Testing"
        elif config.testing ==0:
            mode="Live"
        else:
            mode="Unsure"
    except:
        mode="Unsure -Something Went Wrong"

    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            ip_data = response.json()
            web_address = "http://" + ip_data['ip']
        else:
            web_address = "Could not get Ip Address"
    except Exception as e:
            web_address = "Could not get Ip Address"

    try:
        # Check the status of the MariaDB service
        result = subprocess.run(
            ["systemctl", "is-active", "--quiet", "mariadb"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # If the command exits with code 0, MariaDB is running
        maria_running="Yes"
    except Exception as e:
        maria_running="No"

    flask_running = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(("127.0.0.1", 5000))
            flask_running = "Yes"
        except OSError:
            flask_running = "No"


    apache_running = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(("127.0.0.1", 80))
            apache_running = "Yes"
        except OSError:
            apache_running = "No"
    try:
        rv=test_openai.return_test_query()
        if rv == 1:
            openai_running="Running"
        else:
            openai_running="Not Running"
    except:
            openai_running="Not Running-Something Errored"
    try:
        db_password = os.getenv("DB_PASSWORD")
        if db_password:
            db_password_set="Yes"
        else:
            db_password_set="No"
    except:
            db_password_set="No-Something Errored"

    try:
        db_password = os.getenv("OPENAI_API_KEY")
        if db_password:
            openai_key_set="Yes"
        else:
            openai_key_set="No"
    except:
            openai_key_set="No-Something Errored"



    #mode="live_mo_hc"
    #maria_running="yes_m"
    #flask_running="yes_f"
    #appache_running="yes_a_hc"
    #openai_running="yes_ai_hc"
    #web_address="http://35.178.187.229/"


    print ("====Status===")
    print (f"Mode={mode}")
    print (f"MariaDB Running={maria_running}")
    print (f"Flask Running={flask_running}")
    print (f"Apache Running={apache_running}")
    print (f"OpenAI Connection working={openai_running}")
    print (f"Env Variables - DB password set={db_password_set}")
    print (f"Env Variables- Open AI Key found={openai_key_set}")
    print ("====")
    print (f"Web Address={web_address}")
    print ("====")


def ai_feedback(df):

    try:
        """
        to chatgbt say - I want your analysis on these funds, pros and cons of each based on the information provided and any other research you can do. I want those results in 1 table, & then paste in the input of df
        output will be a table.
        can i just do a raw print out of the output?
        """
        # Convert the dataframe to a string to send in the prompt
        openai.api_key =  os.getenv('OPENAI_API_KEY')

        df_string = df.to_string(index=False)

        # Define the prompt with the DataFrame included
        messages = [
            {"role": "system", "content": "I want your analysis on these funds, pros and cons of each based on the information provided and any other research you can do. I want those results in 1 table."},
            {"role": "user", "content": f"Here is the data of income funds:\n\n{df_string}"}
        ]

        # Use OpenAI's GPT-4 model to send the prompt and get a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-4 or another available model
            messages=messages,
            max_tokens=4095  # Set the maximum number of tokens in the response
        )

        # Print the AI's response
        print ("Here are the raw results and the AI feedback on those funds...")
        print(response['choices'][0]['message']['content'])
        print("AI Analysis completed ")
        ai_date = datetime.now().date()
        ai_time = datetime.now().time()
        insert_into_mariadb.insert_into_automation(ai_date,ai_time,Feedback=response['choices'][0]['message']['content'])

    except Exception as e:
        print("AI failed somewhere error=",e)



def income_funds():
    from pprint import pprint
    #menu_header(Income_Stocks_Found=1500, Previously_checked=1000 , This_round_checking=45 , This_Round_Rejected=5 , This_Round_Suitable_Funds_found=15)
    testing=int(config.testing)
    """steps
    1) read in funds
    2) strip out "acc" or strip in inc
    3) is yield above 4%
    4) is performance of fund 5% per year over last 5 years
    5
    """
    print("Ok so for income funds we have 4 Steps")
    print ("1) Read in Funds # Starting")
    print ("### Read in Funds from fidelity_funds.csv, if you haven't updated these in a while you might want to, there are about 3,000 funds in total.")
    read_in_all_fidelity_funds_csv()
    global all_funds_readin_master
    """
    at this point we have a global variable of all_funds_readin_master which has been read in from our csv (which can be created from other chosen items in menu)
    """
    list_of_income_funds=[]
    total_funds=0
    total_income_funds=0
    print ("1) Read in Funds # Done") 
    print ("2) Show just Income Funds #Starting")

    for i in all_funds_readin_master:
        total_funds+=1

        if "Inc" in i[0] and "Acc" not in i[0]:
            list_of_income_funds.append(i)
            total_income_funds+=1
    menu_header(Income_Stocks_Found=total_income_funds, Previously_checked="-" , This_round_checking="-" , This_Round_Rejected="-" , This_Round_Suitable_Funds_found="-",verbose_message="I have Stripped out Acc funds")
    time.sleep(1)
    print(f"in total i found {total_funds} of which {total_income_funds} are income funds")

    #strip our previousley rejected funds
    new_list_of_income_funds=[]
    read_in_failures()
    match_found=0
    striped_out=0
    for i in list_of_income_funds:
        match_found=0
        for j in failure_funds:
            if j[1] == i[1]:
                match_found=1
                striped_out+=1
                break
        if match_found==0:
            new_list_of_income_funds.append(i)
            continue

    menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking="-" , This_Round_Rejected="-" , This_Round_Suitable_Funds_found="-",verbose_message="I have Stripped out previousley rejected funds")
    time.sleep(2)
    #print(f"in total i Stripped out {striped_out} because they have been flagged as already recentley checked")
    list_of_income_funds= new_list_of_income_funds
    if len(list_of_income_funds)==0:
            write_out_failures(fund="abcdef-dummy data",reason="No funds left to check - most likely all funds have been checked recentley")
            breakpoint()

    
    if testing==1:
        check_funds=config.funds_to_check
        #print(f"###Testing so stripping down income list to {check_funds}")
        list_of_income_funds = list_of_income_funds[-check_funds:]
    menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds) , This_Round_Rejected="-" , This_Round_Suitable_Funds_found="-",verbose_message="Updated income funds based on testing parameters")
    time.sleep(2)

    results=[]
    funds_to_consider=0
    funds_checked=0
    number_of_funds_total=len(list_of_income_funds)
    rejected_funds_this_round=0

    for inc_funds in  list_of_income_funds:

        funds_checked+=1
        portfolio_link={}
        fund_name=inc_funds[0]
        isin=inc_funds[1]
        #print(f"total funds={number_of_funds_total} Funds Checked={funds_checked} Funds to consider={funds_to_consider} fund={isin}  {fund_name}")
        """Build Api """
        fkeystatitics=(f"https://www.fidelity.co.uk/factsheet-data/factsheet/{isin}/key-statistics")#not Json
        fgrowth=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/growthChart") # Json
        finsight=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/filInsight") 
        fperformance=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/performance")#Json
        fportfolio=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/portfolio")#JSON
        friskandrating=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/riskAndRating")#JSON
        fdivdends=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/dividends")#JSON
        fmanagment=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/fund-management")#JSON
        portfolio_link.update({'fgrowth':fgrowth,'finsight':finsight,'fperformance':fperformance,'fportfolio':fportfolio,'friskandrating':friskandrating,'fkeystatitics':fkeystatitics,'fdivdends':fdivdends,'fmanagment':fmanagment})
        
        """Get ongoing Cost"""
        url_to_check=portfolio_link['fkeystatitics']
        res=requests.get(url_to_check)
        soup =bs4.BeautifulSoup(res.text,'html.parser')
        string_soup=str(soup)
        ongoing_charge_row = soup.find('td', string="Ongoing charge (%)")
        verbose_message_checking=f"Starting work on - {fund_name}"
        menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message=verbose_message_checking)

        if ongoing_charge_row:
            try:
                ongoing_charge_value = float(ongoing_charge_row.find_next('td').text.strip())
            except:
                write_out_failures(fund=inc_funds,reason="Failed to convert ongoing fee to float correctly")
                menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message="Failed to convert ongoing fee to float correctly")
                continue
        else:
            ongoing_charge_value = 0
        if ongoing_charge_value > config.max_ongoing_charge:
            write_out_failures(fund=inc_funds,reason=f"cost to high at {ongoing_charge_value}")
            menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message="Cost to high")
            rejected_funds_this_round+=1
            continue


        """Get Yield using JSON """
        # Parse the response JSON
        try:
            url_to_check=portfolio_link['fdivdends']
            response = requests.get(url_to_check)
            data = response.json()

            # Extract the yield values
            distribution_yield = data.get("distributionYield")
            historic_yield = data.get("historicYield")
            underlying_yield = data.get("underlyingYield")
            distrubtution_frequency =data.get("frequency")

        except Exception as ey:
            write_out_failures(fund=inc_funds,reason="yield and freqeuncey check fail")
            menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message="Yield and Frequency check fail")
            rejected_funds_this_round+=1
            continue
        try:
            if float(distribution_yield) < config.min_yield:
                write_out_failures(fund=inc_funds,reason=f"Yield to Low rate={distribution_yield}")
                rejected_funds_this_round+=1
                menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message="Yield to Low")
                continue
        except Exception as ycf :
            if distribution_yield=="":
                write_out_failures(fund=inc_funds,reason=f"Yield Check failure - no Yield Found")
            else:
                write_out_failures(fund=inc_funds,reason=f"Yield Check failure DY Found={distribution_yield} , error={ycf}")
                rejected_funds_this_round+=1
                menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message="Yield check failure")
            continue
        try:
        
            """Get Performance using Json """
            url_to_check=portfolio_link['fperformance']
            perf_response = requests.get(url_to_check)
            perf_data=perf_response.json()
            year1=0
            years_annualised_3 = 0
            years_annualised_5 = 0
            for entry in perf_data.get('timeFrameData', []):
                timeframe = entry.get('timeframe')
                if timeframe == 'M12':
                    year1 = int(float(entry.get('trailingReturnsValue')))
                elif timeframe == 'M36':
                    years_annualised_3 = int(float(entry.get('trailingReturnsValue')))
                elif timeframe == 'M60':
                    years_annualised_5 = int(float(entry.get('trailingReturnsValue')))
            annualized_return_value_check=config.annualized_return_value_check
            try:
                if (float(year1) < annualized_return_value_check) or (float(years_annualised_3) < annualized_return_value_check) or (float( years_annualised_5) < annualized_return_value_check):
                    write_out_failures(fund=inc_funds,reason=f"1,3,or 5 year check failed 1y={year1} 3y={years_annualised_3} 5y={years_annualised_5} ")
                    menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message="1,3 or 5 year return not good enough")
                    rejected_funds_this_round+=1
                    continue
            except:
                write_out_failures(fund=inc_funds,reason=f"1,3,or 5 year check failed 1y={year1} 3y={years_annualised_3} 5y={years_annualised_5} ")
                rejected_funds_this_round+=1
                menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message="1,3 or 5 year check failed")
                continue


        except Exception as e:
            #breakpoint()
            write_out_failures(fund=inc_funds,reason="Larger Catchall for other errors")
            rejected_funds_this_round+=1
            menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message="Larger Catchall for other errors")
            continue

        results.append([fund_name,isin, ongoing_charge_value,distribution_yield ,distrubtution_frequency,year1, years_annualised_3, years_annualised_5])
        verbose_message_checking=f"Suitable Fund Found={fund_name}"
        menu_header(Income_Stocks_Found=total_income_funds, Previously_checked=striped_out , This_round_checking=len(list_of_income_funds)  , This_Round_Rejected=rejected_funds_this_round , This_Round_Suitable_Funds_found=len(results),verbose_message=verbose_message_checking)
        funds_to_consider+=1
    if funds_to_consider==0:
        print("No suitable funds found sorry")
    else:
        #sneding for extra checks 
        results=extra_checks(funds_to_check_more=results)
        if config.write_out_db==1:
            date_s = datetime.now().date()
            time_s = datetime.now().time()
            for i in results:
                # ['abrdn High Yield Bond I Inc', 'GB0000939818', 0.69, '5.53', 'Quarterly', 12, 3, 3, 5.35, '4']
                insert_into_mariadb.insert_fund_record_sucess(date=date_s, time=time_s, fund_name=i[0], isin=i[1], fee=i[2], yield_percentage=i[3], frequency=i[4], y1_annualized=i[5], y3_annualized=i[6], y5_annualized=i[7], last_years_yield=i[8], morning_star_rating=i[9])

        print()
        #print("This is what has been found based on Criteria Given")
        columns = ['Fund Name','ISIN', 'Fee (%)', 'Yield (%)',  'Frequency', 'Y1_Annualized', 'Y3_Annualized', 'Y5_Annualized','Last Years Yield','Morning Star Rating']
        df = pd.DataFrame(results, columns=columns)
        #sorted_df=df.sort_values(by='Frequency')
        #print(sorted_df.to_string(index=False))
        #print("123")
        ai_feedback(df)
        exit()
            

def menu_choice():
    # offer users choiceo
    project_status()
    print ("Enter your option:")
    print ("1) Reload all funds - (about 3,000) - Rarely needs to be run")
    print ("2) Find Income Funds matching criteria -note Anything already which has failed the checks will not be rechecked")
    #print ("3) Run a basic openai query ")
    print ("4) Empty DB and log file locally ")
    print ("5) Check contents of DB")
    #print ("6))Safety checks, db installed, appache running, flask installed,merge with point 3")
    print ("7) Start Flask")
    print ("8) Stop Flask")
    response=input("")
    return (response)
        
while True:
    choice=menu_choice()

    if choice =="1":
        get_allfidelityfunds()
        write_fidelty_funds_to_file(filename="fidelity_funds.csv")

    elif choice =="2":
        income_funds()
        import config
        #if config.write_out_html==1:
        #    write_out_to_html(information="hi 123")

    elif choice =="3":
        import test_openai
    elif choice =="4":
        #empty log file
        with open("failer_test_fund.txt", "w") as file:
            file.write("")  # Write an empty string to the file
        insert_into_mariadb.empty_db()
    elif choice =="5":
        insert_into_mariadb.show_all_records(vlimit=10)
        insert_into_mariadb.show_all_sucess(vlimit=10)
        insert_into_mariadb.show_automation()
    elif choice =="7":
        os.system('sudo systemctl start flaskapp.service')
    elif choice =="8":
        os.system('sudo systemctl stop flaskapp.service')

    else:
        print ("I am not programmed for this...")


