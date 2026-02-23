from infrastructure.database.models import TransactionModel


class TransactionRepository:

    def __init__(self, db_session):
        self.db = db_session

    def save(self, transaction, user_id):
        db_transaction = TransactionModel(
            user_id=user_id,
            date=transaction.date,
            description=transaction.description,
            amount=transaction.amount,
            category_id=transaction.category_id,
        )

        self.db.add(db_transaction)

    def commit(self):
        self.db.commit()