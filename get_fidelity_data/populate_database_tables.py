#!/usr/bin/python3.9

import sys
import requests
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import traceback
import json
import bs4
import random
import time
import argparse
import re



import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME


verbose_output=0


def parse_args():
    p = argparse.ArgumentParser(
        description="Populate tables in the DB",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # make the four modes mutually exclusive
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument(
        "-t", "--test", action="store_true",
        help="Test mode: use exactly one dummy fund"
    )
    grp.add_argument(
        "-pm", "--prod-mini", action="store_true",
        help="Production mini run: grab only the first 10 funds"
    )
    grp.add_argument(
        "-pf", "--prod-full", action="store_true",
        help="Production full run: grab all funds"
    )
    grp.add_argument(
        "-prd", "--prod-refresh", action="store_true",
        help="Production refresh: only use funds already in dividends table"
    )
    grp.add_argument(
        "-new", "--new-funds", action="store_true",
        help="Find first 100 funds not already found in friendly_names and with 10 second delay,Really optimized for a cron to have some intellgience and not hammer API"
    )


    return p.parse_args()


def clean_table(table_name,isin):

    conn = mysql.connector.connect(host=DB_HOST,user=DB_USER,password=DB_PASS,database=DB_NAME)
    cursor = conn.cursor()
    if verbose_output==1:
        print(f"Deleting FROM {table_name} WHERE isin = {isin}")
    delete_sql = f"DELETE FROM {table_name} WHERE isin = %s"
    cursor.execute(delete_sql, (isin,))
    conn.commit()


def insert_record(table, columns, values):
    """
    Inserts a record into a MySQL table.

    Parameters:
    - table (str): The table name.
    - columns (list): List of column names.
    - values (tuple): Tuple of values matching the column order.
    - db_config (dict): Dictionary with DB connection keys: host, user, password, database
    """
    if verbose_output==1:
        print(f"Inserting into {table} WHERE isin = {values[0][0]}")
    db_config = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASS,
    "database": DB_NAME}

    placeholders = ', '.join(['%s'] * len(columns))
    columns_str = ', '.join(columns)
    insert_sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(insert_sql, values)
    conn.commit()
    cursor.close()
    conn.close()

def bulk_insert_records(table, columns, rows):
    if verbose_output==1:
        print(f"Inserting into {table} WHERE isin = {rows[0]}")
    db_config = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASS,
    "database": DB_NAME}

    placeholders = ', '.join(['%s'] * len(columns))
    columns_str = ', '.join(columns)
    insert_sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.executemany(insert_sql, rows)
    conn.commit()
    cursor.close()
    conn.close()



