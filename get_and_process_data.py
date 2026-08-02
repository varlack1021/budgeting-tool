
from datetime import datetime, date
import csv
from type_annotations import Transaction, DataSheetColumns, Categories
from rules import TRANSACTION_DESCIPTION_TO_CATEGORY, TRANSACTIONS_TO_IGNORE
from typing import cast
import calendar
import os
from pathlib import Path

def isIgnoredTransaction(transaction: str)-> bool:
    for item in TRANSACTIONS_TO_IGNORE:
        if (item.lower() in transaction.lower()):
            return True
    return False

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

def getTransactionData(filePath)-> list[Transaction]:
    data: list[Transaction] = []
    with open(filePath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            description = row[DataSheetColumns.DESCRIPTION]
            if (isIgnoredTransaction(description)):
                continue
            transaction: Transaction = {
                "date": datetime.strptime(row[DataSheetColumns.TRANSACTION_DATE], "%m/%d/%Y").date(),
                "description": description,
                "amount": swap_leading_symbols(row[DataSheetColumns.AMOUNT]),
                "category": cast(Categories, row[DataSheetColumns.CATEGORY],)
            }
            data.append(transaction)
    return data

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
    

def getFilePath():
# Automatically locates your system Downloads directory
    downloads_path = Path.home() / "Downloads"

    # Find all CSV files that start with 'Chase' (case-insensitive search)
    chase_files = []

    for f in downloads_path.glob("*.CSV"):
        if f.name.lower().startswith("chase"):
            chase_files.append(f)
    

    if not chase_files:
        print("No Chase CSV files found in Downloads.")
        return None

    # Get the file with the most recent modification time
    latest_file = max(chase_files, key=lambda f: f.stat().st_mtime)

    return latest_file

def getAndProcessData():
    filePath = getFilePath()
    data = getTransactionData(filePath)
    reCategorize(data)
    transactionByCategory = groupByCategory(data)
    return transactionByCategory