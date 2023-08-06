from typing import Literal, List
from numbers import Number as NumberClass
from datetime import datetime

List = List
Choice = Literal

class CustomType:

    def __new__(self, *overflow):

        def wrapper():
            pass

        if overflow:
            return wrapper(*overflow)
        return wrapper

class Number:

    def __new__(self, *overflow, min: NumberClass = None, max: NumberClass = None):

        def wrapper(number: NumberClass):

            if min is not None and number < min:
                raise ValueError(f'Value must be larger than {min}')
            elif max is not None and number > max:
                raise ValueError(f'Value must be no larger than {max}')
            elif min is not None and max is not None:
                if number < min:
                    raise ValueError(f'Value must be larger than {min}')
                if number > max:
                    raise ValueError(f'Value must be no larger than {max}')

            return number

        if overflow:
            return wrapper(*overflow)
        return wrapper

class DateTime:

    def __new__(self, *overflow, date_format: str = '%d/%m/%y %H:%M:%S'):
        def wrapper(date_input: str):
            return datetime.strptime(date_input, date_format)
        if overflow:
            return wrapper(*overflow)
        return wrapper

class Time(DateTime):

    def __new__(self, *overflow, date_format: str = '%H:%M:%S'):
        def wrapper(date_input: str):
            return datetime.strptime(date_input, date_format)
        if overflow:
            return wrapper(*overflow)
        return wrapper

class Date(DateTime):
    
    def __new__(self, *overflow, date_format: str = '%d/%m/%y'):
        def wrapper(date_input: str):
            return datetime.strptime(date_input, date_format)
        if overflow:
            return wrapper(*overflow)
        return wrapper

colors = {
    'red':   'ff0000',
    'green': '00ff00',
    'blue':  '0000ff',
}

class Color:

    def __init__(self, value: Literal[str, tuple, list]):

        if isinstance(value, str):
            value = value.lstrip('#').lower()
            value = colors.get(value, value)

            color_values = self._divide(value, 2)
            while len(color_values) < 3:
                color_values += [0]
            self.red, self.green, self.blue, self.alpha = color_values + [None]

        elif isinstance(value, (list, tuple)):
            value = tuple(value)

            while len(value) < 3:
                value += (0,)
            self.red, self.green, self.blue, self.alpha = value + (None,)
        
        else:
            raise TypeError("Value must be of type 'str' or 'tuple'")
        
        for color, color_value in {
            'red': self.red,
            'green': self.green,
            'blue': self.blue,
            'alpha': self.alpha
        }.items():
            if color_value and color_value > 255:
                raise ValueError(f"Value of {color} must not be larger than 255")

    def __repr__(self):
        result = '#' + self._int_to_hex(self.red) + self._int_to_hex(self.green) + self._int_to_hex(self.blue)
        if self.alpha:
            result += self._int_to_hex(self.alpha)
        return result

    def as_rgb(self):
        return self.red, self.green, self.blue

    def _int_to_hex(self, number: int):
        result = hex(number)[2:].upper()
        while len(result) < 2:
            result += '0'
        return result

    def _divide(self, target, number: int):
        return [ int(target[i:i + number], 16) for i in range(0, len(target), number)]