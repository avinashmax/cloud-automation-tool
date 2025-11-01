import boto3
import logging
import os
from botocore.exceptions import ClientError

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

s3_client = boto3.client('s3', region_name='ap-south-1')

def list_buckets():
    try:
        response = s3_client.list_buckets()
        print("\n=== S3 Buckets ===")
        for bucket in response['Buckets']:
            print(f"🪣 {bucket['Name']}")
        logging.info("Listed S3 buckets successfully.")
    except ClientError as e:
        print(f"❌ Error listing buckets: {e}")
        logging.error(f"Error listing buckets: {e}")

def create_bucket(bucket_name):
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'}
        )
        print(f"✅ Bucket '{bucket_name}' created successfully.")
        logging.info(f"Bucket '{bucket_name}' created.")
    except ClientError as e:
        print(f"❌ Error creating bucket: {e}")
        logging.error(f"Error creating bucket: {e}")

def upload_file(bucket_name, file_path):
    try:
        file_name = os.path.basename(file_path)
        s3_client.upload_file(file_path, bucket_name, file_name)
        print(f"✅ File '{file_name}' uploaded to '{bucket_name}'.")
        logging.info(f"Uploaded {file_name} to {bucket_name}.")
    except ClientError as e:
        print(f"❌ Error uploading file: {e}")
        logging.error(f"Error uploading file: {e}")

def download_file(bucket_name, file_name, destination_path):
    try:
        s3_client.download_file(bucket_name, file_name, destination_path)
        print(f"✅ File '{file_name}' downloaded to '{destination_path}'.")
        logging.info(f"Downloaded {file_name} from {bucket_name}.")
    except ClientError as e:
        print(f"❌ Error downloading file: {e}")
        logging.error(f"Error downloading file: {e}")
