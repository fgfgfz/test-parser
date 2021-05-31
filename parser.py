"""Парсер сайта https://www.rusprofile.ru."""

import requests
from bs4 import BeautifulSoup
import db
import proxy

URL1 = 'https://www.rusprofile.ru/codes/89220'
URL2 = 'https://www.rusprofile.ru/codes/429110'
PROXIES = proxy.get_proxies()

organisations = []


def get_html(url, proxies):
    """
    Получение HTML кода страниы.
        params:
            :parameter url: url страницы
            :parameter proxies: прокси-сервер
    """

    response = requests.get(url, proxies=proxies)
    return response


def get_pages_count(html):
    """
    Получение количества страниц данных.
        params:
            :parameter html: html код страницы
    """

    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('li')
    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1


def get_content(html):
    """
    Получение данных страницы.
        params:
            :parameter html: html код страницы
    """

    # Получение HTML кода данных
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='company-item')

    organisations = []
    for item in items:

        # Проверка наличия статуса
        status = item.find('div', class_='company-item-status')
        if status:
            status = status.get_text()
        else:
            status = 'Действующая организация'

        # Составление кортежа с данными организации
        item_info = item.find_all('div', class_='company-item-info')[1].get_text().split('\n')
        item_info = list(filter(None, item_info))
        item_info_dict = {}
        for i in range(0, len(item_info) - 1, 2):
            item_info_dict[item_info[i]] = item_info[i + 1]

        # Добавление кортежа данных организации в список
        organisations.append({
            'title': item.find('div', class_='company-item__title').get_text(strip=True),
            'ogrn': item_info_dict.get('ОГРН'),
            'okpo': item_info_dict.get('ИНН'),
            'status': status,
            'reg_date': item_info_dict.get('Дата регистрации'),
            'capital': item_info_dict.get('Уставный капитал')
        })

    return organisations


def parse(url, proxies):
    """
    Парсинг страницы сайта.
        params:
            :parameter url: url страницы
            :parameter proxies: прокси-сервер
    """

    # Получение HTML кода страницы
    html = get_html(url, PROXIES)

    if html.status_code == 200:
        organisations = []
        pages_count = get_pages_count(html.text)

        # Парсинг данных постранично
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(url + '/' + str(page) + '/', proxies=proxies)
            organisations.extend(get_content(html.text))

        print(f'Получено организаций: {len(organisations)}')
        return organisations

    else:
        print('Error')


organisations.extend(parse(URL1, PROXIES))
organisations.extend(parse(URL2, PROXIES))
print(f'Всего получено организаций: {len(organisations)}')
db.connect(organisations)
