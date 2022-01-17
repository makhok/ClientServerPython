"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv


def get_data(files):

    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

    # считывание данных из файла и извлечение значений, указанных параметров данных
    for index, file in enumerate(files):
        with open(file, encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                if 'Изготовитель системы' in line:
                    os_prod_list.append(line.split(':')[-1].strip())

                if 'Название ОС' in line:
                    os_name_list.append(line.split(':')[-1].strip())

                if 'Код продукта' in line:
                    os_code_list.append(line.split(':')[-1].strip())

                if 'Тип системы' in line:
                    os_type_list.append(line.split(':')[-1].strip())

        main_data.append([f'{index+1}', os_prod_list[-1], os_name_list[-1], os_code_list[-1], os_type_list[-1]])

    # сохранение данных в файл main_data
    with open('main_data.txt', 'w', encoding='utf-8') as f:
        for data in main_data:
            f.write(f'{"".join(data)}\n')
        return main_data


def write_to_csv(file_csv):
    with open(file_csv, 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f)
        # получение данных через вызов функции get_data(), а также сохранение подготовленных данных
        # в соответствующий CSV-файл
        data = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])
        for row in data:
            f_writer.writerow(row)

    # чтение CSV-файла для проверки результата
    with open(file_csv, encoding='utf-8') as f:
        print(f.read())


write_to_csv('my_data_report.csv')



