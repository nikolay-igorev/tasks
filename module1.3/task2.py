"""
Задача - Параллельная обработка числовых данных

азработайте программу, которая выполняет следующие шаги:

Сбор данных:

Создайте функцию generate_data(n), которая генерирует список из n случайных целых чисел в диапазоне от 1 до 1000. Например, generate_data(1000000) должна вернуть список из 1 миллиона случайных чисел.

Обработка данных:

Напишите функцию process_number(number), которая выполняет вычисления над числом. Например, вычисляет факториал числа или проверяет, является ли число простым. Обратите внимание, что обработка должна быть ресурсоёмкой, чтобы продемонстрировать преимущества мультипроцессинга.

Параллельная обработка:

Используйте модули multiprocessing и concurrent.futures для параллельной обработки списка чисел.

Реализуйте три варианта:

Вариант А: Ипользование пула потоков с concurrent.futures.

Вариант Б: Использование multiprocessing.Pool с пулом процессов, равным количеству CPU.

Вариант В: Создание отдельных процессов с использованием multiprocessing.Process и очередей (multiprocessing.Queue) для передачи данных.

Сравнение производительности:

Измерьте время выполнения для всех вариантов и сравните их с однопоточным (однопроцессным) вариантом. Представьте результаты в виде таблицы или графика.

Сохранение результатов:

Сохраните обработанные данные в файл (например, в формате JSON или CSV).
"""

import multiprocessing
import random
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process

big_number = 1000000

def generate_data(n):
    for i in range(n):
        yield random.randint(0, n)


def process_number(number):
    if number == 1:
        return 1
    else:
        return number * process_number(number - 1)


def timemometr(func):
    def wrapper(*args):
        start_time = time.time()
        res = func(*args)
        end_time = time.time()
        print(f'{func.__name__}: {end_time - start_time} сек.')
        return res

    return wrapper


@timemometr
def a():
    with ThreadPoolExecutor(max_workers=2) as executor:
        for n in generate_data(big_number):
            executor.submit(process_number, n)


@timemometr
def b():
    with multiprocessing.Pool(processes=2) as pool:
        for n in generate_data(big_number):
            pool.apply_async(process_number, (n,))


@timemometr
def c():
    pass


@timemometr
def d():
    for n in generate_data(big_number):
        process_number(n)


if __name__ == '__main__':
    a()
    b()
    c()
    d()
