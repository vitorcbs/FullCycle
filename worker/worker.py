import boto3
import time
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.process_invoice import process_invoice


QUEUE_NAME = "invoice-processing"

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/ai_workspace"


# -------------------------
# Database
# -------------------------

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# -------------------------
# SQS
# -------------------------

def get_sqs_client():
    return boto3.client(
        "sqs",
        endpoint_url="http://localstack:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )


# -------------------------
# Message Handler
# -------------------------

def handle_message(filename: str, user_id: int):
    db = SessionLocal()

    try:
        process_invoice(
            filename=filename,
            user_id=user_id,
            db_session=db
        )
    finally:
        db.close()


# -------------------------
# Worker Loop
# -------------------------

def listen():
    print("🚀 Worker started")

    sqs = get_sqs_client()
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]

    while True:
        print("👂 Waiting for messages...")

        messages = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5,
        )

        if "Messages" in messages:
            for message in messages["Messages"]:
                body = json.loads(message["Body"])

                filename = body["filename"]

                # ⚠️ Por enquanto fixo
                user_id = 1

                print(f"📄 Processing file: {filename}")

                handle_message(filename, user_id)

                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message["ReceiptHandle"],
                )

        time.sleep(2)


if __name__ == "__main__":
    listen()