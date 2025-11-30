from minio import Minio
from io import BytesIO
import pickle

from src.utils.config import minio 
from datetime import datetime

def save_model(model, bucket_name:str):

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Initialize MinIO client
    client = Minio('localhost:9001',
                access_key=minio['access_key'],
                secret_key=minio['secret_key'],
                secure=False)

    # Make a bucket if it doesn't exist
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

    # Convert DataFrame to CSV and then to bytes
    model_pkl = pickle.dumps(model) 
    model_name = 'xgb-model'
    pkl_buffer = BytesIO(model_pkl)

    # Upload the CSV file to the bucket
    client.put_object(
        bucket_name=bucket_name,
        object_name=f"{model_name}_{current_date}.pkl", 
        data=pkl_buffer,
        length=len(model_pkl),
        content_type='application/octet-stream'
    )

    # List objects in the bucket
    objects = client.list_objects(bucket_name, recursive=True)
    for obj in objects:
        print(obj.object_name)