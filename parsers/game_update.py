from data.db_session import *
from data.Game import Game
from data.Sales import Sales


def main():
    global_init('db/games.db')
    db = create_session()
    games = db.query(Game).all()
    for game in games:
        if game.steam_game:
            game.name = game.steam_game.name
        else:
            game.name = game.egs_game.name
        price1 = price2 = 10 ** 10
        if game.steam_game:
            price1 = game.steam_game.final_price
        if game.egs_game:
            price2 = game.egs_game.final_price
        min_price = min(price1, price2)
        if game.min_price != min_price:
            sales = Sales(game_id=game.id, new_price=min_price)
            db.add(sales)
            game.min_price = min_price
    db.commit()


if __name__ == '__main__':
    main()
