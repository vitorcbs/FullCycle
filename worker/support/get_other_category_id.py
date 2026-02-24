from sqlalchemy import text


def get_other_category_id(user_id, db_session):
    query = text(
        """
        SELECT id
        FROM categories
        WHERE user_id = :user_id
          AND name = 'Outros'
        LIMIT 1
        """
    )

    row = db_session.execute(query, {"user_id": user_id}).mappings().first()

    return row["id"] if row else None
