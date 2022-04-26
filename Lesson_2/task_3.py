# 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
# YAML-формата. Для этого: Подготовить данные для записи в виде словаря, в котором первому ключу соответствует
# список, второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с
# юникод-символом, отсутствующим в кодировке ASCII (например, €); Реализовать сохранение данных в файл формата YAML —
# например, в файл file.yaml. При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
# а также установить возможность работы с юникодом: allow_unicode = True; Реализовать считывание данных из созданного
# файла и проверить, совпадают ли они с исходными.

import yaml

DATA = {
    'items': ['computer', 'printer', 'mouse'],
    'items_price': {
        'computer': '200\N{euro sign} - 1000\N{euro sign}',
        'printer': '5\N{euro sign} - 50\N{euro sign}',
        'mouse': '400\N{ruble sign} - 700\N{ruble sign}'
    },
    'item_quantity': 3
}
FILENAME = 'data.yaml'


def write_to_yaml(data, filename):
    with open(filename, 'w') as f_n:
        yaml.dump(data, f_n, default_flow_style=False, allow_unicode=True, sort_keys=False)

    with open(filename) as f_n:
        print(f_n.read())


if __name__ == '__main__':
    write_to_yaml(DATA, FILENAME)
