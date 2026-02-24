from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class CategoryRuleRecord:
    keyword: str
    category_id: int
    priority: int


class CategoryRuleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_rules_by_user(self, user_id: int):
        query = text(
            """
            SELECT keyword, category_id, priority
            FROM category_rules
            WHERE user_id = :user_id
            ORDER BY priority ASC
            """
        )

        rows = self.db.execute(query, {"user_id": user_id}).mappings().all()

        return [
            CategoryRuleRecord(
                keyword=row["keyword"],
                category_id=row["category_id"],
                priority=row["priority"],
            )
            for row in rows
        ]
