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

>>> print(Queen("black", 5, 8))
black queen @ E8

>>> # следующий пример выбросит исключение, игнорируйте комментарий
>>> print(Knight("red", 2, 1))  # doctest: +IGNORE_EXCEPTION_DETAIL
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
  переместиться на новое положение (например, слоны двигаются только по
  диагонали), метод должен выбрасывать исключение ValueError. В случае успеха
  метод ничего не возвращает.

>>> b = Bishop("white", 3, 1)
>>> b.move(4, 2)
>>> b.position()
(4, 2)
>>> b.move(4, 2)  # doctest: +IGNORE_EXCEPTION_DETAIL
Traceback (most recent call last):
    ...
ValueError: ...
>>> b.position()
(4, 2)
>>> b.move(8, 6)
>>> b.position()
(8, 6)

- moves(self): возвращает список всех ходов (новых позиций), доступных для
  фигуры из текущей позиции. Порядок ходов может быть любым.

>>> q = Queen("white", 4, 4)
>>> sorted(q.moves())
[(1, 3), (1, 3), (2, 2), (2, 2), (3, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 5), (4, 6), (4, 6), (4, 7), (4, 7), (4, 8), (4, 8), (5, 1), (5, 1), (6, 2), (6, 2), (7, 3), (7, 3), (8, 4), (8, 4)]
"""

import itertools
from abc import abstractmethod


class Piece:
    def __init__(self, color: str, file: int, rank: int):
        if color not in ("white", "black"):
            raise ValueError(f"color {color} not allowed")

        if not (1 <= file <= 8):
            raise ValueError(f"file {file} not allowed")

        if not (1 <= rank <= 8):
            raise ValueError(f"rank {rank} not allowed")

        self.color = color
        self.file = file
        self.rank = rank

    def position(self) -> tuple[int, int]:
        return (self.file, self.rank)

    @staticmethod
    def validate_square(file: int, rank: int):
        assert 1 <= file <= 8
        assert 1 <= rank <= 8

    def move(self, file: int, rank: int):
        self.validate_square(file, rank)
        try:
            self.validate_move(file, rank)
        except AssertionError as e:
            raise ValueError(e)
        self.file = file
        self.rank = rank

    def __str__(self) -> str:
        file = chr(ord("A") + self.file - 1)
        return f"{self.color} {type(self).__name__.lower()} @ {file}{self.rank}"

    @abstractmethod
    def validate_move(self, file: int, rank: int): ...

    @abstractmethod
    def moves(self) -> list[tuple[int, int]]: ...


class Pawn(Piece):
    def validate_move(self, file: int, rank: int):
        assert (
            abs(self.file - file) <= 1
        ), "pawn can only move straight or one square left or right"
        assert rank - self.rank == 1, "pawn can only move 1 square forward"

    def moves(self):
        f, r = self.file, self.rank
        vectors = [(-1, 1), (0, 1), (1, 1)]
        moves = []
        for df, dr in vectors:
            move = f + df, r + dr
            try:
                self.validate_move(*move)
                self.validate_square(*move)
            except Exception:
                pass
            else:
                moves.append(move)
        return moves


class Knight(Piece):
    def validate_move(self, file: int, rank: int):
        df = abs(self.file - file)
        dr = abs(self.rank - rank)
        l, g = (df, dr) if df < dr else (dr, df)
        assert (l, g) == (1, 2), "knight only moves (1,2) or (2,1)"

    def moves(self) -> list[tuple[int, int]]:
        f, r = self.position()
        moves = []
        vectors = [
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
        ]
        for df, dr in vectors:
            move = f + df, r + dr
            try:
                self.validate_move(*move)
                self.validate_square(*move)
            except Exception:
                pass
            else:
                moves.append(move)
        return moves


class King(Piece):
    def validate_move(self, file: int, rank: int):
        f, r = self.position()
        df, dr = abs(file - f), abs(rank - r)
        assert (df or dr) and df <= 1 and dr <= 1

    def moves(self) -> list[tuple[int, int]]:
        f, r = self.position()
        moves = []
        vectors: list[tuple[int, int]] = [
            (0, 1),
            (1, 0),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
        ]
        for df, dr in vectors:
            move = f + df, r + dr
            try:
                self.validate_move(*move)
                self.validate_square(*move)
            except Exception:
                pass
            else:
                moves.append(move)
        return moves


# class Bishop(Piece):
#     def validate_move(self, file: int, rank: int):
#         df = abs(self.file - file)
#         dr = abs(self.rank - rank)
#         assert df == dr and df >= 1


# class Rook(Piece):
#     pass


# class Queen(Piece):
#     def moves(self):
#         moves: list[tuple[int, int]] = []
#         vectors: list[tuple[int, int]] = [
#             (0, 1),
#             (1, 0),
#             (-1, 0),
#             (0, -1),
#             (1, 1),
#             (-1, -1),
#             (-1, 1),
#             (1, -1),
#         ]
#         f, r = self.file, self.rank
#         for df, dr in vectors:
#             f, r = f + df, r + dr
#             while True:
#                 try:
#                     self.validate_square(f, r)
#                 except Exception:
#                     break
#                 else:
#                     moves.append((f, r))
#                     f, r = f + df, r + dr
#         return moves
