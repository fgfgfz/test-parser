"""Подключение к БД и отправление запросов."""

import pymysql
from config import host, port, user, password, database


def execute_query(connection, query, operation=None, insert=None):
    """
    Отправляет запрос к БД.
        params:
            :parameter connection: подключаемая БД
            :parameter query: тело запроса
            :parameter operation: описание запроса
            :parameter insert: является ли запрос вставкой записи (по умолчанию None)
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        print(f'{operation} successfully completed!')
        if insert:
            connection.commit()


def connect(orgs_list):
    """
    Подключение к БД и отправление запросов.
        params:
            :parameter orgs_list: список организаций
    """

    # Подключение к БД
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        print('\nПодключение прошло успешно!')

        try:
            # Создание таблицы
            create_table_query = "CREATE TABLE IF NOT EXISTS `orgs`(id INT AUTO_INCREMENT, " \
                                                                    "name VARCHAR(100), " \
                                                                    "ogrn VARCHAR(64), " \
                                                                    "okpo VARCHAR(64), " \
                                                                    "status VARCHAR(64), " \
                                                                    "reg_date VARCHAR(64), " \
                                                                    "capital VARCHAR(64), " \
                                                                    "PRIMARY KEY (id));"
            execute_query(connection, create_table_query, 'Создание таблицы')

            # Внесение данных
            count = 0
            for item in orgs_list:
                insert_orgs_query = f"INSERT INTO `orgs` (name, ogrn, okpo, status, reg_date, capital) VALUES " \
                                    f"('{item['title']}', " \
                                    f"'{item['ogrn']}', " \
                                    f"'{item['okpo']}', " \
                                    f"'{item['status']}', " \
                                    f"'{item['reg_date']}', " \
                                    f"'{item['capital']}');"
                count += 1
                execute_query(connection, insert_orgs_query, f'Занесение записи №{count}', True)

        finally:
            connection.close()

    except Exception as ex:
        print('Error...')
        print(ex)
