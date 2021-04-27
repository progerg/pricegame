from data.db_session import SqlAlchemyBase
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Sales(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'sales'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('games.id'))
    new_price = sqlalchemy.Column(sqlalchemy.Integer)

    game = orm.relationship('Game', backref='sale')

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
