"""
    Функции клиента:
    сформировать presence-сообщение;
    отправить сообщение серверу;
    получить ответ сервера;
    разобрать сообщение сервера;
    параметры командной строки скрипта client.py <addr> [<port>]:
        addr — ip-адрес сервера;
        port — tcp-порт на сервере, по умолчанию 7777.
"""

import sys
import time
import logging
import log.client_log_config
from socket import *
from datetime import datetime
from common.transport import transport_send, transport_receive
from common.constant import DFL_PORT, DFL_ADDRESS, ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ALERT
from decorator import log

# Получаем логгер
client_logger = logging.getLogger('client')


@log
def protocol_client(data):

    dict_client = {ACTION: data, TIME: datetime.now().strftime('%H:%M:%S %d.%m.%Y'), USER: {ACCOUNT_NAME: 'Guest'}}
    # подготовка данных к отправке
    if dict_client[ACTION] == 'presence':
        dict_client['type'] = 'online'
    elif dict_client[ACTION] == 'quit':
        dict_client['type'] = 'offline'
    else:
        dict_client['type'] = 'offline'

    client_logger.debug(f'Подготовлен запрос "{dict_client[ACTION]}" от "{dict_client[USER][ACCOUNT_NAME]}" '
                        f'для отправки серверу')
    return dict_client


@log
def analysis_answer(dict_data, msg_service=None):

    if dict_data['response'] == '200':
        print(f'{dict_data[RESPONSE]} {dict_data[ALERT]} {dict_data[TIME]} {msg_service}')
        client_logger.debug(f'Получен ответ "{dict_data[RESPONSE]} {dict_data[ALERT]}" от сервера '
                            f'(правильный запрос/JSON-объект).')
    elif dict_data[RESPONSE] == '400':
        print(f'{dict_data[RESPONSE]} {dict_data[ALERT]} {dict_data[TIME]} Неправильный запрос!')
        client_logger.debug(f'Получен ответ "{dict_data[RESPONSE]} {dict_data[ALERT]}" от сервера '
                            f'(неправильный запрос/JSON-объект).')


def main():
    # обработка параметров командной строки
    client_logger.info('Запуск клиента - обработка параметров командной строки...')
    try:
        # обработка порта
        if len(sys.argv) >= 3:
            port = int(sys.argv[2])
        else:
            port = DFL_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        client_logger.critical('Порт указан неверно. Задайте порт в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        # обработка IP-адреса
        if len(sys.argv) >= 2:
            address = sys.argv[1]
            str_address = ''
            for i in address.split('.'):
                if len(address.split('.')) != 4:
                    raise ValueError
                if len(i) > 3:
                    raise ValueError
                if int(i):
                    str_address += i
        else:
            address = DFL_ADDRESS
    except (UnboundLocalError, IndexError, ValueError):
        print('Задайте IP-адрес в формате "000.000.000.000".')
        client_logger.critical('IP-адрес указан неверно. Задайте IP-адрес в формате "000.000.000.000".')
        sys.exit(1)

    # создаем TCP/IP сокет
    client_socket = socket(AF_INET, SOCK_STREAM)
    server_address = (address, port)

    try:
        client_socket.connect(server_address)
        client_logger.info(f'Подключен клиент к серверу с параметрами {server_address}')
        # формирование запроса
        dict_client = protocol_client('presence')
        print(f'{dict_client[ACTION]} {dict_client[USER][ACCOUNT_NAME]} {dict_client[TIME]}'
              f' Сервисный запрос на подключение {server_address}')
        time.sleep(2)
        # отправка запроса
        transport_send(client_socket, dict_client)
        client_logger.debug(f'Отправлен запрос "{dict_client[ACTION]}" от "{dict_client[USER][ACCOUNT_NAME]}" серверу')
        # получение ответа на запрос
        dict_server = transport_receive(client_socket)
        # разбор ответа
        analysis_answer(dict_server, 'Добро пожаловать!')

        print()
        time.sleep(3)

        if dict_client['type'] == 'online':
            # формирование запроса
            dict_client = protocol_client('quit')
            print(f'{dict_client[ACTION]} {dict_client[USER][ACCOUNT_NAME]} {dict_client[TIME]}'
                  f' Сервиcный запрос на отключение {server_address}')
            time.sleep(2)
            # отправка запроса
            transport_send(client_socket, dict_client)
            client_logger.debug(f'Отправлен запрос "{dict_client[ACTION]}" от "{dict_client[USER][ACCOUNT_NAME]}" серверу')
            # получение ответа
            dict_server = transport_receive(client_socket)
            # разбор ответа
            analysis_answer(dict_server, 'До свидания!')

    except (ConnectionError, OSError, TimeoutError, TypeError):
        print(f'Сервер {server_address} не отвечает!')
        client_logger.error(f'Сервер {server_address} не отвечает!')
    finally:
        client_logger.warning(f'Соединение клиента "{dict_client[USER][ACCOUNT_NAME]}" с сервером закрыто')
        client_socket.close()


if __name__ == '__main__':
    main()
