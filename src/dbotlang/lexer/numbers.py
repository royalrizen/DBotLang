"""
Handles number literal scanning in DBotLang.
"""

from .errors import LexerError
from .helpers import is_digit, is_identifier_part, is_identifier_start
from .tokens import Token, TokenType


def lex_number(code: str, i: int, line: int, column: int):
    start_line = line
    start_column = column
    start_index = i

    while i < len(code) and is_digit(code[i]):
        i += 1
        column += 1

    if i < len(code) and code[i] == ".":
        if i + 1 < len(code) and is_digit(code[i + 1]):
            i += 1
            column += 1

            while i < len(code) and is_digit(code[i]):
                i += 1
                column += 1

        elif i + 1 < len(code) and code[i + 1] == ".":
            invalid_value = code[start_index:i + 2]

            raise LexerError(
                f"Invalid number '{invalid_value}' "
                f"at line {start_line}, column {start_column}"
            )

    if i < len(code) and is_identifier_start(code[i]):
        while i < len(code) and is_identifier_part(code[i]):
            i += 1
            column += 1

        invalid_value = code[start_index:i]

        raise LexerError(
            f"Invalid number '{invalid_value}' "
            f"at line {start_line}, column {start_column}"
        )

    return (
        Token(
            type=TokenType.NUMBER,
            value=code[start_index:i],
            line=start_line,
            column=start_column,
        ),
        i,
        line,
        column,
    )