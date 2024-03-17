# Задание "Комплексные числа"

## Подсказки

В этом задании вам потребуется по-разному обрабатывать аргументы методов в зависимости от их типа. Для этого пользуйтесь встроенной функцией [`isinstance()`](https://docs.python.org/3/library/functions.html#isinstance). Например, `isinstance(x, (int, float))` вернет `True` только если `x` имеет тип `int` или `float`.

Если во время тестов вы получаете ошибку вида `TypeError: unsupported operand type(s) for *: 'int' and 'Complex'`, убедитесь, что вы корректно реализовали соответствующий метод класса `Complex` (в этом случае `__rmul__`). 

## Теоретический минимум

Пусть $x = a + bi$ и $y = c + di$ &mdash; комплексные числа, $r$ &mdash; вещественное число, тогда операции над $x$, $y$ и $r$ представимы так:

#### Сложение

$$
\begin{align*}
x + y &= (a + bi) + (c + di) \\
&= (a + c) + (b + d)i \\
\end{align*}
$$

$$
\begin{align*}
x + r &= (a + bi) + (r + 0i) \\
&= (a + r) + bi \\
\end{align*}
$$

#### Вычитание

$$
\begin{align*}
x - y &= (a + bi) - (c + di) 
\\ &= (a - c) + (b - d)i \\
\end{align*}
$$

$$
\begin{align*}
x - r &= (a + bi) - (r + 0i) 
\\ &= (a - r) + bi
\end{align*}
$$

#### Произведение

$$
\begin{align*}
x \cdot y &=  (a + bi) \cdot (c + di) \\
&= ac + bci + adi + bdi^2 \\
&= (ac - bd) + (bc + ad)i
\end{align*}
$$

$$
x \cdot r = (a + bi) \cdot r = ra + rbi
$$

#### Деление

$$
\begin{align*}
\frac{x}{y} &= \frac{a + bi}{c + di} \\   
&= \frac{(a + bi)(c - di)}{(c + di)(c - di)} \\
&= \frac{(a + bi)(c - di)}{c^2 + d^2} \\
&= \frac{ac + bd}{c^2 + d^2} + \frac{bc - ad}{c^2 + d^2}i
\end{align*}
$$

$$
\frac{x}{r} = \frac{a + bi}{r} = \frac{a}{r} + \frac{b}{r}i
$$