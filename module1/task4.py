"""
Задача - Атрибуты класса

Напишите метакласс, который автоматически добавляет атрибут created_at с текущей датой и временем к любому классу, который его использует.
"""

import datetime


class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.datetime
        return super().__new__(cls, name, bases, attrs)
