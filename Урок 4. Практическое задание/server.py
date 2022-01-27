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
from socket import *
from datetime import datetime
from common.transport import transport_receive, transport_send


def protocol_server(dict_client):
    dict_server = {'time': datetime.now().strftime('%H:%M:%S %d.%m.%Y')}
    # подготовка к отправке ответа клиенту
    if 'action' in dict_client.keys() and 'time' in dict_client.keys() and 'user' in dict_client.keys() \
            and dict_client['action'] in ['presence', 'quit'] \
            and dict_client['time']:

        dict_server['response'] = '200'
        dict_server['alert'] = 'ОК'
        return dict_server

    else:
        dict_server['response'] = '400'
        dict_server['alert'] = 'Error'
        return dict_server


def main():
    # обработка параметров командной строки
    try:
        # обработка порта
        if '-p' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            port = 7777
        if port < 1024 or port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра "-p " необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print('В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
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
            address = '127.0.0.1'
    except (UnboundLocalError, IndexError):
        print('После параметра "-a " необходимо указать IP-адрес.')
        sys.exit(1)
    except ValueError:
        print('Задайте IP-адрес в формате "000.000.000.000".')
        sys.exit(1)

    # создаем TCP/IP сокет
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_address = (address, port)

    # привязываем сокет
    print(f'Start server {server_address}')
    server_socket.bind(server_address)

    # слушаем подключения
    server_socket.listen(5)

    while True:
        # ждем соединения
        connection, client_address = server_socket.accept()
        # принимаем данные от клиента и формируем ответ
        while True:
            # получаем запрос от клиента
            data = transport_receive(connection)
            if not data:
                break
            print(f'{data["action"]} {data["time"]} {client_address} ')
            # отвечаем на запрос клиенту
            data = protocol_server(data)
            transport_send(connection, data)
        # очищаем соединение
        connection.close()


if __name__ == '__main__':
    main()
