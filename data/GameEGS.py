from data.db_session import SqlAlchemyBase
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class GameEGS(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'games_egs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    disc_price = sqlalchemy.Column(sqlalchemy.Integer)
    orig_price = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

