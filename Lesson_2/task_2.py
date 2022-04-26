# 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
# скрипт, автоматизирующий его заполнение данными. Для этого: Создать функцию write_order_to_json(),
# в которую передается 5 параметров — товар (item), количество (quantity), цена (price), покупатель (buyer),
# дата (date). Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных
# указать величину отступа в 4 пробельных символа; Проверить работу программы через вызов функции
# write_order_to_json() с передачей в нее значений каждого параметра.

import json

ORDERS = [
    {
        'item': 'printer',
        'quantity': '32',
        'price': '7999',
        'buyer': 'John Doe',
        'date': '11.08.2020'
    },
    {
        'item': 'scanner',
        'quantity': '42',
        'price': '12999',
        'buyer': 'Vasiliy',
        'date': '16.11.2020'
    },
    {
        'item': 'ноутбук',
        'quantity': '2',
        'price': '40999',
        'buyer': 'John Doe',
        'date': '23.07.2020'
    },
    {
        'item': 'keyboard',
        'quantity': '12',
        'price': '999',
        'buyer': 'Сергей',
        'date': '11.01.2021'
    }
]
FILENAME = 'orders.json'


def write_order_to_json(item, quantity, price, buyer, date):
    dict_to_json = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    with open(FILENAME, 'r') as file:
        json_order = json.load(file)
        json_order.get('orders').append(dict_to_json)

    with open(FILENAME, 'w') as file:
        json.dump(json_order, file, ensure_ascii=False, indent=4)

    with open(FILENAME) as file:
        print(file.read())


if __name__ == '__main__':
    [write_order_to_json(*order.values()) for order in ORDERS]
