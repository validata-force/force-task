import os
from flask import Flask
from dotenv import load_dotenv

def create_app(test_config=None):
    """
    configure the Flask application
    """
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'dev_key_for_development_only')
    if test_config is not None:
        app.config.update(test_config)
    from bank_app.db import init_app as init_db
    init_db(app)
    from bank_app.api import init_app as init_api
    init_api(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
