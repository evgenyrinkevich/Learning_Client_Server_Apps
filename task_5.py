"""
Задание 5.

Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet, иначе задание не засчитается!!!
"""
import asyncio
import subprocess
from chardet import detect

URLS = ['yandex.ru', 'youtube.com']


async def async_ping(url):
    subproc_ping = subprocess.Popen(['ping', url], stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        result = detect(line)
        print(f"{url} - {line.decode(result['encoding'])}")
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(*[async_ping(url) for url in URLS])


asyncio.run(main())
