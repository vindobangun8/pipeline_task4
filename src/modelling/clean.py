import pandas as pd
import numpy as np

def cleaning_data (df:pd.DataFrame) -> pd.DataFrame:
    """
    Clean the input DataFrame by .

    Parameters:
    df (pd.DataFrame): The DataFrame to be cleaned.

    Returns:
    pd.DataFrame: The cleaned DataFrame.
    """

    df = df.drop_duplicates()

    # change values in categorical columns
    trans = {
        'Sedan':'sedan',
        '':np.nan,
    }
    df['transmission'] = df['transmission'].replace(trans)

    color = {
        '—':np.nan,
        '':np.nan,
    }
    df['color'] = df['color'].replace(color)

    interior = {
        '—':np.nan,
        '':np.nan,
    }
    df['interior'] = df['interior'].replace(interior)

    # numerical columns - remove negative values
    num_cols = ['year','odometer','condition','mmr','selling_price']
    for col in num_cols:
        df = df[df[col] >=0]


    # remove columns that are not needed
    list_col_drop = ['sales_id','id_sales_nk','brand_car_id','created_at','id_state']
    df = df.drop(columns=list_col_drop)

    return df