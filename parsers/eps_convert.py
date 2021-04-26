from epicstore_api import EpicGamesStoreAPI, OfferData
from epicstore_api.exc import EGSException
from data.EGSGameData import EGSGameData
from data.SteamGameData import SteamGameData
from data.Game import Game
from data.db_session import *
from os.path import dirname


def get_slug(title: str) -> str:
    new_title = ''
    for i in title:
        if i.isdigit() or i.isalpha() or i == ' ':
            new_title += i
    return new_title.replace('  ', ' ').replace(' ', '-').replace('™', '').replace('®', '').replace("'", '').lower()


def main() -> None:
    global_init(f'C:/Users/Comp/Desktop/ProjectWeb/db/games.db')
    db_sess = create_session()
    egs_games = list(map(lambda x: x.to_dict(), db_sess.query(EGSGameData).all()))
    egs_games_dict = {}
    for i in range(len(egs_games)):
        egs_games_dict[get_slug(egs_games[i]['name'])] = egs_games[i]['id']
    steam_games = db_sess.query(SteamGameData).all()
    for i, game in enumerate(steam_games):
        model = Game(st_id=game.steam_appid)
        try:
            model.ep_id = egs_games_dict[get_slug(game.name)]
        except KeyError:
            pass
        db_sess.add(model)
        print(f'{i + 1}/{len(steam_games)}')
    for i in db_sess.query(EGSGameData).all():
        if not db_sess.query(Game).filter(Game.ep_id == i.id).first():
            game = Game(ep_id=i.id)
            db_sess.add(game)
    db_sess.commit()


if __name__ == '__main__':
    main()
