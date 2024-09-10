import json
import pandas as pd


# Class for handling Accounts
class Account:
    def __init__(self, account_data):
        self.account_data = account_data
        self.accounts_df = self.process_account_data()

    def process_account_data(self):
        accounts_df = pd.DataFrame(self.account_data)
        balances_df = accounts_df.pop('balances').apply(pd.Series)  # Expand nested balances
        return pd.concat([accounts_df, balances_df], axis=1)

    def display_accounts(self):
        print("Accounts DataFrame:")
        print(self.accounts_df)


# Class for handling Transactions
class Transaction:
    def __init__(self, transaction_data):
        self.transaction_data = transaction_data
        self.transactions_df = pd.DataFrame(transaction_data)

    def map_transaction_to_budget_category(self, budget):
        # Helper function to map transactions to budget categories
        def mapper(transaction_categories):
            for category in transaction_categories:
                if category in budget:
                    return category
            return "Miscellaneous"  # Default category if no match found

        self.transactions_df['budget_category'] = self.transactions_df['category'].apply(mapper)

    def display_transactions(self):
        print("\nTransactions DataFrame:")
        print(self.transactions_df)


# Class for managing Budget
class Budget:
    def __init__(self, budget_dict):
        self.budget = budget_dict
        self.budget_df = pd.DataFrame(list(budget_dict.items()), columns=['category', 'budgeted_amount'])

    def calculate_spending(self, transactions_df):
        # Group transactions by budget category and sum the amounts
        spending_df = transactions_df.groupby('budget_category')['amount'].sum().reset_index()
        spending_df.columns = ['category', 'spent_amount']

        # Merge with budget
        self.budget_summary_df = pd.merge(self.budget_df, spending_df, on='category', how='left')
        self.budget_summary_df['spent_amount'] = self.budget_summary_df['spent_amount'].fillna(0)
        self.budget_summary_df['remaining_budget'] = self.budget_summary_df['budgeted_amount'] + self.budget_summary_df[
            'spent_amount']

    def display_budget_summary(self):
        print("\nBudget Summary:")
        print(self.budget_summary_df)


# -------------------------------------------------------------
# Main Application Flow
# -------------------------------------------------------------

# Load the JSON data
with open('../data/mock_data.json', 'r') as f:
    data = json.load(f)

# Initialize the Account class
accounts = Account(data['accounts'])
accounts.display_accounts()

# Initialize the Transaction class
transactions = Transaction(data['transactions'])
transactions.display_transactions()

# Define the budget
budget_data = {
    "Groceries": 400,
    "Rent": 1200,
    "Entertainment": 200,
    "Transportation": 150,
    "Utilities": 300,
    "Food and Drink": 150,
    "Miscellaneous": 100,
    "Income": 0
}

# Initialize the Budget class and calculate remaining budget
budget = Budget(budget_data)
transactions.map_transaction_to_budget_category(budget.budget)  # Map transactions to budget categories
budget.calculate_spending(transactions.transactions_df)
budget.display_budget_summary()
