from sqlalchemy.orm import Session
from infrastructure.database.models import CategoryRule


class CategoryRuleRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_rules_by_user(self, user_id: int):
        """
        Retorna todas as regras do usuário ordenadas por prioridade
        """
        return (
            self.db.query(CategoryRule)
            .filter(CategoryRule.user_id == user_id)
            .order_by(CategoryRule.priority.asc())
            .all()
        )