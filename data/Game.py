from data.db_session import SqlAlchemyBase
from datetime import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    st_id = sqlalchemy.Column(sqlalchemy.Integer)
    ep_id = sqlalchemy.Column(sqlalchemy.Integer)
    foll_profiles = sqlalchemy.Column(sqlalchemy.String)
    min_price = sqlalchemy.Column(sqlalchemy.Integer)
    steam_game = orm.relationship('SteamGameData', uselist=False)
    egs_game = orm.relationship('EGSGameData', uselist=False)
    name = sqlalchemy.Column(sqlalchemy.String)
    min_price = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
