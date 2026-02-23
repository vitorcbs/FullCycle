from infrastructure.aws.s3_service import download_invoice
from infrastructure.pdf.pdf_service import parse_nubank_invoice
from repositories.category_rule_repository import (
    CategoryRuleRepository,
)
from repositories.transaction_repository import (
    TransactionRepository,
)
from application.categorize_transaction import categorize_transaction
from support.get_other_category_id import get_other_category_id


def process_invoice(filename: str, user_id: int, db_session):
    file_path = download_invoice(filename)

    transactions = parse_nubank_invoice(file_path)

    rule_repo = CategoryRuleRepository(db_session)
    print("USER ID:", user_id)
    rules = rule_repo.get_rules_by_user(user_id)
    print("Rules encontradas:", rules)
    print("Qtd rules:", len(rules))

    transaction_repo = TransactionRepository(db_session)

    for transaction in transactions:
        print(repr(transaction.description))
        category_id = categorize_transaction(
            transaction.description,
            rules
        )

        if not category_id:
            category_id = get_other_category_id(user_id, db_session)

        transaction.category_id = category_id

        transaction_repo.save(transaction, user_id)

    transaction_repo.commit()
   