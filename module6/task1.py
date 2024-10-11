"""
Задача - ASGI / WSGI функция которая проксирует курс валют

Приложение должно отдавать курс валюты к доллару используя стороннее АПИ https://api.exchangerate-api.com/v4/latest/{currency} Например, в ответ на http://localhost:8000/USD должен возвращаться ответ вида:
"""

import requests


def run_wsgi_app(app, environ):
    def start_response(status, response_headers):
        # Сохраняем статус и заголовки для последующей отправки
        global status_line, headers
        status_line = status
        headers = response_headers

    # Вызываем WSGI-приложение
    response_body = app(environ, start_response)

    # Формируем HTTP-ответ
    response = [f'HTTP/1.1 {status_line}'.encode()]
    for header in headers:
        response.append(f'{header[0]}: {header[1]}'.encode())
    response.append(b'')
    response.extend(response_body)

    return response


# Пример использования
environ = {
    'REQUEST_METHOD': 'GET',
    'PATH_INFO': '/',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '8000',
    # Другие необходимые ключи
}


def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [b'<html><body><h1>Hello, WSGI!</h1></body></html>']


response = run_wsgi_app(simple_app, environ)
print(b'\r\n'.join(response).decode())


def get_currency(currency):
    url = 'https://api.exchangerate-api.com/v4/latest/' + currency
    response = requests.get(url)
    data = response.json()
    return data
