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