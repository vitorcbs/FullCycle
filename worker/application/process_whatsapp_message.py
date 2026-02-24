from repositories.category_rule_repository import CategoryRuleRepository
from repositories.transaction_repository import TransactionRepository
from infrastructure.message.message_service import parse_message
from application.categorize_transaction import categorize_transaction
from support.get_other_category_id import get_other_category_id
from domain.transaction import Transaction
from datetime import date


def process_whatsapp_message(message_text: str, user_id: int, db_session):

    rule_repo = CategoryRuleRepository(db_session)
    transaction_repo = TransactionRepository(db_session)

    rules = rule_repo.get_rules_by_user(user_id)

    description, amount = parse_message(message_text)

    category_id = categorize_transaction(description, rules)

    if not category_id:
        category_id = get_other_category_id(user_id, db_session)

    transaction_repo.save(
        Transaction(
            date=date.today(),
            description=description,
            amount=amount,
            category_id=category_id
        ),
        user_id
    )

    transaction_repo.commit()