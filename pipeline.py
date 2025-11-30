from src.extract.extraction import extract_database,extract_api,extract_spreadsheet
from src.utils.config import api_url
from src.load.load import load_database
from src.transform.transform import transform_data  
from src.extract.extraction import extract_database
from src.modelling.clean import cleaning_data
from src.modelling.preprocessing.splitting_data import split_data
from src.modelling.preprocessing.preprocess import preprocess_data
from src.modelling.xgboost import modelling_process

from dotenv import load_dotenv
import pandas as pd
import numpy as np


load_dotenv()
def pipeline():
    # Extraction
    sales_df = extract_database(table_name='car_sales', engine_name='source')
    state_df = extract_api(url=api_url)
    brand_df = extract_spreadsheet(worksheet_name='brand_car')

    # Load into Staging   
    # Car Sales
    list_sales_columns = ['id_sales','year','brand_car','transmission','state','condition','odometer','color','interior','mmr','sellingprice']
    sales_df = sales_df[list_sales_columns]
    sales_df = sales_df.set_index('id_sales')
    load_database(df=sales_df, table_name='car_sales', engine_name='staging')
    
    # State Data
    state_df = state_df.set_index('id_state')
    load_database(df=state_df, table_name='us_state', engine_name='staging')
    
    # Brand Data
    brand_df = brand_df.set_index('brand_car_id')
    load_database(df=brand_df, table_name='car_brand', engine_name='staging')
    

    # Warehouse
    # Extract from staging
    sales_staging_df = extract_database(table_name='car_sales', engine_name='staging')
    state_staging_df = extract_database(table_name='us_state', engine_name='staging')
    brand_staging_df = extract_database(table_name='car_brand', engine_name='staging')
    
    # Transform
    car_df = transform_data(sales_staging_df,brand_staging_df,state_staging_df)

    # Load into Warehouse
    load_database(df=car_df, table_name='car_sales', engine_name='warehouse')

    #Modelling
    # Extract from warehouse
    car_warehouse_df = extract_database(table_name='car_sales', engine_name='warehouse')
    
    #Cleaning Data
    clean_df = cleaning_data(car_warehouse_df)

    # Split data
    X_train,X_test,y_train,y_test = split_data(clean_df, target='selling_price', test_size=0.2, random_state=42)
    
    # Preprocess data
    num_cols = ['year','odometer','condition','mmr']
    cat_cols = ['transmission','color','interior']
    preprocess = preprocess_data(num_cols,cat_cols)

    X_train_pre = preprocess.fit_transform(X_train)
    X_test_pre = preprocess.transform(X_test)

    modelling_process(X_train_pre, y_train, X_test_pre, y_test)

    print("==== Finish ML Pipeline ====")


if __name__ == "__main__":
    pipeline()
    