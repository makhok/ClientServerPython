import logging
import sys
import os
sys.path.append('../')


# Подготовка имени файла для логирования
PATH = os.path.dirname(os.path.abspath(__file__))
if sys.argv[0].split('/')[-1] == 'server.py':
    PATH = os.path.join(PATH, 'server.log')
else:
    PATH = os.path.join(PATH, 'client.log')

# Создаем объект-логгер:
decorator_logger = logging.getLogger('decorator')

# Создаем объект форматирования:
formatter = logging.Formatter("%(asctime)s - %(message)s")

# Создаем файловый обработчик логирования для client:
file_handler_client = logging.FileHandler(PATH, encoding='utf-8')
file_handler_client.setLevel(logging.DEBUG)
file_handler_client.setFormatter(formatter)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
decorator_logger.addHandler(file_handler_client)
decorator_logger.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    decorator_logger.critical('Критическая ошибка')
    decorator_logger.error('Ошибка')
    decorator_logger.debug('Отладочная информация')
    decorator_logger.info('Информационное сообщение')
