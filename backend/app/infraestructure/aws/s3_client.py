import boto3
from botocore.client import Config

BUCKET_NAME = "finance-invoices"

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url="http://localstack:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
        config=Config(signature_version="s3v4"),
    )

def create_bucket_if_not_exists():
    s3 = get_s3_client()

    existing_buckets = s3.list_buckets()
    bucket_names = [b["Name"] for b in existing_buckets.get("Buckets", [])]

    if BUCKET_NAME not in bucket_names:
        s3.create_bucket(Bucket=BUCKET_NAME)

def upload_file(file_bytes: bytes, filename: str):
    s3 = get_s3_client()
    
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=file_bytes,
        ContentType="application/pdf",
    )

    return f"s3://{BUCKET_NAME}/{filename}"