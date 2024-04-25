"""
Реализуйте класс Complex, экземпляры которого представляют собой комплексные
числа.

Обратите внимание! Python предоставляет встроенный интерфейс для работы с
комплексными числами: тип complex (со строчной буквы). В рамках этого задания
считайте, что этого типа не существует.

Конструктор Complex должен принимать два параметра: 

- real типа int или float, отражающий вещественную часть числа;
- imag типа int или float, отражающий множитель числа i. 

Оба параметра должны поддерживать позиционные и ключевые аргументы и иметь
значение по умолчанию 0.

Примеры использования конструктора Complex:

>>> Complex()
0+0i

>>> Complex(1)
1+0i

>>> Complex(-2, 0.5)
-2+0.5i

>>> Complex(imag=-1)
0-1i

>>> Complex(real=4, imag=2)
4+2i

Экземпляры Complex должны иметь поля real и imag, содержащие соответствующие им
значения вещественной части числа и коэффициента числа i

>>> Complex(10, 20).real
10

>>> Complex(imag=-1.0).imag
-1.0

Строковое представление экземпляров Complex должно иметь вид a+bi, при
отрицательных b знак "+" опускается. Примеры:

>>> Complex()
0+0i

>>> Complex(1)
1+0i

>>> Complex(1, 2)
1+2i

>>> Complex(-1, -2)
-1-2i

Экземпляры Complex должны поддерживать следующие операции:

- сложение (+);
- вычитание (-);
- умножение (*);
- деление (/);
- проверка равенства (==, !=).

Результатом всех операций (кроме == и !=) должны быть новые экземпляры Complex,
старые экземпляры при этом не должны изменяться.

Эти операции должны поддерживаться между любыми экземплярами Complex или
встроенных типов int и float вне зависимости от порядка аргументов. Примеры
допустимых операций:

>>> 1 + Complex(1, 2)
2+2i

>>> Complex(3, 4) - 0.5
2.5+4i

>>> 3 / Complex(-2, 1)
-1.2-0.6i

>>> Complex(5, 1) * Complex(0.4, 0.3)
1.7+1.9i

>>> 7.7 == Complex(real=7.7)
True

>>> -1 == Complex(real=-1, imag=4)
False
"""

from __future__ import annotations  # игнорируйте эту строку


class Complex:
    def __add__(self):
        return NotImplemented
