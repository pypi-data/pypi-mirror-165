from pathlib import Path

from block_pruner.match_str import MatchStr


class BlockPruner:
    def __init__(
        self,
        start: str,
        end: str,
        needle: str,
    ) -> None:
        self.start = MatchStr(start)
        self.end = MatchStr(end)
        self.needle = MatchStr(needle)

        self._temp: list[bytes] = []
        self._save: list[bytes] = []

        self._keep_block = True
        self._inside_block = False

    def prune_file(self, input_file: Path) -> bytes:
        with open(input_file, "rb") as input_fp:
            for line in input_fp:
                self._feed_line(raw_line=line)
        return b"".join(self._save)

    def prune_bytes(self, input_data: bytes) -> bytes:
        for line in input_data.split(b"\n"):
            self._feed_line(raw_line=line + b"\n")  # noqa: WPS336
        return b"".join(self._save)

    def _feed_line(self, raw_line: bytes) -> None:
        line: str = utf8_or_empty(raw_line).strip("\n")
        if self.start == line:
            self._inside_block = True
        if self._inside_block:
            self._temp.append(raw_line)
            if self.needle == line:
                self._keep_block = False
        else:
            self._save.append(raw_line)
        if self.end == line:
            self._keep_or_disregard_block()

    def _keep_or_disregard_block(self) -> None:
        if self._keep_block:
            self._save.extend(self._temp)
        self._temp.clear()
        self._keep_block = True
        self._inside_block = False


def utf8_or_empty(line: bytes) -> str:
    try:
        return line.decode()
    except UnicodeDecodeError:
        return ""
