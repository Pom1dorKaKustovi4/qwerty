import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cart = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    product = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("cart.id"), nullable=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self.id} {self.email} {self.user_name} {self.hashed_password} {self.cart}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        User(hashed_password=self.hashed_password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
