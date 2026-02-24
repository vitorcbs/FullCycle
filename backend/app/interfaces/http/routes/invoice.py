from fastapi import APIRouter, UploadFile, File
from app.infraestructure.aws.s3_client import upload_file
from app.infraestructure.aws.sqs_client import send_message
from app.infraestructure.aws.message_schema import QueueMessage
import uuid

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    contents = await file.read()

    filename = f"{uuid.uuid4()}.pdf"

    file_url = upload_file(contents, filename)

    message = QueueMessage.create(
        event_type="invoice.uploaded",
        user_id=1,
        payload={"filename": filename},
    )
    send_message(message)

    return {
        "message": "Upload successful",
        "file_url": file_url,
    }
