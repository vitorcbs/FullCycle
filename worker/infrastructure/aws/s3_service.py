import boto3
import os

BUCKET_NAME = "finance-invoices"

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url="http://localstack:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

def download_invoice(filename: str) -> str:
    s3 = get_s3_client()

    local_path = f"/tmp/{filename}"

    s3.download_file(
        BUCKET_NAME,
        filename,
        local_path
    )

    return local_path