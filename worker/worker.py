import json
import time

import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from application.process_invoice import process_invoice
from infrastructure.aws.message_schema import QueueMessage
from repositories.processing_status_repository import ProcessingStatusRepository


QUEUE_NAME = "invoice-processing"
DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/ai_workspace"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_sqs_client():
    return boto3.client(
        "sqs",
        endpoint_url="http://localstack:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )


def handle_message(message: QueueMessage):
    db = SessionLocal()
    status_repo = ProcessingStatusRepository(db)

    try:
        existing_status = status_repo.get_by_message_id(message.message_id)
        if existing_status and existing_status.status == "done":
            return

        status_repo.start(message.message_id, message.event_type)

        if message.event_type == "invoice.uploaded":
            process_invoice(
                filename=message.payload["filename"],
                user_id=message.user_id,
                db_session=db,
            )
        else:
            raise ValueError(f"Unsupported event_type: {message.event_type}")

        status_repo.mark_done(message.message_id)

    except Exception as exc:
        status_repo.mark_failed(message.message_id, str(exc))
        raise
    finally:
        db.close()


def listen():
    print("🚀 Worker started")

    sqs = get_sqs_client()
    queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)["QueueUrl"]

    while True:
        messages = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10,
            VisibilityTimeout=45,
        )

        for raw_message in messages.get("Messages", []):
            try:
                envelope = QueueMessage.from_dict(json.loads(raw_message["Body"]))
                handle_message(envelope)

                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=raw_message["ReceiptHandle"],
                )
            except Exception as exc:
                print(f"❌ Failed to process message: {exc}")

        time.sleep(1)


if __name__ == "__main__":
    listen()
