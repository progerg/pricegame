from data.db_session import SqlAlchemyBase
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class EGSGameData(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'epic'

    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('games.ep_id'), primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    initial_price = sqlalchemy.Column(sqlalchemy.Integer)
    final_price = sqlalchemy.Column(sqlalchemy.Integer)
    image_1 = sqlalchemy.Column(sqlalchemy.String)
    image_2 = sqlalchemy.Column(sqlalchemy.String)
    url = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
