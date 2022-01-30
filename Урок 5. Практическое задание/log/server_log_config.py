"""
    Для проекта «Мессенджер» реализовать логирование с использованием модуля logging:

    1. В директории проекта создать каталог log, в котором для клиентской и серверной сторон в отдельных модулях
формата client_log_config.py и server_log_config.py создать логгеры;

    2. В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:
    создание именованного логгера;
    сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
    журналирование должно производиться в лог-файл;
    на стороне сервера необходимо настроить ежедневную ротацию лог-файлов.

    3. Реализовать применение созданных логгеров для решения двух задач:
    журналирование обработки исключений try/except. Вместо функции print() использовать журналирование и обеспечить
вывод служебных сообщений в лог-файл;
    журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.

"""


import logging.handlers
import sys
import os
sys.path.append('../')

# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

# Создаем объект-логгер с именем 'client':
server_logger = logging.getLogger('server')

# Создаем объект форматирования:
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s.%(funcName)s - %(message)s ")

# Создаем файловый обработчик логирования:
file_handler = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='D')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
server_logger.addHandler(file_handler)
server_logger.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    server_logger.critical('Критическая ошибка')
    server_logger.error('Ошибка')
    server_logger.debug('Отладочная информация')
    server_logger.info('Информационное сообщение')