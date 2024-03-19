"""
Реализуйте класс Piece, отражающий фигуру шахматной доски, а также его
классы-наследники: Pawn (пешка), Knight (конь) и King (король).

Наследники Piece должны иметь общий конструктор, принимающий цвет фигуры и ее
текущее положение на доске. Цвет фигуры может быть либо строкой "white", либо
строкой "black" (в нижнем регистре, без пробелов). Начальное положение задается
двумя параметрами: номер столбца и номер строки в виде целых чисел от 1 до 8
включительно. Конструктор должен проверять, что аргументы соответствуют этим
требованиям, в противном случае должно возникать исключение ValueError.
Гарантируется, что типы аргументов будут соответствовать описанным выше.

При переводе в строку экземпляры этих классов должны выводить свой цвет,
название класса в нижнем регистре и текущее положение, где номер столбца выражен
соответствующей заглавной латинской буквой. 

>>> print(Pawn("white", 1, 2))
white pawn @ A2

>>> print(King("black", 5, 8))
black king @ E8

>>> print(Knight("red", 2, 1))              # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
ValueError: ...

Все фигуры должны поддерживать следующие методы:

- position(self): возвращает пару (tuple), соответствующую текущим значениям
  номера столбца и номера строки.

>>> King("white", 6, 1).position()
(6, 1)

- move(self, file, rank): изменяет текущее положение фигуры, "перемещая" ее на
  новый столбец file и новую строку rank. В случае, фигура не может
  переместиться на новое положение (например, король двигается только на одну
  клетку в любом направлении), метод должен выбрасывать исключение ValueError. В
  случае успеха метод ничего не возвращает.

>>> p = Pawn("white", 1, 2)
>>> p.move(1, 4)
>>> p.position()
(1, 4)
>>> p.move(1, 3)                            # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
ValueError: ...
>>> p.position()
(1, 4)
>>> p.move(1, 5)
>>> p.position()
(1, 5)

- moves(self): возвращает список всех ходов (новых позиций), доступных для
  фигуры из текущей позиции. Порядок ходов может быть любым.

>>> n = Knight("white", 4, 4)
>>> n.moves()
[(5, 6), (5, 2), (3, 6), (3, 2), (6, 5), (6, 3), (2, 5), (2, 3)]




"""

import itertools
from typing import override


class ChessEntity:
    @staticmethod
    def validate_square(file: int, rank: int) -> ValueError | None:
        if not (1 <= file <= 8) or not (1 <= rank <= 8):
            return ValueError(f"square {file}:{rank} is invalid")

    @staticmethod
    def format_square(file: int, rank: int) -> str:
        letter = chr(ord("A") + file - 1)
        return f"{letter}{rank}"


class Piece(ChessEntity):
    def __init__(self, color: str, file: int, rank: int) -> None:
        if color not in ("white", "black"):
            raise ValueError(f"color {color} not allowed")

        if error := self.validate_square(file, rank):
            raise error

        self.color = color
        self.file = file
        self.rank = rank

    def position(self) -> tuple[int, int]:
        return (self.file, self.rank)

    def move(self, file: int, rank: int) -> None:
        if error := self.validate_square(file, rank):
            raise error

        if error := self.validate_move(file, rank):
            raise error

        self.file = file
        self.rank = rank

    def __str__(self) -> str:
        klass = type(self).__name__.lower()
        square = self.format_square(self.file, self.rank)
        return f"{self.color} {klass} @ {square}"

    def validate_move(self, file: int, rank: int) -> None | Exception: ...

    def moves(self) -> list[tuple[int, int]]: ...


class Pawn(Piece):
    @override
    def validate_move(self, file: int, rank: int) -> ValueError | None:
        df, dr = file - self.file, rank - self.rank
        if dr <= 0:
            return ValueError("pawn can only move forward")
        if abs(df) > 1:
            return ValueError("pawn can only move in the same or adjacent file")
        if dr > 2:
            return ValueError("pawn can only move forward 1 or 2 ranks")
        if dr == 2 and self.rank != 2:
            return ValueError("pawn can only move 2 ranks from rank 2")

    @override
    def moves(self) -> list[tuple[int, int]]:
        vectors = ((-1, 1), (0, 1), (1, 1))
        moves = []
        for df, dr in vectors:
            fp, rp = self.file + df, self.rank + dr
            if error := self.validate_square(fp, rp):
                continue
            moves.append((fp, rp))
        if self.rank == 2:
            moves.append((self.file, self.rank + 2))
        return moves


class Knight(Piece):
    @override
    def validate_move(self, file: int, rank: int) -> ValueError | None:
        df, dr = abs(file - self.file), abs(rank - self.rank)
        vector = (df, dr) if df > dr else (dr, df)
        if vector != (2, 1):
            return ValueError("knight only moves (1,2) or (2,1)")

    @override
    def moves(self) -> list[tuple[int, int]]:
        moves = []
        vectors = itertools.chain(
            itertools.product((1, -1), (2, -2)),
            itertools.product((2, -2), (1, -1)),
        )
        for df, dr in vectors:
            fp, rp = self.file + df, self.rank + dr
            if error := self.validate_square(fp, rp):
                continue
            moves.append((fp, rp))
        return moves


class King(Piece):
    @override
    def validate_move(self, file: int, rank: int):
        df, dr = abs(file - self.file), abs(rank - self.rank)
        if not (0 <= df <= 1 and 0 <= dr <= 1 and df + dr):
            return ValueError("king can only move 1 square in each direction")

    @override
    def moves(self) -> list[tuple[int, int]]:
        moves = []
        vectors = ((i, j) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j)
        for df, dr in vectors:
            fp, rp = self.file + df, self.rank + dr
            if error := self.validate_square(fp, rp):
                continue
            moves.append((fp, rp))
        return moves
