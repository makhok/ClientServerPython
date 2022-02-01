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

import logging
import sys
import os
sys.path.append('../')


# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

# Создаем объект-логгер с именем 'client':
client_logger = logging.getLogger('client')

# Создаем объект форматирования:
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s ")

# Создаем файловый обработчик логирования:
file_handler = logging.FileHandler(PATH, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
client_logger.addHandler(file_handler)
client_logger.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    client_logger.critical('Критическая ошибка')
    client_logger.error('Ошибка')
    client_logger.debug('Отладочная информация')
    client_logger.info('Информационное сообщение')


