import re
def parse_message(text: str):
    match = re.search(r"(.+?)\s+([\d]+[\.,]?[\d]*)$", text)

    if not match:
        raise ValueError("Formato invalido")
    
    description = match.group(1).strip()
    amount = float(match.group(2).replace(",", "."))

    return description, amount