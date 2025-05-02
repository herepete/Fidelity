#!/usr/bin/env python3
import os
import mysql.connector
import openai

# ─── CONFIG ────────────────────────────────────────────────────────────────────
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable")

# ─── TOOL: RUN SQL ─────────────────────────────────────────────────────────────
def run_sql(query: str):
    conn = mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
    )
    cur = conn.cursor()
    cur.execute(query)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return cols, rows

# ─── AGENT: ASK A QUESTION ─────────────────────────────────────────────────────
def ask_question(question: str):
    system_prompt = """
You are an AI assistant that ONLY ever emits a single MySQL SELECT statement (no semicolon) against this schema:

Note for all table fields:
-id is an incremental number on each table
-isin is related to the fund name and mapped in the friendly_names table. 
-fetched_on is the date we import the data into the database

Other notes:
-If there is a question about Yield check the dividends table
-The Frequency of a yield means how often the yields are given out expected values are Annually,Semi-Annually,Quarterly or Monthly although it can be None or Null
-fidelity_insights has data in the commentary field has a write up from Fidelity they only do this for some funds not all on most recent checks it was 60 out of 2500 have commentary
-friendly_names helps convert isin to a more friendly fund name, fund_type is typically ACC or INC so if you get a query to search for Income funds use fund_type=="INC"
- in the growth table period could be M for Month, D for Day or Y for Year  so M6 would be 6 months, or D5 would be 5 days, Y1 would be One Year.
- in the performance_trailing_returns table timeframe could be M for Month, D for Day or Y for Year or W for Week, so M6 would be 6 months, or D5 would be 5 days, Y1 would be One Year ,W1 would be Week 1.
- in portfolio_geographical_breakdown type could be country for example Japan and then the value is a % for example 18.52334. That would mean the portfolio has 18.5% percent of the portfolio is based in Japan. Some funds don't provide this information so it might be blank or missing.
- in portfolio_holdings this list the top 10 holding in the funds , the security_name is the name of the company for example Microsoft , country_id is where that company is based for example USA, the weighting is how much of the portfolio is in that company so 3.53115 would mean 3.5% percent of Microsoft which is a USA based company is in this portfolio. Some funds don't publish data so there might be some missing data
- risk_and_rating_data is largely morning star ratings time period could be M for Month, D for Day or Y for Year or W for Week, so M6 would be 6 months, or D5 would be 5 days, Y1 would be One Year ,W1 would be Week 1. Rating values are out of 5 and risk_rating gives a score it might be Average,Above Average,Below Average,High,Low



Here are the table and the values

- dividend_history (id,isin ,pay_date ,reinvestment_price ,per_share_amount,fetched_on)
- dividends (id,isin,is_primary  ,distribution_yield  ,historic_yield   ,underlying_yield ,frequency  ,latest_payment_date ,fetched_on)
- fidelity_insights (isin ,name ,imgUrl, designation ,commentary ,fetched_on )
- friendly_names (id ,isin ,fund_type ,friendly_name,fetch_date )
-  growth(id ,isin , period ,endDate ,value ,fetched_on )
- performance_annual (id ,isin ,year ,start_date ,end_date,annualPerformanceValue ,annualPerformanceBenchmarkValue , fetched_on )
- performance_trailing_returns (id ,isin , timeframe ,trailingReturnsValue ,trailingReturnsBenchmarkValue ,fetched_on )
-  portfolio_geographical_breakdown(id,isin,type,value,fetched_on )
- portfolio_holdings (id ,isin,security_name,country_id,industry_id,weighting,fetched_on)
- risk_and_rating_data  (id,isin ,time_period,rating_value,risk_rating_value,performance_rating_value,fetched_on ) 

Use only those exact table- and column-names. If the user asks about columns or tables that don't exist here, respond with a brief “That field/table doesn’t exist in my schema.” and do not emit SQL.
If i say show me income funds check the friendly_names table where fund_type = "INC"
If i say show me Morning Star Rating check the risk_and_rating_data risk_rating_value
"""
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": question.strip()},
        ],
    )

    sql = resp.choices[0].message.content.strip()
    print(f"\n🔍 Generated SQL:\n{sql}\n")

    try:
        return run_sql(sql)
    except mysql.connector.Error as e:
        # bubble up a nice error
        raise RuntimeError(f"MySQL Error {e.errno}: {e.msg}")

# ─── MAIN LOOP ────────────────────────────────────────────────────────────────
def main():
    print("🤖 AI Fund Agent — ask me about your funds database!")
    print("Type 'exit' or 'quit' to leave.")
    while True:
        q = input("\n> ").strip()
        if q.lower() in ("exit", "quit"):
            break
        if not q:
            continue

        try:
            cols, rows = ask_question(q)
        except RuntimeError as err:
            print(f"❌ {err}")
            continue

        # pretty-print a simple table
        print("│ " + " │ ".join(cols) + " │")
        print("├" + "─" * (len(cols) * 15) + "┤")
        for r in rows:
            print("│ " + " │ ".join(str(x) for x in r) + " │")

if __name__ == "__main__":
    main()

