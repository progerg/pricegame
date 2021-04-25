from data.db_session import SqlAlchemyBase
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class GameSteam(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('games_egs.name'))
    logo_img = sqlalchemy.Column(sqlalchemy.String)
    icon_img = sqlalchemy.Column(sqlalchemy.String)
    appid = sqlalchemy.Column(sqlalchemy.Integer)
    discount_percent = sqlalchemy.Column(sqlalchemy.Integer)
    price = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    egs_game = orm.relation('GameEGS')
