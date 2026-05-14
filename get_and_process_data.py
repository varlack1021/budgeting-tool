
from datetime import datetime, date
import csv
from type_annotations import Transaction, DataSheetColumns, Categories, CategorySummary
from typing import cast, Mapping


START_DATE = date.fromisoformat("2026-05-01")
END_DATE = date.fromisoformat("2026-05-30")

DESCIPTION_TO_CATEGORY: dict[str, Categories] = {
    # Groceries
    'Costco': Categories.Groceries,
    'STEWLEONARD': Categories.Groceries,
    #Miscellaneous
    'Amazon': Categories.Miscellaneous,
    'COSTCO *ANNUAL RENEWAL': Categories.Miscellaneous,
    #Insurance
    'USAA': Categories.Insurance,

    #Subscriptions
    'AAA MEMBERSHIP DUES': Categories.Subscriptions,
    'CrunchyRoll':  Categories.Subscriptions,
    'Obsidian': Categories.Subscriptions,
    'Apple': Categories.Subscriptions,

    # Guilt Free
    'Teng and Sons': Categories.GuiltFree,

    # Transportation
    'Shell OIL': Categories.Transportation
}

def swap_leading_symbols(text: str) -> str:
    """Swaps a leading '-' with '+' and a leading '+' with '-'"""
    if text[0] == "-":
        return "+" + text[1:]
    elif text[0] == "+":
        return "-" + text[1:]
    return text

def reCategorize(transactions:list[Transaction]):
    targets = (DESCIPTION_TO_CATEGORY).keys()
    for transaction in transactions:
        for target in targets:
            if target.lower() in transaction["description"].lower():
                transaction['category'] = DESCIPTION_TO_CATEGORY[target]

def getTransactionData()-> list[Transaction]:
    data: list[Transaction] = []
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            transaction: Transaction = {
                "date": datetime.strptime(row[DataSheetColumns.TRANSACTION_DATE], "%m/%d/%Y").date(),
                "description": row[DataSheetColumns.DESCRIPTION],
                "amount": swap_leading_symbols(row[DataSheetColumns.AMOUNT]),
                "category": cast(Categories, row[DataSheetColumns.CATEGORY],)
            }
            data.append(transaction)
    return data


def withinDateRange(transaction: Transaction):
    return START_DATE <= transaction["date"] <= END_DATE

def cleanTransactionData(data, ):
    return list(filter(withinDateRange, data))

def groupByCategory(transactions: list[Transaction])-> dict[str, CategorySummary]:
    transactionByCategory:dict[str, CategorySummary] = {category.value: {"transactions": []} for category in Categories}
    known_categories = [category.value for category in Categories]

    for transaction in transactions:
        category = transaction['category']
        if category in known_categories:
            summary = transactionByCategory[transaction['category']]
            summary['transactions'].append(transaction)
        else:
            transactionByCategory['GuiltFree']['transactions'].append(transaction)
    return transactionByCategory
    

def getAndProcessData():
    data = getTransactionData()
    cleanedData = cleanTransactionData(data)
    reCategorize(cleanedData)
    transactionByCategory = groupByCategory(cleanedData)
    return transactionByCategory