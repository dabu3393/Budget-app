from flask import Flask
from .routes import main_routes


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Register routes (blueprints)
    app.register_blueprint(main_routes)

    return app

# from app.services.transactions import Transaction
# from app.services.budget import Budget
# from app.services.accounts import Account