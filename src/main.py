# Imports
import json  # To load JSON data
import pandas as pd  # To create DataFrame

# Load the JSON data from a file (replace 'file_path' with your actual file location)
with open('../data/mock_data.json', 'r') as f:
    data = json.load(f)

# Extract the 'accounts' section from the data
accounts_data = data['accounts']
# Convert the accounts data to a DataFrame
accounts_df = pd.DataFrame(accounts_data)

# Expand the 'balances' field into separate columns since it's nested inside each account
balances_df = accounts_df.pop('balances').apply(pd.Series)
# Merge the balances data back into the accounts DataFrame
accounts_df = pd.concat([accounts_df, balances_df], axis=1)

# Display the Accounts DataFrame
print("Accounts DataFrame:")
print(accounts_df)

# Extract the 'transactions' section from the data
transactions_data = data['transactions']
# Convert the transactions data to a DataFrame
transactions_df = pd.DataFrame(transactions_data)

# Display the Transactions DataFrame
print("\nTransactions DataFrame:")
print(transactions_df)

# Optionally, you can save the data to CSV files if needed
# accounts_df.to_csv('accounts.csv', index=False)
# transactions_df.to_csv('transactions.csv', index=False)

# -------------------------------------------------------------
# Budget System Implementation
# -------------------------------------------------------------

# Define a sample budget for each category
budget = {
    "Groceries": 400,
    "Rent": 1200,
    "Entertainment": 200,
    "Transportation": 150,
    "Utilities": 300,
    "Food and Drink": 150,
    "Miscellaneous": 100,  # Default for uncategorized transactions
    "Income": 0 # Budget for income is set to 0 by default
}

# Convert the budget dictionary to a DataFrame for easier manipulation
budget_df = pd.DataFrame(list(budget.items()), columns=['category', 'budgeted_amount'])

# A helper function to map transaction categories to the budget categories
def map_transaction_to_budget_category(transaction_categories):
    for category in transaction_categories:
        if category in budget:
            return category
    return "Miscellaneous"  # If no match found, categorize as "Miscellaneous"

# Apply the function to create a new 'budget_category' column in the transactions DataFrame
transactions_df['budget_category'] = transactions_df['category'].apply(map_transaction_to_budget_category)

# Group transactions by budget category and sum the amounts spent
spending_df = transactions_df.groupby('budget_category')['amount'].sum().reset_index()

spending_df.columns = ['category', 'spent_amount']

# Merge the budget DataFrame with the spending DataFrame to compare budget vs spending
budget_summary_df = pd.merge(budget_df, spending_df, on='category', how='left')

# Replace NaN values in spent_amount with 0 (if no transactions occurred in that category)
budget_summary_df['spent_amount'] = budget_summary_df['spent_amount'].fillna(0)


# Calculate the remaining budget for each category
budget_summary_df['remaining_budget'] = budget_summary_df['budgeted_amount'] + budget_summary_df['spent_amount']

# Display the budget summary
print("\nBudget Summary:")
print(budget_summary_df)

# Optionally, you can save the budget summary to a CSV file
# budget_summary_df.to_csv('budget_summary.csv', index=False)
