from typing import Callable

import colorama
from art import text2art

colorama.init()

type Sink = Callable[[str, ...], any]
type Generator = Callable[[str, ...], any]


def colorize(text: str, color: str = "") -> str:
    return f"{color}{text}{colorama.Style.RESET_ALL}"


def generate(*values: object, sep: str = " ", end: str = " ") -> str:
    return sep.join(map(str, values)) + end


def print_colored(
        *values: object,
        sep: str = " ",
        end: str = "\n",
        color: str = "",
        sink: Sink = print,
        generator: Generator = generate,
        **kwargs,
) -> any:
    text = generator(*values, sep=sep, end=end)
    return sink(colorize(text=text, color=color), **kwargs)


def print_art(
        *values: object,
        sep: str = " ",
        end: str = "\n",
        sink: Sink = print_colored,
        generator: Generator = generate,
        **kwargs,
):
    text = generator(*values, sep=sep, end=end)
    art = text2art(text=text)
    return sink(art, **kwargs)


__all__ = [
    "print_colored",
    "print_art",
]
