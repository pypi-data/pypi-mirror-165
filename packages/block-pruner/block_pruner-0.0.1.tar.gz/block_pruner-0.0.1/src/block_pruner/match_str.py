import re


class MatchStr:
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def __eq__(self, line: object) -> bool:
        if not isinstance(line, str):
            return NotImplemented
        return re.search(pattern=self.pattern, string=line) is not None

    def __str__(self) -> str:
        return self.pattern
