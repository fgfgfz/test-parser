"""Получение списка бесплатных прокси серверов и выбор случайного из них."""

import requests
import random
from bs4 import BeautifulSoup as bs


def get_free_proxies():
    """Получение списка бесплатных прокси серверов."""

    url = "https://free-proxy-list.net/"
    soup = bs(requests.get(url).content, "html.parser")
    free_proxies = []
    for row in soup.find("table", attrs={"id": "proxylisttable"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            host = f"{ip}:{port}"
            free_proxies.append(host)
        except IndexError:
            continue
    print(f'Обнаружено бесплатных прокси - {len(free_proxies)}:')
    return free_proxies


def get_proxies():
    """Выбор случайного прокси сервера."""

    free_proxies = get_free_proxies()
    proxy = random.choice(free_proxies)
    proxies = {'http://': proxy}
    print(f'Выбран прокси {proxies}\n')
    return proxies
