import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import duckdb

def get_token_from_user_file(user_file_path):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    credentials = service_account.Credentials.from_service_account_file(
        user_file_path,
        scopes=SCOPES
        )

    request = Request()
    credentials.refresh(request)
    return credentials.token

key_file_path = "credentials.json"
token = get_token_from_user_file(key_file_path)

env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
    # Set the token as an env var for some tests
    myfile.write(f"TOKEN={token}\n")
    # Set the key_file filepath as an env var for other tests
    myfile.write(f"KEY_FILE_PATH={key_file_path}")

duckdb_con = duckdb.connect(':memory:')
duckdb_con.sql("install gsheets from community")
duckdb_con.sql("load gsheets")

duckdb_con.sql(f"create or replace secret gsheet_secret (TYPE gsheet, provider access_token, token '{token}')")

print(duckdb_con.sql("select * from read_gsheet('https://docs.google.com/spreadsheets/d/11QdEasMWbETbFVxry-SsD8jVcdYIT1zBQszcF84MdE8/edit?gid=644613997#gid=644613997');"))

print('It seems to have worked!')
