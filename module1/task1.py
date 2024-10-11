"""
Задача - Декоратор кеширования

Реализуйте декоратор, согласно следующим требованиям

Этот декоратор должен кешировать результаты вызовов функции на основе её аргументов.
Если функция вызывается с теми же аргументами, что и ранее, возвращайте результат из кеша вместо повторного выполнения функции.
Реализуйте кеширование с использованием словаря, где ключами будут аргументы функции, а значениями — результаты её выполнения.
Ограничьте размер кеша до 100 записей. При превышении этого лимита удаляйте наиболее старые записи (используйте подход FIFO).
"""
import inspect
import unittest.mock


def cache_wrapper(func, cache_dict, maxsize, f_args, f_kwargs):
    res = func(*f_args, **f_kwargs)
    if f_args in cache_dict:
        return cache_dict[f_args]
    cache_dict[f_args] = res

    if maxsize and len(cache_dict) > maxsize:
        first_key = list(cache_dict.keys())[0]
        cache_dict.pop(first_key)

    return res


def lru_cache(*args, **kwargs):
    cache_dict = {}
    maxsize = kwargs['maxsize'] if 'maxsize' in kwargs else None
    if args:
        func = args[0]

        def wrapper(*f_args, **f_kwargs):
            return cache_wrapper(func, cache_dict, maxsize, f_args, f_kwargs)

        return wrapper

    else:

        def decorator(func):
            def wrapper(*f_args, **f_kwargs):
                return cache_wrapper(func, cache_dict, maxsize, f_args, f_kwargs)

            return wrapper

        return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
