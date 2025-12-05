
from datetime import datetime, date
import csv
from type_annotations import Transaction, DataSheetColumns
from pprint import pprint

START_DATE = date.fromisoformat("2025-11-01")
END_DATE = date.fromisoformat("2025-11-30")

def getTransactionData()-> list[Transaction]:
    data: list[Transaction] = []
    with open('data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            transaction: Transaction = {
                "date": datetime.strptime(row[DataSheetColumns.TRANSACTION_DATE], "%m/%d/%Y").date(),
                "description": row[DataSheetColumns.DESCRIPTION],
                "amount": row[DataSheetColumns.AMOUNT],
                "category": row[DataSheetColumns.CATEGORY]
            }
            data.append(transaction)
    return data


def withinDateRange(transaction: Transaction):
    return START_DATE <= transaction["date"] <= END_DATE

def cleanTransactionData(data, ):
    return list(filter(withinDateRange, data))

def main():
    data = getTransactionData()
    cleanedData = cleanTransactionData(data)
    pprint(cleanedData)
main()