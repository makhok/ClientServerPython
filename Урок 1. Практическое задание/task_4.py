"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    str_byte = word.encode('utf-8')
    byte_str = str_byte.decode('utf-8')
    print()
    print(f'{word} ({type(word)})')
    print(f'{str_byte} ({type(str_byte)})')
    print(f'{byte_str} ({type(byte_str)})')

