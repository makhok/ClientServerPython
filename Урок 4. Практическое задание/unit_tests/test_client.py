"""
    Для всех функций из урока 3 написать тесты с использованием unittest.
Они должны быть оформлены в отдельных скриптах с префиксом test_ в имени файла
(например, test_client.py).
"""

import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))
from client import protocol_client

class TestClass(unittest.TestCase):

    def test_protocol_client(self):

        test_object = protocol_client('presence')
        self.assertEqual(test_object, {'time': test_object['time'], 'action': 'presence',
                                'type': 'online', 'user': {'account_name': 'Guest'}})

        test_object = protocol_client('quit')
        self.assertEqual(test_object, {'time': test_object['time'], 'action': 'quit',
                                'type': 'offline', 'user': {'account_name': 'Guest'}})

    def test_protocol_client_type(self):
        self.assertEqual(type(protocol_client('presence')), type({}))
        self.assertEqual(type(protocol_client('quit')), type({}))


if __name__ == '__main__':
    unittest.main()
