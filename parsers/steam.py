import requests
import json
import sqlite3
from pprint import pprint

HEADERS = {
    'user-agent': "Mozilla/5.0 (X11; FreeBSD amd64; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/87.0.4280.88 Safari/537.36"
}

con = sqlite3.connect("../db/game.db")

# Создание курсора
cur = con.cursor()

res = cur.execute("""SELECT id, name, steam_id FROM games WHERE id < 314 AND id > 35""").fetchall()


def parsing(url, id):
    ID = str(id)
    response = requests.get(url, headers=HEADERS, params={'appids': ID})
    json_response = response.json()
    is_free = json_response[ID]['data']['is_free']
    header_image = json_response[ID]['data']['header_image']
    name = json_response[ID]['data']['name']
    if not is_free:
        initial_price = json_response[ID]['data']['price_overview']['initial_formatted']
        final_price = json_response[ID]['data']['price_overview']['final_formatted']
        discount_percent = json_response[ID]['data']['price_overview']['discount_percent']
        print(name, '-', initial_price, final_price, discount_percent, header_image)
        cur.execute("""INSERT INTO steam_games (name, discPrice, origPrice, image,  steam_id) VALUES (?,?,?,?,?)""",
                    (name, final_price, initial_price, header_image, ID))
        con.commit()


for i in res:
    print(i)
    if i[2] is None:
        continue
    else:
        try:
            parsing('https://store.steampowered.com/api/appdetails/', i[2])
        except Exception as err:
            print(err)
