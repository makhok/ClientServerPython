"""
    1. Продолжая задачу логирования, реализовать декоратор @log, фиксирующий обращение к декорируемой функции.
Он сохраняет ее имя и аргументы.
    2. В декораторе @log реализовать фиксацию функции, из которой была вызвана декорированная. Если имеется такой код:

    @log
    def func_z():
        pass

    def main():
        func_z()

...в логе должна быть отражена информация: "<дата-время> Функция func_z() вызвана из функции main"
"""

import logging
import traceback
import log.decorator_log_config

decorator_logger = logging.getLogger('decorator')


def log(log_func):
    def fixing_function(*args):
        decorator_logger.debug(f'Функция "{log_func.__name__}" вызвана из функции '
                               f'"{traceback.format_stack()[0].strip().split()[-1]}"')

        return log_func(*args)
    return fixing_function