def fidelity_api(isin,friendly_name):
    try:
        #read in isin number and format API urls
        fkeystatitics=(f"https://www.fidelity.co.uk/factsheet-data/factsheet/{isin}/key-statistics")#not Json
        fgrowth=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/growthChart") # Json
        finsight=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/filInsight")
        fperformance=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/performance") # Json
        fportfolio=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/portfolio") # Json
        friskandrating=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/riskAndRating") # Json
        fdivdends=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/dividends")#JSON
        fmanagment=(f"https://www.fidelity.co.uk/factsheet-data/api/factsheet/{isin}/fund-management")#JSON
        global portfolio_link
        portfolio_link={}
        portfolio_link.update({'fgrowth':fgrowth,'finsight':finsight,'fperformance':fperformance,'fportfolio':fportfolio,'friskandrating':friskandrating,'fkeystatitics':fkeystatitics,'fdivdends':fdivdends,'fmanagment':fmanagment})

        clean_table(table_name="friendly_names",isin=isin)
        type_of_account=""
        try:
            name = friendly_name.strip()
            type_of_account="NA"
            # 1. Try last three characters
            suffix = name[-3:].upper()
            if suffix in ("ACC", "INC"):
                type_of_account = suffix
                print(f"Suffix found {type_of_account} friednly name ={friendly_name}")
            # 2. Otherwise search the whole string for a standalone ACC or INC
            #    (e.g. matches “ W-Acc-GBP ” or “-INC-”)
            else:
                m = re.search(r'\b(INC|ACC)\b', name, flags=re.IGNORECASE)
                if m:
                    type_of_account= m.group(1).upper()
                    print(f"Suffix not found, type of account determined to be {type_of_account} Fn={friendly_name}")
        except:
            type_of_account="NA"
            print(f"Suffix logic broke, friendley name {friendly_name}")
        insert_record("friendly_names", columns=["isin", "friendly_name","fund_type"], values=(isin, friendly_name,type_of_account))
        
        
        # Non Kson check
        for key, value in portfolio_link.items():
            if verbose_output==1:
                print("#Verbose Working on = ",key,value)
            if key=="fkeystatitics": 
                #non Json search
                if verbose_output==1:
                    print ("#Verbose Non Json logic triggered")
                try:
                    response = requests.get(value)
                except TooManyRedirects:
                    print(f"⚠️ Skipping {key}: too many redirects on {value!r}")
                    continue


                    
                soup = bs4.BeautifulSoup(response.text, 'html.parser')
                #print(soup.prettify()[:2])

            else:
                #Json search
                if verbose_output==1:
                    print ("#Verbose Json logic Trigged")
                response = requests.get(value)
                data = response.json()
                if key =="fgrowth":
                    if verbose_output==1:
                        print ("#Verbose growth logic starting")

                    # delete before add anything new
                    if verbose_output==1:
                        print ("#Verbose Deleting Data before adding anything new")
                    clean_table("growth",isin)
                    if verbose_output==1:
                        print ("#Verbose About to Start Inserting new Data")

                    # Insert New Data
                    #print("Inserting into growth WHERE isin=", isin)

                    rows_to_insert = []
    
                    for period, data_points in data.items():
                        for entry in data_points:
                            end_date = entry.get("endDate")
                            value = entry.get("value")
                            if end_date and value:
                                rows_to_insert.append((isin, period, end_date, float(value)))
                    bulk_insert_records(table="growth",columns=["isin", "period", "endDate", "value"],rows=rows_to_insert)

                elif key =="finsight":

                    # delete before add anything new
                    if verbose_output==1:
                        print ("#Verbose Deleting Data before adding anything new")
                    clean_table("fidelity_insights",isin)
                    # insert data
                    if verbose_output==1:
                        print ("#Verbose About to Start Inserting new Data")
                    insert_record(table="fidelity_insights",columns=["isin", "name", "imgUrl", "designation", "commentary"],values=(isin,data.get("name", ""),data.get("imgUrl", ""),data.get("designation", ""),data.get("commentary", "")))

                elif key =="fportfolio":
                    #for example https://www.fidelity.co.uk/factsheet-data/api/factsheet/GB00BL4SFB26/portfolio
                                        # delete before add anything new
                    if verbose_output==1:
                        print ("#Verbose Deleting Data before adding anything new")
                    clean_table("portfolio_geographical_breakdown",isin)
                    if verbose_output==1:
                        print ("#Verbose About to Start Inserting new Data")
                    rows = []
                    for entry in data["geographicalBreakdown"]:
                        raw = entry.get("Value") or None
                        val = float(raw) if raw is not None else None
                        rows.append((isin, entry["Type"], val))
                    if rows:
                        bulk_insert_records(
                            table="portfolio_geographical_breakdown",
                            columns=["isin","type","value"],
                            rows=rows
                        )
                    else:    
                        print(f"No geographicalBreakdown rows for {isin}, skipping.")

                    if verbose_output==1:
                        print ("#Verbose Deleting Data before adding anything new")
                    clean_table("portfolio_holdings",isin)
                    if verbose_output==1:
                        print ("#Verbose About to Start Inserting new Data")
                    rows = []
                    for entry in data.get("holdings", {}) \
                            .get("portfolioHoldings", []):
                        sec_name = entry.get("securityName", "")
                        country  = entry.get("countryId") or None
                        industry = entry.get("industryId") or None
                        raw      = entry.get("weighting") or None
                        weight   = float(raw) if raw is not None else None
                        rows.append((isin, sec_name, country, industry, weight))

                    if rows:
                
                        bulk_insert_records(
                            table="portfolio_holdings",
                            columns=["isin", "security_name", "country_id", "industry_id", "weighting"],
                            rows=rows
                        )
                    else:
                         #print(f"No Portfolio holdings rows for {isin}, skipping.")
                        pass


                elif key =="friskandrating":
                    #for example https://www.fidelity.co.uk/factsheet-data/api/factsheet/GB00BL4SFB26/riskAndRating
                    #lets grab Morning Star rating
                    if verbose_output==1:
                        print ("#Verbose Deleting Data before adding anything new")
                    clean_table("risk_and_rating_data",isin)

                    if verbose_output==1:
                        print ("#Verbose About to Start Inserting new Data")
                    rows = []
                    for entry in data.get("riskAndRatingData", []):
                    # convert ratingValue to int if present, else None
                        try:
                            rv = int(entry.get("ratingValue")) if entry.get("ratingValue") != "" else None
                        except ValueError:
                            rv = None
                        rows.append((
                            isin,
                            entry.get("timePeriod"),
                            rv,
                            entry.get("riskRatingValue") or None,
                            entry.get("performanceRatingValue") or None
                        ))

                    if rows:
                        bulk_insert_records(
                            table="risk_and_rating_data",
                            columns=[
                                "isin",
                                "time_period",
                                "rating_value",
                                "risk_rating_value",
                                "performance_rating_value"
                            ],
                            rows=rows
                        )
                        if verbose_output==1:                        
                            print(f"✅ Inserted {len(rows)} rows into `risk_and_rating_data` for {isin}.")
                    else:
                        if verbose_output==1:                        
                            print(f"ℹ️  No riskAndRatingData found for {isin}.")

                    
                elif key =="fdivdends":
                    #for example https://www.fidelity.co.uk/factsheet-data/api/factsheet/GB00BL4SFB26/dividends
                    #lets grab all dividend information
                    if verbose_output==1:
                        print ("#Verbose Deleting Data before adding anything new")
                    
                    clean_table("dividends", isin)
                    clean_table("dividend_history", isin)

                    if verbose_output==1:
                        print ("#Verbose About to Start Inserting new Data")
                    rows = []
                    insert_record(
                        table="dividends",
                        columns=[
                            "isin", "is_primary", "distribution_yield",
                            "historic_yield", "underlying_yield",
                            "frequency", "latest_payment_date"
                        ],
                        values=(
                            isin,
                            True if data.get("isPrimary") == "true" else False,
                            float(data.get("distributionYield")) if data.get("distributionYield") else None,
                            float(data.get("historicYield"))   if data.get("historicYield")   else None,
                            float(data.get("underlyingYield")) if data.get("underlyingYield") else None,
                            data.get("frequency"),
                            data.get("latestPaymentDate", "")[:10] or None
                        )
                    )

                    rows = []
                    for entry in data.get("history", []):
                        date_str = entry.get("date", "")
                        rows.append((
                            isin,
                            date_str[:10] or None,
                            float(entry.get("reInvPrice"))     if entry.get("reInvPrice")     else None,
                            float(entry.get("perShareAmount")) if entry.get("perShareAmount") else None
                        ))
                    
                    if rows:
                        bulk_insert_records(
                            table="dividend_history",
                            columns=["isin", "pay_date", "reinvestment_price", "per_share_amount"],
                            rows=rows
                        )
                    else:
                        print(f"No Divident History found for {isin}.")


                elif key =="fmanagment":
                    #for example https://www.fidelity.co.uk/factsheet-data/api/factsheet/GB00BL4SFB26/fund-management
                    #cannot connect so lets not worry
                    #print ("fmanagment- Yet to add code")
                    pass




                elif key =="fperformance":
                    if verbose_output==1:
                        print ("#Verbose Deleting Data from performance tables before adding anything new")
                    clean_table("performance_annual",isin)
                    clean_table("performance_trailing_returns",isin)


                    rows = []

                    try:
                        

                        for entry in data.get("yearlyData", []):
                            rows.append((
                                isin,
                                entry.get("year"),
                                entry.get("startDate"),
                                entry.get("endDate"),
                                entry.get("annualPerformanceValue") or None,
                                entry.get("annualPerformanceBenchmarkValue") or None
                            ))
                    except Exception as ee:
                        print ("Oops something errored 1")
                        print(ee)
                        breakpoint()
                        
                    # Insert
                    if verbose_output==1:
                        print ("#Verbose About to Start Inserting new Data into performance_annual table")
                    bulk_insert_records(table="performance_annual", columns=["isin", "year", "start_date", "end_date", "annualPerformanceValue", "annualPerformanceBenchmarkValue"],rows=rows)

                    #reset rows to be used again
                    rows=[]

                    try:
                        for entry in data.get("timeFrameData", []):
                            rows.append((
                                isin,
                                entry.get("timeframe"),
                                entry.get("trailingReturnsValue")or None,
                                entry.get("trailingReturnsBenchmarkValue")or None
                            ))
                    except Exception as ee:
                        print ("Oops something errored 2")
                        print(ee)
                        breakpoint()

                    # Insert
                    if verbose_output==1:
                        print ("#Verbose About to Start Inserting new Data into performance_annual table")
                    bulk_insert_records(table="performance_trailing_returns", columns=["isin","timeframe","trailingReturnsValue","trailingReturnsBenchmarkValue"],rows=rows)

                    

                else:
                    print("#not coded yet=",key,value)
                    pass

                #print(json.dumps(data, indent=2)[:500])
            if verbose_output==1:
                print("#Verbose Finished on = ",key,value)

        if verbose_output==1:
            print("#Verbose worked reached end of function")    
    except Exception as e:
        breakpoint()
        full_error = traceback.format_exc()
        print("Wow Errors=",full_error)



