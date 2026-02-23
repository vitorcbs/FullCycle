from fastapi import APIRouter, UploadFile, File
from app.infraestructure.aws.s3_client import upload_file
import uuid
import json
from app.infraestructure.aws.sqs_client import send_message

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    contents = await file.read()

    filename = f"{uuid.uuid4()}.pdf"

    file_url = upload_file(contents, filename)

    send_message(json.dumps({
        "filename": filename
    }))

    return {
        "message": "Upload successful",
        "file_url": file_url,
    }