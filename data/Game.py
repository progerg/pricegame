from data.db_session import SqlAlchemyBase
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'main_games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_st = sqlalchemy.Column(sqlalchemy.Integer)
    id_ep = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String)
    st_price = sqlalchemy.Column(sqlalchemy.Integer)
    ep_price = sqlalchemy.Column(sqlalchemy.Integer)
    image = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
