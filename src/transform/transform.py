import pandas as pd

def transform_data(sales_df:pd.DataFrame,brand_df:pd.DataFrame,state_df:pd.DataFrame) -> pd.DataFrame:

    # Merge data
    sales_brand_df = pd.merge(sales_df,brand_df,left_on='brand_car', right_on='brand_name',how='left')
    merge_df = pd.merge(sales_brand_df,state_df,left_on='state', right_on='code',how='left')

    
    # list of columns to use in warehouse
    list_colums = ['id_sales','year','brand_car_id','transmission','id_state','condition','odometer','color','interior','mmr','sellingprice']
    merge_df = merge_df[list_colums]

    #rename columns 
    columns = {
        'id_sales':'id_sales_nk',
        'sellingprice':'selling_price'
    }
    merge_df = merge_df.rename(columns=columns)

    # fill null values for id columns
    merge_df['brand_car_id'] = merge_df['brand_car_id'].fillna(0)
    merge_df['id_state'] = merge_df['id_state'].fillna(0)

    cols_to_cast = {
        'year':'int',
        'odometer':'float',
        'condition':'float',
        'mmr':'float',
        'selling_price':'float',
        'id_state':'int',
        'brand_car_id':'int'
    }

    merge_df = merge_df.astype(cols_to_cast)
    #set index
    merge_df = merge_df.set_index('id_sales_nk')
    
    return merge_df 