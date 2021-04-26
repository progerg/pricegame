from data.db_session import *
from data.GameData import GameData
from data.DlcData import DlcData
from json import loads, dumps
from os import listdir
from sqlalchemy.exc import IntegrityError


def convert_to_db() -> None:
    global_init('db/games.db')
    db_sess = create_session()
    dirs = listdir('jsons')
    for index, i in enumerate(dirs):
        with open(f'jsons/{i}') as f:
            data = loads(f.read())
        if data:
            data = data['data']
            model = None
            if data['type'] == 'game':
                model = GameData(name=data['name'], is_free=data['is_free'],
                                 steam_appid=data['steam_appid'], header_image=data['header_image'],
                                 required_age=data['required_age'])
                for j in ['metacritic', 'screenshots', 'genres']:
                    try:
                        if j == 'genres':
                            setattr(model, j, ','.join(map(lambda x: x['description'], data[j])))
                        else:
                            setattr(model, j, dumps(data[j]))
                    except KeyError:
                        pass
            elif data['type'] == 'dlc':
                try:
                    model = DlcData(game_appid=data['fullgame']['appid'], name=data['name'],
                                    steam_appid=data['steam_appid'], is_free=data['is_free'],
                                    header_image=data['header_image'])
                except KeyError:
                    continue
                try:
                    model.metacritic = dumps(data['metacritic'])
                except KeyError:
                    pass
            try:
                model.initial_price = data['price_overview']['initial']
                model.final_price = data['price_overview']['final']
                model.discount_percents = data['price_overview']['discount_percent']
            except KeyError:
                if not data['is_free']:
                    continue

            if model:
                db_sess.add(model)
        print(f'{index + 1}/{len(dirs)}')
    db_sess.commit()


if __name__ == '__main__':
    convert_to_db()
