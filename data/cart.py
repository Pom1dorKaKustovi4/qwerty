import sqlalchemy

from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase):
    __tablename__ = 'cart'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    price_steam = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price_egs = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price_gog = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    links = sqlalchemy.Column(sqlalchemy.Text, nullable=True)