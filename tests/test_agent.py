from agents.sql_agent import sql_agent
from langchain_community.utilities import SQLDatabase
import os
from dotenv import load_dotenv

load_dotenv()

db_path = "Chinook_Sqlite.sqlite"
db = SQLDatabase.from_uri("sqlite:///{db_path}".format(db_path=db_path))
print(f"--- Database ---")
print(db.dialect)
print(db.get_usable_table_names())
print(db.table_info)

# collect user info
api_key = os.environ.get("GOOGLE_API_KEY")
provider = "google_genai"
model = "gemini-2.0-flash"

question = "How many foods are there?"

# run agent
response = sql_agent(db, question, model, provider, api_key)

print("\n--- Final AI Response ---")
print(response)
