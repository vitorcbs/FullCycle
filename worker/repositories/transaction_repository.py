from sqlalchemy.orm import Session
from infrastructure.database.models import TransactionModel


class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, transaction, user_id: int):
        model = TransactionModel(
            user_id=user_id,
            date=transaction.date,
            description=transaction.description,
            amount=transaction.amount,
            category_id=transaction.category_id,
        )

        self.db.add(model)

    def commit(self):
        self.db.commit()