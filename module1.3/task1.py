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

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


def worker(url, session, urls_dict, file):
    try:
        response = session.get(url)
        status = response.status
        urls_dict[url] = status
        file.write(f'{url} {status}\n')
    except aiohttp.ClientConnectorError:
        urls_dict[url] = 0
        file.write(f'{url} {0}\n')


async def fetch_urls(urls: list[str], file_path: str):
    urls_dict = {}
    with open(file_path, 'w') as file:
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(worker(url, session, urls_dict, file)) for url in urls]
            await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(fetch_urls(urls, './results.jsonl'))
