"""
    Функции сервера:
    принимает сообщение клиента;
    формирует ответ клиенту;
    отправляет ответ клиенту;
    имеет параметры командной строки:
        -p <port> — TCP-порт для работы (по умолчанию использует 7777);
        -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

import sys
import logging
import log.server_log_config
from socket import *
from datetime import datetime
from common.constant import DFL_PORT, DFL_ADDRESS, CONNECTIONS, ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ALERT
from common.transport import transport_receive, transport_send


# Получаем логгер
server_logger = logging.getLogger('server')


def protocol_server(dict_client):
    dict_server = {TIME: datetime.now().strftime('%H:%M:%S %d.%m.%Y')}
    # подготовка к отправке ответа клиенту
    if ACTION in dict_client.keys() and TIME in dict_client.keys() and USER in dict_client.keys() \
            and dict_client[ACTION] in ['presence', 'quit'] \
            and dict_client[TIME]:
        dict_server[RESPONSE] = '200'
        dict_server[ALERT] = 'ОК'

    else:
        dict_server[RESPONSE] = '400'
        dict_server[ALERT] = 'Error'

    server_logger.debug(f'Подготовлен клиенту "{dict_client[USER][ACCOUNT_NAME]}" ответ '
                        f'"{dict_server[RESPONSE]} {dict_server[ALERT]}"')
    return dict_server


def main():
    server_logger.info('Запуск сервера - обработка параметров командной строки ...')
    # обработка параметров командной строки
    try:
        # обработка порта
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = DFL_PORT
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра "-p " не указан номер порта.')
        server_logger.critical(f'После параметра "-p " не указан номер порта.')
        sys.exit(1)
    except ValueError:
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        server_logger.critical(f'Порт указан неверно "{sys.argv[sys.argv.index("-p") + 1]}". Задайте порт в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        # обработка IP-адреса
        if '-a' in sys.argv:
            address = sys.argv[sys.argv.index('-a') + 1]
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
    except (UnboundLocalError, IndexError):
        print('После параметра "-a " не указан IP-адрес.')
        server_logger.critical('После параметра "-a " не указан IP-адрес. Задайте IP-адрес в формате "000.000.000.000".')
        sys.exit(1)
    except ValueError:
        print('Задайте IP-адрес в формате "000.000.000.000".')
        server_logger.critical(f'IP-адрес указан неверно: "{sys.argv[sys.argv.index("-a") + 1]}". Задайте IP-адрес в формате "000.000.000.000".')
        sys.exit(1)

    # создаем TCP/IP сокет
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_address = (address, port)

    # привязываем сокет
    print(f'Start server {server_address}')
    server_logger.info(f'Запущен сервер с параметрами {server_address}')
    server_socket.bind(server_address)

    # слушаем подключения
    server_socket.listen(CONNECTIONS)

    while True:
        # ждем соединения
        connection, client_address = server_socket.accept()
        # принимаем данные от клиента и формируем ответ
        while True:
            # получаем запрос от клиента
            dict_client = transport_receive(connection)
            if not dict_client:
                break
            print(f'{dict_client[ACTION]} {dict_client[TIME]} {client_address} ')
            server_logger.debug(f'Получен от клиента "{dict_client[USER][ACCOUNT_NAME]}" запрос: "{dict_client[ACTION]} {dict_client[TIME]} {client_address}"')
            # отвечаем на запрос клиенту
            dict_server = protocol_server(dict_client)
            transport_send(connection, dict_server)
            server_logger.debug(f'Отправлен клиенту "{dict_client[USER][ACCOUNT_NAME]}" ответ "{dict_server[RESPONSE]} {dict_server[ALERT]}"')
        # очищаем соединение
        server_logger.warning(f'Соединение с клиентом закрыто')
        connection.close()


if __name__ == '__main__':
    main()
