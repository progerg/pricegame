from stem import Signal
from stem.control import Controller
import requests
from json import dumps, loads
import asyncio
import aiohttp
from aiohttp_socks import ProxyConnector

key = '9BF2E94FABA6F8675FFDB50DE7A8B6DC'
params = {'key': key, 'format': 'json'}


async def get_tor_session():
    proxy = 'socks5://127.0.0.1:9050'
    headers = {'Users-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/51.0.2704.103'}
    connector = ProxyConnector.from_url(proxy)
    sess = aiohttp.ClientSession(connector=connector, headers=headers)
    return sess


async def renew_connection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="16:864330436B19F02A60505FBD53B891A0DE716F921B89B9938B96569BB3")
        controller.signal(Signal.NEWNYM)


async def get_current_ip(session):
    try:
        async with session.get('http://httpbin.org/ip') as resp:
            print(await resp.read())
    except Exception as e:
        print(str(e))


async def save_json(json_list: list, i) -> None:
    with open(f'jsons/{i}.json', 'w') as f:
        f.write(dumps(json_list))


async def main():
    await renew_connection()
    session = await get_tor_session()
    async with session.get('http://api.steampowered.com/ISteamApps/GetAppList/v0002',
                           params=params) as resp:
        games_list = loads(await resp.read())
    games_list = games_list['applist']['apps']

    length = len(games_list)
    print('Games list completed')

    full_games_list = []
    for index, game_info in enumerate(games_list):
        while True:
            try:
                async with session.get('https://store.steampowered.com/api/appdetails',
                                       params={'appids': str(game_info['appid']), 'cc': 'ru'}) as response:
                    if response:
                        if response.status == 200:
                            info = loads(await response.read())
                            info = info[str(game_info['appid'])]
                            if info['success'] and info['data']['type'] in ('game', 'dlc'):
                                await save_json(info, game_info['appid'])
                                full_games_list.append(info)
                                full_games_list[-1]['appid'] = game_info['appid']
                            print(f'Completed {index + 1}/{length}')

                            break
                        else:
                            print(f'Error: {response.status}')

            except Exception as err:
                print(f'Error {err}')
            await session.close()
            await renew_connection()
            await asyncio.sleep(10)
            print('New Tor Connection was created')
            session = await get_tor_session()
            await get_current_ip(session)


if __name__ == '__main__':
    asyncio.run(main())
