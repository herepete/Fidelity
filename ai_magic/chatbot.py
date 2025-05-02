#!/usr/bin/python3.9

import os
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import OpenAI
from langchain_experimental.sql import SQLDatabaseChain

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

DB_HOST = config.DB_HOST
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_NAME = config.DB_NAME


# ✅ Load environment variables
DB_PASSWORD = DB_PASS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not DB_PASSWORD or not OPENAI_API_KEY:
    print("❌ Please set DB_PASSWORD and OPENAI_API_KEY environment variables.")
    exit(1)

# ✅ Database connection string (MariaDB/MySQL)
DB_URI = f"mysql+mysqlconnector://root:{DB_PASSWORD}@localhost/investment_db"

# ✅ Initialize the database connection
db = SQLDatabase.from_uri(DB_URI)

# ✅ Initialize the OpenAI LLM
llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

# ✅ Create the LangChain SQL-to-LLM chain
db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)

# ✅ Interactive CLI loop
def main():
    print("🤖 Chat with your database! Ask about `all_funds_long_list` or type 'exit' to quit.\n")
    while True:
        user_input = input("🧠 Ask a question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        try:
            answer = db_chain.run(user_input)
            print(f"\n💡 Answer:\n{answer}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

if __name__ == "__main__":
    main()

