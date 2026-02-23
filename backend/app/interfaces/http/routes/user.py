from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.deps import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)

    return service.register_user(
        email=data.email,
        name=data.name,
        password_hash=data.password
    )
