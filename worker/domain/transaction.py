from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Transaction:
    date: date
    description: str
    amount: float
    category_id: Optional[int] = None