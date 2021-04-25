import sqlite3
from bs4 import BeautifulSoup
import time
import requests

# Подключение к БД
con = sqlite3.connect("../db/game.db")

# Создание курсора
cur = con.cursor()

HEADERS = {
    'user-agent': "Mozilla/5.0 (X11; FreeBSD amd64; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/87.0.4280.88 Safari/537.36"
}


def req(key, params=''):
    html = requests.get(f'https://kanobu.ru/games/pc/popular/?years=2015-2019&page={key}', headers=HEADERS, params=params)
    return html


for i in range(1, 361):
    try:
        html = req(key=i)
        soup = BeautifulSoup(html.text, 'html.parser')
        res = soup.find_all(class_="c-game__option")
        for j in res:
            print(i, j.a.get_text())
            name = j.a.get_text()
            time.sleep(0.1)
            cur.execute("""INSERT INTO games (name) VALUES (?)""", (name, ))
            con.commit()
    except Exception:
        print(i, 'ОШИБКА')

con.close()

