from data.db_session import SqlAlchemyBase
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class DlcData(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'dlc'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    steam_appid = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String)
    initial_price = sqlalchemy.Column(sqlalchemy.Integer)
    final_price = sqlalchemy.Column(sqlalchemy.Integer)
    discount_percents = sqlalchemy.Column(sqlalchemy.Integer)
    header_image = sqlalchemy.Column(sqlalchemy.String)
    game_appid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('game.steam_appid'))
    metacritic = sqlalchemy.Column(sqlalchemy.JSON)
    is_free = sqlalchemy.Column(sqlalchemy.Boolean)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
