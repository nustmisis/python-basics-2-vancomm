import csv
import io
from collections import defaultdict
from itertools import chain, product, starmap
from pathlib import Path

import pytest

if __name__ == "__main__":
    import os.path
    import sys

    sys.path.append(os.path.curdir)

from tasks import chess

VALID_SQUARES = [(i, j) for i in range(1, 9) for j in range(1, 9)]
VALID_ARGS = list(product(("white", "black"), range(1, 9), range(1, 9)))
INVALID_RANKS = INVALID_FILES = [
    x if -20 <= x <= 20 else int(0.003 * x**3)
    for x in chain(range(-33, 1), range(9, 33))
]
INVALID_ARGS = list(
    product(("red", "yellow", "green", "white"), INVALID_RANKS, INVALID_FILES)
)
MOVES_DIR = Path("./tests/data")


def parse_square(square: str) -> ValueError | tuple[int, int]:
    if len(square) != 2:
        return ValueError()
    file_str, rank_str = square
    file = ord(file_str) - ord("A") + 1
    try:
        rank = int(rank_str)
    except ValueError as e:
        return e
    return file, rank


def encode_square(file: int, rank: int) -> str:
    letter = chr(ord("A") + file - 1)
    return f"{letter}{rank}"


def load_moves(filepath: Path) -> dict[tuple[int, int], list[tuple[int, int]]]:
    moves: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(list)
    with filepath.open() as lines:
        for row in csv.reader(lines):
            source, *destinations = row
            square = parse_square(source)
            if isinstance(square, Exception):
                continue
            dest_sq = [
                sq
                for d in destinations
                if (sq := parse_square(d)) and not isinstance(sq, Exception)
            ]
            moves[square] = dest_sq
    return moves


def test_chess_classes() -> None:
    for cls in (chess.Pawn, chess.Knight, chess.King):
        for args in VALID_ARGS:
            assert cls(*args)
        for args in INVALID_ARGS:
            with pytest.raises(ValueError):
                cls(*args)


def test_chess_move():
    pass


def test_chess_moves() -> None:
    for cls in (chess.Pawn, chess.Knight, chess.King):
        file_name = cls.__name__.lower() + ".csv"
        moves = load_moves(MOVES_DIR / file_name)
        for square in VALID_SQUARES:
            expected = sorted(moves[square])
            piece = cls("white", *square)
            actual = sorted(piece.moves())
            assert actual == expected, (
                f"{piece}: "
                f"expected moves {list(starmap(encode_square, expected))}, "
                f"received {list(starmap(encode_square, actual))}"
            )


def dump():
    for cls in (chess.Pawn, chess.Knight, chess.King):
        buffer = io.StringIO()
        for source in VALID_SQUARES:
            file, rank = source
            moves = cls("white", file, rank).moves()
            if moves:
                row = ",".join(starmap(encode_square, (source, *moves))) + "\n"
                buffer.write(row)
        filename = cls.__name__.lower() + ".csv"
        (MOVES_DIR / filename).write_text(buffer.getvalue())


def plot():
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes

    fig, axes = plt.subplots(2, 2)
    for cls, ax in zip(
        (chess.Pawn, chess.Knight, chess.King), chain.from_iterable(axes)
    ):
        assert isinstance(ax, Axes)
        ax.grid()
        ax.set_title(cls.__name__)

        for source in VALID_SQUARES:
            file, rank = source
            moves = cls("white", file, rank).moves()
            if not moves:
                ax.plot(file, rank, "ro")
            else:
                ax.plot(file, rank, "go")
                for f, r in moves:
                    ax.arrow(
                        file,
                        rank,
                        f - file,
                        r - rank,
                        head_width=0.12,
                        head_length=0.18,
                        length_includes_head=True,
                    )

    plt.show()


if __name__ == "__main__":
    plot()
