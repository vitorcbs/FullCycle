import boto3

QUEUE_NAME = "invoice-processing"

def get_sqs_client():
    return boto3.client(
        "sqs",
        endpoint_url="http://localstack:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )

def create_queue_if_not_exists():
    sqs = get_sqs_client()
    sqs.create_queue(QueueName=QUEUE_NAME)

def send_message(message: str):
    sqs = get_sqs_client()
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]

    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
    )