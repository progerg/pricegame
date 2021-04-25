from epicstore_api import EpicGamesStoreAPI, EGSProductType
from pprint import pprint
import sqlite3

con = sqlite3.connect("../db/game.db")

# Создание курсора
cur = con.cursor()

title = ''
api = EpicGamesStoreAPI()
games = api.fetch_store_games(count=1000, product_type=EGSProductType.PRODUCT_GAME, start=0)
data = games['data']['Catalog']['searchStore']['elements']
for i in data:
    title = i['title']
    discprice = i['price']['totalPrice']['discountPrice']
    origprice = i['price']['totalPrice']['originalPrice']
    if len(i['keyImages']) >= 2:
        image_1 = i['keyImages'][0]['url']
        image_2 = i['keyImages'][1]['url']
    elif len(i['keyImages']) == 1:
        image_1 = i['keyImages'][0]['url']
        image_2 = ''
    else:
        image_1 = ''
        image_2 = ''
    print(title, discprice, origprice, image_1, image_2)
    cur.execute('''INSERT INTO epic (name, discPrice, origPrice, image_1, image_2) VALUES (?,?,?,?,?)''', (title, discprice, origprice, image_1, image_2))
    con.commit()