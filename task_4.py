"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

WORDS = ['разработка', 'администрирование', 'protocol', 'standard']

for word in WORDS:
    enc_word = word.encode('utf-8')
    print(f'Слово: {enc_word}, тип: {type(enc_word)}')
    dec_word = enc_word.decode('utf-8')
    print(f'Слово: {dec_word}, тип: {type(dec_word)}')
