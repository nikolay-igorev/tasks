"""
Задача - Распределенный лок

У вас есть распределенное приложение работающее на десятках серверах.
Вам необходимо написать декоратор single который гарантирует, что декорируемая функция не исполняется параллельно.
"""
import datetime
import time


def single(max_processing_time):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            while (datetime.datetime.now() - start_time) < max_processing_time:
                func(*args, **kwargs)

        return wrapper

    return decorator


@single(max_processing_time=datetime.timedelta(minutes=2))
def process_transaction():
    time.sleep(2)
