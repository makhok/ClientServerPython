"""
    Для всех функций из урока 3 написать тесты с использованием unittest.
Они должны быть оформлены в отдельных скриптах с префиксом test_ в имени файла
(например, test_client.py).
"""

import sys
import os
import json
from datetime import datetime
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.transport import transport_send, transport_receive


class TestSocket:
    """
    Тестовый класс для тестирования отправки и получения
    """
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.enc_msg = None
        self.rec_msg = None

    def send(self, transport_send):
        """
        Тестовая функция отправки, корретно  кодирует сообщение,
        так-же сохраняет что должно было отправлено в сокет.
        transport_send - то, что отправляем в сокет
        """
        json_test_message = json.dumps(self.test_dict)
        # кодирует сообщение
        self.enc_msg = json_test_message.encode()
        # сохраняем что должно было отправлено в сокет
        self.rec_msg = transport_send

    def recv(self, transport_receive):
        """
        Получаем данные из сокета
        """
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode()


class Tests(unittest.TestCase):
    """
    Тестовый класс.
    """
    test_dict_send = {'time': datetime.now().strftime('%H:%M:%S %d.%m.%Y'), 'action': 'presence', 'user': {'account_name': 'Guest'}}
    test_dict_recv_ok = {'200': 'OK'}
    test_dict_recv_err = {'400': 'Error'}

    def test_transport_send(self):
        """
        Тестируем корректность работы фукции отправки,
        создадим тестовый сокет и проверим корректность отправки словаря
        """
        # экземпляр тестового сокета, хранит собственно тестовый словарь
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        transport_send(test_socket, self.test_dict_send)
        # проверка корретности кодирования словаря.
        # сравниваем результат кодирования и результат от тестируемой функции
        self.assertEqual(test_socket.enc_msg, test_socket.rec_msg)

    def test_transport_receive(self):
        """
        Тест функции приёма сообщения
        """
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # тест корректной расшифровки корректного словаря
        self.assertEqual(transport_receive(test_sock_ok), self.test_dict_recv_ok)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(transport_receive(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()

