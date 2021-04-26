from requests import get, codes
from bs4 import BeautifulSoup
from json import dumps
from base64 import b64decode

page = 1
proxies_count = 0
proxies = []
while True:
    if page == 151:
        break
    response = get(f'http://free-proxy.cz/ru/proxylist/main/{page}')
    if response.status_code == codes['ok']:
        soup = BeautifulSoup(response.text, 'html.parser')
        info = soup.find(id='proxy_list').find_all('tr')
        for i in range(len(info)):
            proxy = info[i].find_all('td')
            if len(proxy) >= 3:
                ip = str(proxy[0]).split('.decode("')[1].split('"')[0]
                ip = b64decode(ip)
                proxies.append({proxy[2].get_text().lower(): f'{ip}:{proxy[1].get_text()}'})

                proxies_count += 1
                print(f'Проксей украдено: {proxies_count}')
        page += 1
    else:
        if response.status_code == 404:
            break
        print(f'Error {response.status_code}')

with open('proxies.json', 'w') as json:
    json.write(dumps(proxies))
