from epicstore_api import EpicGamesStoreAPI
import json
import sqlite3
from pprint import pprint

con = sqlite3.connect("../db/game.db")

# Создание курсора
cur = con.cursor()


def main():
    api = EpicGamesStoreAPI()
    games = api.fetch_catalog(count=1000)
    print(len(games['data']['Catalog']['catalogOffers']['elements']))
    for i in games['data']['Catalog']['catalogOffers']['elements']:
        cur.execute("""INSERT INTO epicgames (name, discPrice, origPrice, image) VALUES (?,?,?,?)""",
                    (i['title'], i['price']['totalPrice']['discountPrice'], i['price']['totalPrice']['originalPrice'],
                     i['keyImages'][1]['url']))
        con.commit()
        # print('API Response:\n', json.dumps(games, indent=4))


if __name__ == '__main__':
    main()
