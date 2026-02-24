from sqlalchemy import text


class TransactionRepository:
    def __init__(self, db_session):
        self.db = db_session

    def save(self, transaction, user_id):
        query = text(
            """
            INSERT INTO transactions (user_id, date, description, amount, category_id)
            VALUES (:user_id, :date, :description, :amount, :category_id)
            """
        )

        self.db.execute(
            query,
            {
                "user_id": user_id,
                "date": transaction.date,
                "description": transaction.description,
                "amount": transaction.amount,
                "category_id": transaction.category_id,
            },
        )

    def commit(self):
        self.db.commit()
