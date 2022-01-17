"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""

import subprocess
import chardet


def ping_web(name):
    args = ['ping', name]
    subproc_ping = subprocess.Popen(args, stdout=subprocess.PIPE)
    for byte in subproc_ping.stdout:
        result = chardet.detect(byte)
        print(byte.decode(result['encoding']).encode('utf-8').decode('utf-8'))


ping_web('yandex.ru')
ping_web('youtube.com')

