from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

database = SQLAlchemy()
password_hasher = PasswordHasher()

class User(UserMixin, database.Model):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(64), unique=True, nullable=False)
    password_hash = database.Column(database.String(256))

    def set_password(self, password):
        self.password_hash = password_hasher.hash(password)

    def check_password(self, password):
        try:
            password_hasher.verify(self.password_hash, password)
            return True
        except VerifyMismatchError:
            return False
