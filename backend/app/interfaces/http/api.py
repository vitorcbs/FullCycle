from fastapi import APIRouter
from app.interfaces.http.routes.invoice import router as invoice_router
from app.interfaces.http.routes.user import router as user_router

api_router = APIRouter()

api_router.include_router(invoice_router)
api_router.include_router(user_router)