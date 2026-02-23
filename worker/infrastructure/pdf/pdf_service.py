import pdfplumber
import re
import unicodedata
from datetime import datetime
from domain.transaction import Transaction


MONTH_MAP = {
    "JAN": 1,
    "FEV": 2,
    "MAR": 3,
    "ABR": 4,
    "MAI": 5,
    "JUN": 6,
    "JUL": 7,
    "AGO": 8,
    "SET": 9,
    "OUT": 10,
    "NOV": 11,
    "DEZ": 12,
}


def normalize_text(text: str) -> str:
    # remove acentos
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ASCII", "ignore").decode("ASCII")

    # normaliza unicode estranho (− para -)
    text = text.replace("−", "-")

    return text


def extract_year(text: str) -> int:
    match = re.search(r"FATURA\s+\d{2}\s+[A-Z]{3}\s+(\d{4})", text)
    if match:
        return int(match.group(1))

    raise ValueError("Ano da fatura não encontrado")


def parse_nubank_invoice(file_path: str) -> list[Transaction]:
    transactions = []

    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    text = normalize_text(text)

    # extrai ano automaticamente
    year = extract_year(text)

    # Regex mais robusto:
    TRANSACTION_PATTERN = re.compile(
        r"^(\d{2})\s+(JAN|FEV|MAR|ABR|MAI|JUN|JUL|AGO|SET|OUT|NOV|DEZ).*?([\d]+\,[\d]{2})$"
    )

    matches = re.findall(TRANSACTION_PATTERN, text)

    for day, month_str, description, amount_str in matches:

        # ignora pagamentos
        if "PAGAMENTO" in description.upper():
            continue

        month = MONTH_MAP[month_str]
        date_obj = datetime(year, month, int(day)).date()

        amount = float(amount_str.replace(".", "").replace(",", "."))

        transactions.append(
            Transaction(
                date=date_obj,
                description=description.strip(),
                amount=amount,
                category_id=None,  # temporário
            )
        )

    return transactions