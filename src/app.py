import json

from flask import Flask, render_template
from src import Account,Transaction,Budget

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def budget_summary():
    # Load the JSON data
    with open('../data/mock_data.json', 'r') as f:
        data = json.load(f)

    # Initialize the Account and Transaction class
    transactions = Transaction(data['transactions'])

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

    return render_template('budget_summary.html')






