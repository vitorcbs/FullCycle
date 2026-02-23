from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infraestructure.aws.s3_client import create_bucket_if_not_exists
from app.infraestructure.aws.sqs_client import create_queue_if_not_exists
from app.interfaces.http.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_bucket_if_not_exists()
    create_queue_if_not_exists()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
