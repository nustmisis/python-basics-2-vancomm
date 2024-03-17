"""
Комплексные числа - числа вида a + bi, где a, b - вещественные числа, i - мнимая
единица, то есть число, для которого выполняется равенство i**2 == -1.

В этом задании вам потребуется реализовать класс Complex, экземпляры которого
представляют собой комплексные числа.

Конструктор Complex принимает два параметра: real, отражающий вещественную часть
числа, и imag, отражающий множитель числа i. Оба параметра должны поддерживать
позиционные и ключевые аргументы и иметь значение по умолчанию 0:

Complex()                   # эквивалентно 0+0i 
Complex(1)                  # эквивалентно 1+0i 
Complex(1, 2)               # эквивалентно 1+2i
Complex(imag=3)             # эквивалентно 0+3i
Complex(pos=-2, imag=-5)    # эквивалентно -2+(-5i)

Экземпляры Complex должны поддерживать следующие операции:

- сложение (+)
- вычитание (-)
- умножение (*)
- деление (/)
- проверка равенства (==, !=)

Эти операции должны поддерживаться между любыми экземплярами Complex или
встроенных типов int и float.

Вывод экземпляра 

Справка:

Пусть (a + bi) и (c + di) - комплексные числа, тогда cложение и вычитание этих
чисел определяются так:

    (a + bi) + (c + di) == (a + c) + (b + d)i

    (a + bi) - (c + di) == (a - c) + (b - d)i

Так как любое вещественное число r представимо в виде комплексного с
коэффициентом 0 перед мнимой едининцей, аналогичные операции между комплексными
числами определяются так:

    (a + bi) + (r + 0i) == (a + r) + bi

    (a + bi) - (r + 0i) == (a - r) + bi

Произведение комплексных чисел:

    (a + bi) * (c + di) == ac + bci + adi + bdi**2
                        == ac + bdi**2 + bci + adi
                        == (ac - bd) + (bc + ad)i

для вещественных чисел:

    (a + bi) * (r + 0i) == r(a + bi) == ar + bri

Деление комплексных чисел:

    (a + bi) / (c + di) == ((a + bi)(c - di)) / ((c + di)(c - di))
                        == ((a + bi)(c - di)) / (c**2 + d**2)
                        == (ac + bd) / (c**2 + d**2) + ((bc - ad) / (c**2 + d**2)) * i

для вещественных чисел:

    (a + bi) / (r + 0i) == ar / r**2 + (br / r**2) * i
                        == a/r + (b/r)i


"""

from __future__ import annotations


class Complex:
    __match_args__ = ("real", "imag")

    def __init__(self, real: float = 0, imag: float = 0):
        self.real = real
        self.imag = imag

    def __add__(self, other) -> Complex:
        if isinstance(other, (int, float)):
            return Complex(self.real + other, self.imag)

        if isinstance(other, Complex):
            return Complex(self.real + other.real, self.imag + other.imag)

        return NotImplemented

    def __sub__(self, other) -> Complex:
        if isinstance(other, (int, float)):
            return Complex(self.real - other, self.imag)

        if isinstance(other, Complex):
            return Complex(self.real - other.real, self.imag - other.imag)

        return NotImplemented

    def __mul__(self, other) -> Complex:
        if isinstance(other, (int, float)):
            return Complex(self.real * other, self.imag * other)

        if isinstance(other, Complex):
            # (a + bi) * (c + di)   == ac + bci + adi + bdii
            #                       == ac + bd + bci + adi
            #                       == (ac - bd) + (bc + ad)i
            a, b = self.real, self.imag
            c, d = other.real, other.imag
            return Complex(
                real=a * c - b * d,
                imag=b * c + a * d,
            )

        return NotImplemented

    def __truediv__(self, other) -> Complex:
        if isinstance(other, (int | float)):
            return Complex(self.real / other, self.imag / other)

        if isinstance(other, Complex):
            # (a + bi) / (c + di)   == ((a + bi)(c - di)) / ((c + di)(c - di))
            #                       == ((a + bi)(c - di)) / (cc + dd)
            #                       == (ac + bd)/(cc + dd) + (bc - ad)/(cc + dd)
            a, b = self.real, self.imag
            c, d = other.real, other.imag
            return Complex(
                real=(a * c + b * d) / (c**2 + d**2),
                imag=(b * c - a * d) / (c**2 + d**2),
            )

        return NotImplemented

    def __str__(self) -> str:
        imag_str = f"{self.imag}i"
        if self.imag < 0:
            imag_str = f"({imag_str})"
        return f"{self.real}+{imag_str}"
