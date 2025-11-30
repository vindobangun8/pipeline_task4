
from datetime import datetime
from sqlalchemy import create_engine,inspect
from pangres import upsert
import pandas as pd

from src.utils.helper import init_connection,etl_log,init_key_file
from src.utils.config import staging



def load_database(df:pd.DataFrame,table_name:str,engine_name:str):
    """
    Load data from a pandas DataFrame into a database table.

    Parameters:
    df (pd.DataFrame): The DataFrame containing data to load.
    table_name (str): The name of the table to load data into.
    engine_name (str): The name of the database engine to connect to.

    Returns:
    None
    """
    try:
        # Initialize database connection
        conn = init_connection(engine_name)

        # Use pangres upsert to load data into the table
        upsert(
            df = df,
            con = conn,
            table_name =table_name,
            if_row_exists="update"
        )


        log_msg = {
                "step" : engine_name.lower(),
                "component":"load database",
                "status": "success",
                "table_name": table_name,
                "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
            }

    except Exception as e:
        log_msg = {
            "step" : engine_name.lower(),
            "component":"load database",
            "status": "failed",
            "table_name": table_name,
            "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
            "error_msg": str(e)
        }

    finally:
        etl_log(log_msg)    