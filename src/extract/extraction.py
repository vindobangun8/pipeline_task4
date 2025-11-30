import requests
import pandas as pd

from src.utils.helper import init_connection,etl_log,init_key_file
from datetime import datetime

def extract_database(table_name:str,engine_name:str) -> pd.DataFrame:
    """
    Extract data from a database table and return it as a pandas DataFrame.

    Parameters:
    table_name (str): The name of the table to extract data from.
    engine_name (str): The name of the database engine to connect to.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted data.
    """
    try:
        # Initialize database connection
        conn = init_connection(engine_name)

        # Query to extract data
        query = f"SELECT * FROM {table_name};"

        # Read data into DataFrame
        df = pd.read_sql(query, conn)

        step = ""
        if engine_name.lower() == 'source':
            step = "staging"
        elif engine_name.lower() == 'staging':
            step = "warehouse" 
        elif engine_name.lower() == 'warehouse':
            step = "modeling"

        log_msg = {
                "step" : step,
                "component":"extraction database",
                "status": "success",
                "table_name": table_name,
                "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
            }

        return df

    except Exception as e:

        step = ""
        if engine_name.lower() == 'source':
            step = "staging"
        elif engine_name.lower() == 'staging':
            step = "warehouse" 
        elif engine_name.lower() == 'warehouse':
            step = "modeling"

        log_msg = {
            "step" : step,
            "component":"extraction database",
            "status": "failed",
            "table_name": table_name,
            "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
            "error_msg": str(e)
        }
    
    finally:
        etl_log(log_msg)

def extract_api(url:str) -> pd.DataFrame: 
    """
    Extract data from an API endpoint and return it as a pandas DataFrame.

    Parameters:
    url (str): The API endpoint URL.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted data.
    """
    try:
        response = requests.get(url)
        data = response.json()

        # Convert to DataFrame
        df = pd.DataFrame(data['regions'])

        log_msg = {
                "step" : "staging",
                "component":"extraction API",
                "status": "success",
                "table_name": "API",
                "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
            }

        return df

    except Exception as e:

        log_msg = {
            "step" : "staging",
            "component":"extraction API",
            "status": "failed",
            "table_name": "API",
            "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
            "error_msg": str(e)
        }
    
    finally:
        etl_log(log_msg)



def extract_sheet( worksheet_name: str) -> pd.DataFrame:
    # init sheet
    sheet_result = init_key_file()
    
    worksheet_result = sheet_result.worksheet(worksheet_name)
    
    df_result = pd.DataFrame(worksheet_result.get_all_values())
    
    # set first rows as columns
    df_result.columns = df_result.iloc[0]
    
    # get all the rest of the values
    df_result = df_result[1:].copy()
    
    return df_result


def extract_spreadsheet(worksheet_name: str):

    try:
        # extract data
        
        df_data = extract_sheet(worksheet_name = worksheet_name)
        
        df_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # success log message
        log_msg = {
                "step" : "staging",
                "component":"extraction spreadsheet",
                "status": "success",
                "table_name": worksheet_name,
                "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
            }
    except Exception as e:
        # fail log message
        log_msg = {
                "step" : "staging",
                "component":"extraction",
                "status": "failed",
                "table_name": worksheet_name,
                "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
                "error_msg": str(e)
            }
        df_data = pd.DataFrame()
    finally:
        # load log to database
        etl_log(log_msg)
        
    return df_data
