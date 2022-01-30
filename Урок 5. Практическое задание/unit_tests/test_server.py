"""
    Для всех функций из урока 3 написать тесты с использованием unittest.
Они должны быть оформлены в отдельных скриптах с префиксом test_ в имени файла
(например, test_client.py).
"""

import sys
import os
from datetime import datetime
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import protocol_server


class TestClass(unittest.TestCase):

    ok_dict = {'response': '200', 'alert': 'ОК', 'time': datetime.now().strftime('%H:%M:%S %d.%m.%Y')}
    error_dict = {'response': '400', 'alert': 'Error', 'time': datetime.now().strftime('%H:%M:%S %d.%m.%Y')}

    # Корректный запрос
    def test_protocol_server(self):
        tested_object = protocol_server({'time': self.ok_dict['time'], 'action': 'presence', 'user': {'account_name': 'Guest'}})
        self.assertEqual(tested_object, self.ok_dict)

    # Ошибка если нет 'action'
    def test_protocol_server_no_action(self):
        tested_object = protocol_server({'time': self.error_dict['time'], 'user': {'account_name': 'Guest'}})
        self.assertEqual(tested_object, self.error_dict)

    # Ошибка если нет 'time'
    def test_protocol_server_no_time(self):
        tested_object = protocol_server({'action': 'presence', 'user': {'account_name': 'Guest'}})
        self.assertEqual(tested_object, self.error_dict)


if __name__ == '__main__':
    unittest.main()
