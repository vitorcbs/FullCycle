import unicodedata


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ASCII", "ignore").decode("ASCII")
    return text.upper().strip()


def categorize_transaction(description: str, rules: list):
    desc = normalize_text(description)
    
    sorted_rules = sorted(
        rules,
        key=lambda r: (r.priority, -len(r.keyword))
    )

    for rule in sorted_rules:
        keyword = normalize_text(rule.keyword)

        if keyword in desc:
            return rule.category_id

    return None