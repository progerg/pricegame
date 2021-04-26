from data.db_session import SqlAlchemyBase
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class SteamGameData(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'steam_games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    initial_price = sqlalchemy.Column(sqlalchemy.Integer)
    final_price = sqlalchemy.Column(sqlalchemy.Integer)
    discount_percents = sqlalchemy.Column(sqlalchemy.Integer)
    header_image = sqlalchemy.Column(sqlalchemy.String)
    is_free = sqlalchemy.Column(sqlalchemy.Boolean)
    steam_appid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('games.st_id'))
    screenshots = sqlalchemy.Column(sqlalchemy.JSON)
    metacritic = sqlalchemy.Column(sqlalchemy.JSON)
    genres = sqlalchemy.Column(sqlalchemy.String)
    required_age = sqlalchemy.Column(sqlalchemy.Integer)
    dlc = orm.relationship('DlcData')

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
