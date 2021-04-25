import requests
import sqlite3
from bs4 import BeautifulSoup

HEADERS = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/87.0.4280.66 Safari/537.36",
}

proxy = {
    "https": '192.162.192.148:55443',
    "http": '192.162.192.148:55443'
}

con = sqlite3.connect("../db/game.db")
# Создание курсора
cur = con.cursor()


def req(url, params=''):
    html = requests.get(url, headers=HEADERS, proxies=proxy)
    return html


def parsing(url):
    html = req(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    items = soup.find_all(class_='app')
    print(items[0]['data-appid'])
    return items[0]['data-appid']


res = cur.execute("""SELECT id, name FROM games""").fetchall()

for i in res[314:]:
    try:
        game = i[1]
        game = game.replace(' ', '+')
        print(game)
        a = parsing(f"https://steamdb.info/search/?a=app&q={game}&type=1&category=0")
        cur.execute(f"""UPDATE games SET steam_id={int(a)} WHERE id = {i[0]}""")
        con.commit()
    except Exception:
        print(i, "ОШИБКА")