def get_distinct_dividend_isins():
    DB_NAME = DB_NAME
    """
    Connects to MySQL and returns a list of all distinct ISINs
    from the dividend_history table.
    """
    db_config = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASS,
        "database": DB_NAME
    }

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT isin FROM dividend_history;")
        rows = cursor.fetchall()
        # rows is list of 1-tuples, so extract the first element of each
        list_build=[]
        for i in rows:
            list_build.append({"Name":"","isin":i[0]})
            
        return list_build
    except Error as e:
        print(f"❌ Error fetching distinct ISINs: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def new_funds_check(funds,firstx):
    DB_CONFIG = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASS,      # or os.getenv("DB_PASSWORD")
    "database": DB_NAME,
    }   

    # 1) Fetch existing ISINs
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT isin FROM friendly_names")
    existing_isins = {row[0] for row in cursor.fetchall()}
    cursor.close()
    conn.close()

    # 2) Filter out any fund whose isin is in the DB already
    new_funds = [f for f in funds if f.get("isin") not in existing_isins]
    count_of_total_funds=len(new_funds)
    new_funds = new_funds[:firstx]

    return new_funds,count_of_total_funds




def fetch_fidelity_funds():
    print("Connecting to Morning Star to get fund list")
    # Updated URL with extra fields: Sector, TotalFundSize, and FundType (Inc/Acc)
    url = (
        "https://lt.morningstar.com/api/rest.svc/9vehuxllxs/security/screener?"
        "page=1&pageSize=5000&outputType=json&languageId=en-GB&currencyId=GBP&"
        "universeIds=FOGBR%24%24ALL_3521&securityDataPoints="
        "Name%7Cisin%7COngoingCostEstimated%7CYield_M12%7CCustomCategoryId3Name%7CStarRatingM255%7CQR_GBRReturnM12%7CQR_GBRReturnM36%7CQR_GBRReturnM60%7CSector%7CTotalFundSize%7CFundType"
    )
    res = requests.get(url)
    res.raise_for_status()
    return res.json().get("rows", [])


