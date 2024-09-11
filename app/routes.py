from flask import Blueprint, render_template
import json
from .services.transactions import Transaction
from .services.budget import Budget

# Create a blueprint for the routes
main_routes = Blueprint('main', __name__)


@main_routes.route('/')
def index():
    return render_template('index.html')


@main_routes.route('/budget')
def budget_summary():
    with open('data/mock_data.json', 'r') as f:
        data = json.load(f)

    transactions = Transaction(data['transactions'])

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

    budget = Budget(budget_data)
    transactions.map_transaction_to_budget_category(budget.budget)
    budget.calculate_spending(transactions.transactions_df)

    return render_template('budget_summary.html',
                           budget=budget.budget_summary_df.to_html(),
                           categories=budget.budget_summary_df['category'].tolist(),
                           budgeted_amounts=budget.budget_summary_df['budgeted_amount'].tolist(),
                           spent_amounts=budget.budget_summary_df['spent_amount'].abs().tolist(),
                           zip=zip)
