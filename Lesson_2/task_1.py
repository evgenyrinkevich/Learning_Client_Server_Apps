# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из
# файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого: Создать
# функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. В
# этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
# соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
# os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и
# поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
# каждого файла); Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать
# получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий
# CSV-файл; Проверить работу программы через вызов функции write_to_csv().

import csv

FILES = ['info_1.txt', 'info_2.txt', 'info_3.txt']
KEYS = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']


def get_data(files_list, keys_to_parse) -> list:
    """
    Returns values of keys_to_parse in all files in files_list
    """
    res_list = [keys_to_parse]
    for file in files_list:
        with open(file, 'rb') as f:
            row = [None] * len(keys_to_parse)
            counter = 0
            for line in f:
                # тут пытался через chardet, но detect работает некорректно, пришлось захардкодить
                text = line.decode('windows-1251')
                for key in keys_to_parse:
                    if key in text:
                        row[keys_to_parse.index(key)] = text[len(key) + 1:].strip()
                        counter += 1
                if counter == len(keys_to_parse):
                    break  # выходим когда нашли все ключи в файле

            res_list.append(row)

    return res_list


def write_to_csv(data_to_csv, filename):
    """
    Writes data_to_csv to filename and prints the contents of file
    """
    with open(filename, 'w') as f_n:
        writer = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        for row in data_to_csv:
            writer.writerow(row)
    with open(filename) as f_n:
        print(f_n.read())


if __name__ == '__main__':
    data = get_data(FILES, KEYS)
    write_to_csv(data, 'task_1.csv')
