from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from src.utils.helper import etl_log
from datetime import datetime

from src.modelling.save_model import save_model

def modelling_process(X_train: pd.DataFrame, y_train: pd.Series, 
                     X_test: pd.DataFrame, y_test: pd.Series):
    try:
        model = XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
        )
        # train the model    
        model.fit(X_train, y_train)
        
        # make predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        #evaluate the model
        mse_train = mean_squared_error(y_train, y_pred_train)
        rmse_train = round(np.sqrt(mse_train), 2)
        mape_train = round(np.mean(np.abs((y_train - y_pred_train) / y_train)) * 100, 2)
        print(f"Train RMSE: {rmse_train}")
        print(f"Train MAPE: {mape_train}")

        mse_test = mean_squared_error(y_test, y_pred_test)
        rmse_test = round(np.sqrt(mse_test), 2)
        mape_test = round(np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100, 2)
        print(f"Test RMSE: {rmse_test}")
        print(f"Test MAPE: {mape_test}")

        save_model(model, bucket_name='models')

        log_msg = {
            "step" : "Modelling",
            "component":"Modelling XGBoost",
            "status": "Success",
            "table_name": f"Train RMSE: {rmse_train}, Test RMSE: {rmse_test}",
            "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        log_msg = {
            "step" : "Modelling",
            "component":"Modelling XGBoost",
            "status": "failed",
            "table_name": "",
            "etl_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Current timestamp
            "error_msg": str(e)
        }
        
    finally:
        etl_log(log_msg)