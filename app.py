from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import Config
from models import database, User
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
database.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import routes after app initialization to avoid circular imports
from routes import *

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def init_db():
    with app.app_context():
        database.create_all()
        # Create admin user if it doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin')
            database.session.add(admin)
            database.session.commit()

if __name__ == '__main__':
    # Create the database and admin user
    if not os.path.exists('app.db'):
        init_db()
    app.run(port=5002, debug=True)
