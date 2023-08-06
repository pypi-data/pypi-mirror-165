"""
Author        : Selvaganapathy
Email         : selva.g@subcom.tech

Describe      :

Copyright (C) 2022 Subconscious Compute 'All rights reserved.'
"""

import typing as T
from collections import defaultdict

DELIMITERS: T.Final[T.List[str]] = ["|", "&&", ";", "&"]


def extract_info_from_line(line: str) -> T.Optional[T.Tuple[str, list]]:
    l = line.strip()
    if not l:
        return None
    if l[0] == r"#":
        return "comment", [line]

    assert (
        l[-1] != "\\"
    ), f"linebreak found in `{line}`, next line is also part of this line"
    fs = l.split()
    if fs[0] in [
        "export",
        "alias",
        "if",
        "else",
        "fi",
        "for",
        "while",
        "do",
        "done",
        "set",
    ]:
        return "shell", [line]
    return "executable", [fs[0]]


def join_multiline_command(lines: T.List[str]):
    """Join command split by `\\`"""
    newlines = [lines[0]]
    for line in lines[1:]:
        if not line:
            continue
        prevline = newlines[-1]
        if prevline[-1] == "\\":
            # Then the newline is part of the previous line.
            newlines[-1] = newlines[-1][:-1] + line
        else:
            newlines.append(line)
    return newlines


def extract_info(text: str) -> T.Dict[str, T.List[T.Any]]:
    """extracts the executable commands, files given in a shell script"""
    result = defaultdict(list)
    lines = join_multiline_command(text.splitlines())
    if lines[0].startswith("#!"):
        result["shebang"] = lines[0]
        lines = lines[1:]

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        info = extract_info_from_line(line)
        if info is not None:
            result[info[0]] += info[1]
    return result


if __name__ == "__main__":
    import sys
    from pathlib import Path

    text = Path(sys.argv[1]).read_text()
    print(extract_info(text))
