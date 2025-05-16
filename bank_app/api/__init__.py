from bank_app.api.routes import bank_bp
from bank_app.api.loan_routes import loan_bp

def init_app(app):
    """
    register all blueprints with the Flask app
    """
    app.register_blueprint(bank_bp)
    app.register_blueprint(loan_bp)
