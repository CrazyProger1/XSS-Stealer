import argparse
import os
import sys
from pathlib import Path
from typing import Sequence, Iterable

import pyperclip
import colorama
from jinja2 import Environment, FileSystemLoader, meta

from stealer.__version__ import (
    __title__,
    __description__
)
from stealer.constants import (
    DEFAULT_TEMPLATE_FILE,
    DEFAULT_TEMPLATES_DIRECTORY,
)
from stealer.utils import io


def parse_args(args: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog=__title__,
        description=__description__,
    )

    parser.add_argument(
        "-d", "--directory",
        help="templates directory",
        default=DEFAULT_TEMPLATES_DIRECTORY,
    )

    parser.add_argument(
        "template",
        help="template filename",
        default=DEFAULT_TEMPLATE_FILE,
        nargs="?",
    )
    return parser.parse_args(args=args)


def get_keys(env: Environment, content: str) -> Iterable[str]:
    parsed_content = env.parse(content)
    return meta.find_undeclared_variables(parsed_content)


def print_positive(*values: str):
    io.print_colored(
        *values,
        color=colorama.Fore.LIGHTGREEN_EX,
    )


def main(args: Sequence[str] = None):
    if args is None:
        args = sys.argv[1:]

    io.print_art(
        __title__,
        color=colorama.Fore.RED,
    )

    namespace = parse_args(args=args)

    path = Path(namespace.directory).joinpath(namespace.template)

    if not path.exists():
        raise RuntimeError(f"Template does not exists: {path}")

    env = Environment(loader=FileSystemLoader(namespace.directory))
    template = env.get_template(namespace.template)

    print_positive(f"[+] Template Loaded: {template}")

    with open(path, "r") as file:
        content = file.read()

    keys = get_keys(
        env=env,
        content=content,
    )
    print_positive(f"[+] Found Keys: {", ".join(keys)}\n")

    values = {
        "cwd": os.getcwd(),
        "args": namespace,
    }

    for key in keys:
        if key not in values:
            print(f"[{key}]")
            values[key] = input(">>>")
            print()

    print_positive(f"[+] Values: {' '.join((
        f'\n{key} = {value}'
        for key, value in values.items()))
    }")

    print_positive("\n[+] Generating...")

    payload = template.render(**values)

    print_positive("[+] Payload:")

    print("\n", payload, "\n", sep="")

    pyperclip.copy(payload)

    print_positive("\n[+] Copied to clipboard")

    os.system("pause")


if __name__ == '__main__':
    main()
