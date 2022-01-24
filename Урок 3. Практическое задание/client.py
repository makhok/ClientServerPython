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
from socket import *
from datetime import datetime
from transport import transport_send, transport_receive


def protocol_client(data):
    dict_data = {'time': datetime.now().strftime('%H:%M:%S %d.%m.%Y')}
    # подготовка данных к отправке
    if data == 'presence':
        dict_data['action'] = 'presence'
        dict_data['type'] = 'online'
        dict_data['user'] = {'account_name': 'Guest'}
        return dict_data

    if data == 'quit':
        dict_data['action'] = 'quit'
        dict_data['type'] = 'offline'
        dict_data['user'] = {'account_name': 'Guest'}
        return dict_data


def main():
    # обработка параметров командной строки
    try:
        # обработка порта
        if len(sys.argv) >= 3:
            port = int(sys.argv[2])
        else:
            port = 7777
        if port < 1024 or port > 65535:
            raise ValueError
    except ValueError:
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
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
            address = '127.0.0.1'
    except (UnboundLocalError, IndexError, ValueError):
        print('Задайте IP-адрес в формате "000.000.000.000".')
        sys.exit(1)

    # создаем TCP/IP сокет
    client_socket = socket(AF_INET, SOCK_STREAM)
    server_address = (address, port)
    client_socket.connect(server_address)

    try:
        # формирование запроса
        data = protocol_client('presence')
        print(f'{data["action"]} {data["user"]["account_name"]} - {data["type"]} {data["time"]} Сервисный запрос на подключение {server_address}')
        time.sleep(2)
        # отправка запроса
        transport_send(client_socket, data)
        # получение ответа
        data = transport_receive(client_socket)
        print(f'{data["response"]} {data["alert"]} {data["time"]} Добро пожаловать! {server_address}')

        print()
        time.sleep(3)

        # формирование запроса
        data = protocol_client('quit')
        print(f'{data["action"]} {data["user"]["account_name"]} - {data["type"]} {data["time"]} Сервиcный запрос на отключение {server_address}')
        time.sleep(2)
        # отправка запроса
        transport_send(client_socket, data)
        # получение ответа
        data = transport_receive(client_socket)
        print(f'{data["response"]} {data["alert"]} {data["time"]} До свиданья! {server_address}')

    except (ConnectionRefusedError, TimeoutError):
        print(f'Сервер {server_address} не отвечает!')
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
