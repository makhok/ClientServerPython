"""
    Функции приема-передачи
"""

import json


def transport_send(sock, data):
    sock.send(json.dumps(data).encode())


def transport_receive(connect):
    data = connect.recv(1024)
    if not data:
        return None
    rez = json.loads(data.decode())
    return rez

