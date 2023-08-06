import os
from pathlib import Path
import sys
from typing import Optional

from typer import Argument
from typer import Option
from typer import Typer

from block_pruner.block_pruner import BlockPruner

app = Typer()
Required = Option(...)
OutFileWithHelp = Option(None, help="Stores the output to this file, otherwise to stdout")


def save(output: bytes, out: Optional[Path] = None) -> None:
    if out is None:
        with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:
            stdout.write(output)
            stdout.flush()
    else:
        with open(out, mode="w+b") as out_fp:
            out_fp.write(output)


@app.command()
def main(
    input_files: Optional[list[Path]] = Argument(None),
    start: str = Required,
    end: str = Required,
    needle: str = Required,
    out: Optional[Path] = OutFileWithHelp,
) -> None:

    if not input_files:
        bp = BlockPruner(
            start=start,
            end=end,
            needle=needle,
        )
        output = bp.prune_bytes(sys.stdin.buffer.read())
        save(output=output, out=out)
        return

    for input_file in input_files:
        bp = BlockPruner(
            start=start,
            end=end,
            needle=needle,
        )
        output = bp.prune_file(input_file=input_file)
        save(output=output, out=out)


if __name__ == "__main__":
    app()
