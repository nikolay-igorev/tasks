"""
Задача - Асинхронный HTTP-запрос

Напишите асинхронную функцию fetch_urls, которая принимает список URL-адресов и возвращает словарь, где ключами являются URL, а значениями — статус-коды ответов. Используйте библиотеку aiohttp для выполнения HTTP-запросов.

Требования:

Ограничьте количество одновременных запросов до 5.
Обработайте возможные исключения (например, таймауты, недоступные ресурсы) и присвойте соответствующие статус-коды (например, 0 для ошибок соединения).
Сохраните все результаты в файл
"""


import asyncio
import aiohttp
import requests
from time import time

from aiohttp import ClientConnectorError

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def fetch_urls(urls: list[str], file_path: str):
    urls_dict = {}
    with open(file_path, 'w') as file:
        async with aiohttp.ClientSession() as session:
            for url in urls:
                try:
                    async with session.get(url) as response:
                        status = response.status
                        urls_dict[url] = status
                        file.write(f'{url} {status}\n')
                except ClientConnectorError:
                    urls_dict[url] = 0
                    file.write(f'{url} {0}\n')


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))
