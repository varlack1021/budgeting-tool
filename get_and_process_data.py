
from datetime import datetime, date
import csv
from type_annotations import Transaction, DataSheetColumns, Categories
from rules import TRANSACTION_DESCIPTION_TO_CATEGORY
from typing import cast
import calendar

def makeStartDate():
    today = datetime.now()
    first_day = today.replace(day=1)
    first_day_iso = first_day.date()
    return first_day_iso

def makeEndDate():
    today = datetime.now()
    _, last_day_num = calendar.monthrange(today.year, today.month)
    last_day = today.replace(day=last_day_num)
    last_day_iso = last_day.date()
    return last_day_iso

def swap_leading_symbols(text: str) -> str:
    """Swaps a leading '-' with '+' and a leading '+' with '-'"""
    if text[0] == "-":
        return "+" + text[1:]
    elif text[0] == "+":
        return "-" + text[1:]
    else:
        return "-" + text

def reCategorize(transactions:list[Transaction]):
    targets = (TRANSACTION_DESCIPTION_TO_CATEGORY).keys()
    for transaction in transactions:
        for target in targets:
            if target.lower() in transaction["description"].lower():
                transaction['category'] = TRANSACTION_DESCIPTION_TO_CATEGORY[target]

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
    return makeStartDate() <= transaction["date"] <= makeEndDate()

def cleanTransactionData(data, ):
    return list(filter(withinDateRange, data))

def groupByCategory(transactions: list[Transaction])-> dict[str, list[Transaction]]:
    transactionByCategory:dict[str, list[Transaction]] = {category.value: [] for category in Categories}
    known_categories = [category.value for category in Categories]

    for transaction in transactions:
        category = transaction['category']
        if category in known_categories:
            transactionByCategory[transaction['category']].append(transaction)
        else:
            transactionByCategory[Categories.GuiltFree.value].append(transaction)
    return transactionByCategory
    

def getAndProcessData():
    data = getTransactionData()
    cleanedData = cleanTransactionData(data)
    reCategorize(cleanedData)
    transactionByCategory = groupByCategory(cleanedData)
    return transactionByCategory