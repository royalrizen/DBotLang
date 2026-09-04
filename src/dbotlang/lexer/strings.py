"""
Handles string literal scanning and escape sequences in DBotLang.
"""

from .constants import ESCAPE_SEQUENCES
from .errors import LexerError
from .tokens import Token, TokenType


def lex_string(code: str, i: int, line: int, column: int):
    # Example:
    # code = '"hello\\nworld"'
    # i = 0
    # line = 1
    # column = 1
    start_line = line
    start_column = column
    i += 1
    column += 1
    value = []
    while i < len(code):
        char = code[i]
        if char == '"':
            i += 1
            column += 1

            return (
                Token(
                    type=TokenType.STRING,
                    value="".join(value),
                    line=start_line,
                    column=start_column,
                ),
                i,
                line,
                column,
            )

        if char == "\r" or char == "\n":
            raise LexerError(
                f"Unterminated string at line {start_line}, "
                f"column {start_column}"
            )

        if char == "\\":
            escape_line = line
            escape_column = column

            i += 1
            column += 1

            if i >= len(code):
                raise LexerError(
                    f"Unterminated escape sequence at line "
                    f"{escape_line}, column {escape_column}"
                )

            escaped = code[i]

            if escaped not in ESCAPE_SEQUENCES:
                raise LexerError(
                    f"Invalid escape sequence '\\{escaped}' "
                    f"at line {escape_line}, column {escape_column}"
                )

            value.append(ESCAPE_SEQUENCES[escaped])

            i += 1
            column += 1
            continue

        value.append(char)

        i += 1
        column += 1

    raise LexerError(
        f"Unterminated string at line {start_line}, "
        f"column {start_column}"
    )