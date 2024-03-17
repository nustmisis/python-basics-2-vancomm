from __future__ import annotations

import itertools
import math
import operator
import random
import re
from typing import TYPE_CHECKING, Any, Callable

import pytest

if TYPE_CHECKING:

    class Complex:
        real: int | float
        imag: int | float

        def __init__(self, real: int | float = 0, imag: int | float = 0): ...
        def __add__(self, other) -> Complex: ...
        def __sub__(self, other) -> Complex: ...
        def __mul__(self, other) -> Complex: ...
        def __truediv__(self, other) -> Complex: ...

else:
    from tasks.complex import Complex


def rand_int() -> int:
    return random.randint(-1000, 1000)


def rand_float() -> float:
    return rand_int() + round(random.random(), 2)


def rand_real() -> float | int:
    return random.choice((rand_int, rand_float))()


def rand_complex() -> complex:
    a = random.choice((rand_int, rand_float))()
    b = random.choice((rand_int, rand_float))()
    return complex(a, b)


def rand_op() -> Callable[[Any, Any], Any]:
    return random.choice(
        (
            operator.__add__,
            operator.__sub__,
            operator.__mul__,
            operator.__truediv__,
        )
    )


def num_to_complex(num: int | float | complex) -> Complex:
    if isinstance(num, (int, float)):
        return Complex(num)
    return Complex(real=num.real, imag=num.imag)


def run_case(
    a: int | float | complex, b: int | float | complex, op: Callable[[Any, Any], Any]
):
    if b == 0 and op is operator.truediv:
        with pytest.raises(ZeroDivisionError):
            op(num_to_complex(a), b)
            return

    _as = (num_to_complex(a),) if isinstance(a, complex) else (a, num_to_complex(a))
    _bs = (num_to_complex(b),) if isinstance(b, complex) else (b, num_to_complex(b))

    expected = num_to_complex(op(a, b))

    for _a, _b in itertools.product(_as, _bs):
        actual = op(_a, _b)
        assert isinstance(actual, Complex)
        if op is operator.truediv:  # division may be innacurate due to float
            a1, a2 = actual.real, expected.real
            b1, b2 = actual.imag, expected.imag
            assert math.isclose(a1, a2) and math.isclose(b1, b2)
        else:
            assert actual == expected


def test_complex_operations():
    for _ in range(1000):
        c1, c2 = rand_complex(), rand_complex()
        r = rand_real()
        op = rand_op()
        for a, b in itertools.permutations((c1, c2, r), 2):
            run_case(a, b, op)


def test_complex_str():
    re_parens = re.compile(r"[()]")
    for _ in range(1000):
        a, b = rand_real(), rand_real()
        expected = re_parens.sub("", str(complex(a, b)).replace("j", "i"))
        actual = str(Complex(a, b))
        assert actual == expected
