from typing import TypedDict
from enum import IntEnum
from datetime import date

class Transaction(TypedDict):
    date: date
    category: str
    amount: str
    description: str

class DataSheetColumns(IntEnum):
    TRANSACTION_DATE=0
    DESCRIPTION=2
    CATEGORY=3
    AMOUNT=5