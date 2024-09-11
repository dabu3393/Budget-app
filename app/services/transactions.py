import pandas as pd


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