"""
    Функции сервера:
    принимает сообщение клиента;
    формирует ответ клиенту;
    отправляет ответ клиенту;
    имеет параметры командной строки:
        -p <port> — TCP-порт для работы (по умолчанию использует 7777);
        -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""
import select
import sys
import logging
import log.server_log_config
from socket import *
from datetime import datetime
from common.constant import DFL_PORT, DFL_ADDRESS, CONNECTIONS, ACTION, TIME, USER, ACCOUNT_NAME, RESPONSE, ALERT, TO, \
    FROM
from common.transport import transport_receive, transport_send
from decorator import log

# Получаем логгер
server_logger = logging.getLogger('server')


@log
def protocol_server(dict_client):
    dict_server = {TIME: datetime.now().strftime('%H:%M:%S %d.%m.%Y')}
    # подготовка к отправке ответа клиенту
    if ACTION in dict_client.keys() and TIME in dict_client.keys() and USER in dict_client.keys() \
            and dict_client[ACTION] in ['presence', 'quit', 'msg'] \
            and dict_client[TIME]:
        dict_server[RESPONSE] = '200'
        dict_server[ALERT] = 'ОК'

    else:
        dict_server[RESPONSE] = '400'
        dict_server[ALERT] = 'Error'

    server_logger.debug(f'Подготовлен ответ "{dict_server[RESPONSE]} {dict_server[ALERT]}" '
                        f'для клиента "{dict_client[USER][ACCOUNT_NAME]}"')
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
        server_logger.critical(f'Порт указан неверно "{sys.argv[sys.argv.index("-p") + 1]}". '
                               f'Задайте порт в диапазоне от 1024 до 65535.')
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
        server_logger.critical('После параметра "-a " не указан IP-адрес. '
                               'Задайте IP-адрес в формате "000.000.000.000".')
        sys.exit(1)
    except ValueError:
        print('Задайте IP-адрес в формате "000.000.000.000".')
        server_logger.critical(f'IP-адрес указан неверно: "{sys.argv[sys.argv.index("-a") + 1]}". '
                               f'Задайте IP-адрес в формате "000.000.000.000".')
        sys.exit(1)

    # создаем TCP/IP сокет
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setblocking(0)
    server_address = (address, port)

    # привязываем сокет
    print(f'Start server {server_address}')
    server_logger.info(f'Запущен сервер с параметрами {server_address}')
    server_socket.bind(server_address)

    # слушаем подключения
    server_socket.listen(CONNECTIONS)

    messages = {}
    clients = {}
    inputs = [server_socket]
    outputs = []
    excepts = []


    while True:

        read, write, exp = select.select(inputs, outputs, excepts)

        # ПОЛУЧАЕМ ЗАПРОСЫ
        for r in read:
            if r == server_socket:
                # Пришел новый клиент, принимаем подключение
                connection, client_address = r.accept()
                print(f'Клиент {client_address} подключился!')
                # Устанавливаем неблокирующийся сокет
                connection.setblocking(0)
                # Добавляем сокет нового клиента на прослушивание
                inputs.append(connection)
            else:
                # Получаем запрос от клиента
                dict_client = transport_receive(r)

                if dict_client:
                    print(f'{dict_client[ACTION]} {dict_client[TIME]} [{dict_client[USER][ACCOUNT_NAME]}] ')
                    server_logger.debug(f'Получен запрос "{dict_client[ACTION]}" '
                                        f'от клиента "{dict_client[USER][ACCOUNT_NAME]}" ')

                    # Создаем словарь пользователей
                    if dict_client[USER][ACCOUNT_NAME] not in clients.keys():
                        clients[dict_client[USER][ACCOUNT_NAME]] = r

                    # Кладем сообщение в словарь
                    if messages.get(r, None):
                        messages[r].append(dict_client)
                        if dict_client[ACTION] == 'msg':
                            messages[clients[dict_client[USER][ACCOUNT_NAME]]].append(dict_client)
                    else:
                        messages[r] = [dict_client]
                        if dict_client[ACTION] == 'msg':
                            messages[clients[dict_client[USER][ACCOUNT_NAME]]] = [dict_client]

                    # Добавляем соединение клиента в очередь на готовность к приему сообщений
                    if r not in outputs:
                        outputs.append(r)

                    if dict_client[ACTION] == 'msg':
                        if clients[dict_client[TO]] not in outputs:
                            outputs.append(clients[dict_client[TO]])

                else:
                    print(f'Клиент {r.getpeername()} отключился!')
                    server_logger.warning(f'Клиент {r.getpeername()} отключился!')
                    # Очищаем соединение

                    inputs.remove(r)
                    #del clients[messages[r][[USER][ACCOUNT_NAME]]]

                    del messages[r]
                    r.close()

        # ОТПРАВЛЯЕМ ЗАПРОСЫ
        for w in write:
            # Выбираем из словаря сообщения для текущего сокета
            msg = messages.get(w, None)
            if msg:
                if msg[0][ACTION] == 'msg' and msg[0][TO] == msg[0][USER][ACCOUNT_NAME]:
                    transport_send(w, msg[0])

                elif msg[0][ACTION] == 'msg' and msg[0][TO] != msg[0][USER][ACCOUNT_NAME]:
                    transport_send(clients[msg[0][TO]], msg[0])


                # Формируем ответы сервера
                dict_server = protocol_server(msg.pop(0))
                transport_send(w, dict_server)
                server_logger.debug(f'Отправлен ответ "{dict_server[RESPONSE]} {dict_server[ALERT]}" '
                                    f'клиенту "{dict_client[USER][ACCOUNT_NAME]}"')
            else:
                # Удаляем из очереди сокетов, готовых принять сообщение
                outputs.remove(w)


        # ОБРАБАТЫВАЕМ ОШИБКИ
        for e in exp:
            print('Клиент отвалился ...')
            inputs.remove(e)
            if e in outputs:
                outputs.remove(e)
            e.close()
            del messages[e]


        """
        # принимаем данные от клиента и формируем ответ
        while True:
            # получаем запрос от клиента
            dict_client = transport_receive(connection)
            if not dict_client:
                break
            print(f'{dict_client[ACTION]} {dict_client[TIME]} {client_address} ')
            server_logger.debug(f'Получен запрос "{dict_client[ACTION]}" '
                                f'от клиента "{dict_client[USER][ACCOUNT_NAME]}" ')
            # отвечаем на запрос клиенту
            dict_server = protocol_server(dict_client)
            transport_send(connection, dict_server)
            server_logger.debug(f'Отправлен ответ "{dict_server[RESPONSE]} {dict_server[ALERT]}" '
                                f'клиенту "{dict_client[USER][ACCOUNT_NAME]}"')
        """




if __name__ == '__main__':
    main()
