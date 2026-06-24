from typing import TypedDict
from enum import IntEnum
from datetime import date
from enum import Enum

class Categories(str, Enum):
    Comics='Comics'
    Groceries='Groceries' # Costco, stew, stop & shop, whole foods
    GuiltFree='GuiltFree'
    Insurance='Insurance' # US AAA
    Miscellaneous='Miscellaneous'# Amazon
    Phone='Phone'
    Subscriptions='Subscriptions' #Crunchyroll, Spotify, icloud, triple A, costco membership dues, obsidian
    Transportation='Transportation'

class Transaction(TypedDict):
    date: date
    category: Categories
    amount: str
    description: str

class DataSheetColumns(IntEnum):
    TRANSACTION_DATE=0
    DESCRIPTION=2
    CATEGORY=3
    AMOUNT=5