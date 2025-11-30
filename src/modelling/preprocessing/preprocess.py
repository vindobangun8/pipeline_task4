from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder


def preprocess_data(num_col:list, cat_col:list) -> ColumnTransformer:
    """
    Create a preprocessing pipeline for numeric and categorical features.

    Parameters:
    num_col (list): List of names of numeric features.
    cat_col (list): List of names of categorical features.

    Returns:
    ColumnTransformer: A column transformer with preprocessing pipelines.
    """
    
    # Numeric pipeline
    numeric_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    # Categorical pipeline
    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
        ('onehot', OneHotEncoder(sparse_output=False, handle_unknown='ignore'))
    ])
    
    # Combine pipelines into a column transformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_pipeline, num_col),
            ('cat', categorical_pipeline, cat_col)
        ]
    )
    
    return preprocessor