if __name__ == "__main__":


    #funds_to_check=10
    time_wait_max=3
    args = parse_args()
    if args.test:
        print("#We will only use 1 dummy record")
        print("▶▶ Running in TEST mode")
        funds= [{'Name': 'SVS AllianceBernst Sust US Eq I GBP Acc', 'isin': 'GB00BL4SFB26', 'OngoingCostEstimated': 0.8, 'Yield_M12': 0.23731, 'CustomCategoryId3Name': 'North America', 'StarRatingM255': 2}]
    else:
        print("📥 Fetching funds from Fidelity...")
        funds = fetch_fidelity_funds()
        print(f"✅ Retrieved {len(funds)} funds.\n")

        if args.prod_mini:
            print(f"▶▶ PROD-MINI: processing first 10 funds")
            funds = funds[:10]

        elif args.prod_full:
            print(f"▶▶ PROD-FULL: processing all {len(all_funds)} funds")
        
        elif args.prod_refresh:
            print("▶▶ PROD-REFRESH: processing only funds already in dividends table")
            # you'll need to implement `filter_new_or_updated()` yourself,
            # e.g. compare against database timestamps
            funds=get_distinct_dividend_isins()
        elif args.new_funds:
            lets_check=100
            print("▶▶ NEW Funds: just search for funds not already seen in friendly_names, with 10 Second Delay")
            funds,len_of_funds=new_funds_check(funds,firstx=lets_check)
            #breakpoint()
            print(f"After removing funds already in the DB I have Found {len_of_funds} to process i will take the first {lets_check}")
            time_wait_max=10
            if len(funds)==0:
                print("▶▶ No Funds Found exiting...")
                exit()
                
        
    count=0
    length_funds=len(funds)
    for i in funds:
        count+=1
        isin = i["isin"]
        friendly_name=i["Name"]
        print (f"Starting Record {count} of {length_funds} isin={isin}")
        delay = random.uniform(0,time_wait_max )
        print(f"Sleeping for {delay:.2f}s…")
        time.sleep(delay)
        fidelity_api(isin,friendly_name)
        print ("")


