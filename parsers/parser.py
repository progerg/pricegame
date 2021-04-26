from stem import Signal
from stem.control import Controller
import requests
from json import dumps, loads
import time
# Нет таких слов в русском языке, чтобы описать тот ужас, когда
# спарсилось 79000 запросов, а потом выскочила ошибка, что
# в запросе нет json`а. А ты не сохранял промежуточно запросы и ловил исключения
# только RequestException. Хотя даже если бы все ловил, то все равно бы не сохранил значения.
# Асинхронка выдает ошибку на рандомном запросе и стирает весь json. Парсер бесплатных проксей?
# Зачем ты его сделал, стим блокирует большинство бесплатных проксей
# И конечно, ошибки вылезают только к запросу 10000, ведь лучше подождать побольше
# А еще json открываешь и все лагает, а ведь сейчас только 30000 из 114000 спарсилось,
# да и сам json в 210мб уже. А где Дарк Соулс 3? В бд его нет, но мне уже все равно, там и так много игр

key = '9BF2E94FABA6F8675FFDB50DE7A8B6DC'
params = {'key': key, 'format': 'json'}


def get_tor_session():
    sess = requests.session()
    sess.proxies = {'http': 'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'}
    return sess


def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="16:864330436B19F02A60505FBD53B891A0DE716F921B89B9938B96569BB3")
        controller.signal(Signal.NEWNYM)


def get_current_ip(session):
    try:
        r = session.get('http://httpbin.org/ip')
        return r.text
    except Exception as e:
        print(str(e))


def main():
    renew_connection()
    session = get_tor_session()
    with session.get('http://api.steampowered.com/ISteamApps/GetAppList/v0002',
                     params=params) as resp:
        print(resp.content)
        games_list = resp.json()['applist']['apps']

    length = len(games_list)
    print('Games list completed')

    full_games_list = []
    for index, game_info in enumerate(games_list):
        while True:
            try:
                with session.get('https://store.steampowered.com/api/appdetails',
                                 params={'appids': str(game_info['appid']), 'cc': 'ru'}) as response:
                    print(response.content)
                    if response.status_code == requests.codes['ok']:
                        info = response.json()[str(game_info['appid'])]
                        if info['success'] and info['data']['type'] in ('game', 'dlc'):
                            with open(f'jsons/{game_info["appid"]}.json', 'w') as f:
                                f.write(dumps(info))
                            full_games_list.append(info)
                            full_games_list[-1]['appid'] = game_info['appid']
                        print(f'Completed {index + 1}/{length}')
                        break

                    print(f'Error: {response.status_code}')

            except Exception as err:
                print(f'Error {err}')
            renew_connection()
            time.sleep(10)
            print('New Tor Connection was created')
            session = get_tor_session()
            print(get_current_ip(session))


if __name__ == '__main__':
    main()
