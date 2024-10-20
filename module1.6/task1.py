"""
Задача - ASGI / WSGI функция которая проксирует курс валют

Приложение должно отдавать курс валюты к доллару используя стороннее АПИ https://api.exchangerate-api.com/v4/latest/{currency} Например, в ответ на http://localhost:8000/USD должен возвращаться ответ вида:
"""

import requests


async def application(scope, receive, send):
    currency = scope["path"].split("/", 1)[-1]
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"text/plain"], ],
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": f'{get_currency(currency)}'.encode(),
            "more_body": False,
        }
    )


def get_currency(currency):
    url = 'https://api.exchangerate-api.com/v4/latest/' + currency
    response = requests.get(url)
    data = response.json()
    return data
