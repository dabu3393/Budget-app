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