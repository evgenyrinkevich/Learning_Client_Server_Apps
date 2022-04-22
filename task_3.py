"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

WORDS = ['attribute', 'класс', 'функция', 'type']

for word in WORDS:
    try:
        if len(word) != len(bytes(word, 'utf-8')):
            raise UnicodeError(f'Слово "{word}" нельзя записать с помощью "b"')
        print(bytes(word, 'utf-8'))
    except UnicodeError as e:
        print(e)
