from sqlalchemy import create_engine
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd

from src.utils.config import source, staging, warehouse, log,sheets




def init_connection(engine_name:str):
    try:
        
        if engine_name.lower() == 'source':
            conn = create_engine(f'postgresql+psycopg2://{source["user"]}:{source["password"]}@{source["host"]}:{source["port"]}/{source["db"]}')
        elif engine_name.lower() == 'staging':
            conn = create_engine(f'postgresql+psycopg2://{staging["user"]}:{staging["password"]}@{staging["host"]}:{staging["port"]}/{staging["db"]}')
        elif engine_name.lower() == 'warehouse':
            conn = create_engine(f'postgresql+psycopg2://{warehouse["user"]}:{warehouse["password"]}@{warehouse["host"]}:{warehouse["port"]}/{warehouse["db"]}')
        else:
            raise ValueError("Invalid engine name")
        
        return conn

    except Exception as e:
        raise Exception(e)
    

# Logging 
def etl_log(log_msg: dict):

    try:
        # create connection to database
        conn = create_engine(f"postgresql+psycopg2://{log['user']}:{log['password']}@{log['host']}:{log['port']}/{log['db']}")
        
        # convert dictionary to dataframe
        df_log = pd.DataFrame([log_msg])

        #extract data log
        df_log.to_sql(name = "etl_log",  # Your log table
                        con = conn,
                        if_exists = "append",
                        index = False,
                        )
    except Exception as e:
        print("Can't save your log message. Cause: ", str(e))


def auth_gspread():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    #Define your credentials
    credentials = ServiceAccountCredentials.from_json_keyfile_name(sheets['cred_path'], scope) # Your json file here

    gc = gspread.authorize(credentials)

    return gc

def init_key_file():
    #define credentials to open the file
    gc = auth_gspread()
    
    #open spreadsheet file by key
    sheet_result = gc.open_by_key(sheets["key_spreadsheet"])
    
    return sheet_result



   