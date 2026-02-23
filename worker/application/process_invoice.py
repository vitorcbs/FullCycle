from infrastructure.aws.s3_service import download_invoice
from infrastructure.pdf.pdf_service import parse_nubank_invoice
from repositories.category_rule_repository import (
    CategoryRuleRepository,
)
from repositories.transaction_repository import (
    TransactionRepository,
)
from application.categorize_transaction import categorize_transaction


def process_invoice(filename: str, user_id: int, db_session):
    # 1. baixar
    file_path = download_invoice(filename)

    # 2. extrair transações
    transactions = parse_nubank_invoice(file_path)

    # 3. buscar regras do usuário
    rule_repo = CategoryRuleRepository(db_session)
    print("USER ID:", user_id)
    rules = rule_repo.get_rules_by_user(user_id)
    print("Rules encontradas:", rules)
    print("Qtd rules:", len(rules))

    # 4. repository de transação
    transaction_repo = TransactionRepository(db_session)

    for transaction in transactions:
        print(repr(transaction.description))
        category_id = categorize_transaction(
            transaction.description,
            rules
        )

        transaction.category_id = category_id

        transaction_repo.save(transaction, user_id)

    transaction_repo.commit()
   