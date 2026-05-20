This is a tool for personal budgeting

# Setup

## Setup Service Account
1. Setup a service account in google
2. Download the service account credenitals as json
3. Add the service account in the root of the repo. Must be named `service_account.json`
3. Share the google sheet folder with the email used to create the service account

## Add Data Set

The script expects the dataset to be configured as follows
- Must be a CSV file
- Must be named `data`

# Adding a Rule

 The script matches a transaction to a category by using the category provided in the csv file if the category is a known category.
 If the transaction is not a known category or is not in the override rules then it is labelled as `GUILT FREE`.

 The override rules match a rule to a transaction by doing a simple string match. That is, if the override transaction rule exists within the target string it will be considered a match. String matching is case insensitive. 

 Example:

 This will match:
 ```
 Transaction: "TST COSTCO"
 Rule: "COSTCO": Category.Groceries
 ```

 This will not match:
 ```
  Transaction: "COSTCO Renewal"
  Rule: "Costco Annual Renewal": Category.Subscriptions
 ```

 To add an override rule, update `rules.py` with the string to match the transaction with and the desired Category.