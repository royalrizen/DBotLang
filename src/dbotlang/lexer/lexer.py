"""
Contains the main lexer for converting DBotLang source code into tokens.
"""

from .constants import (
    KEYWORDS,
    LITERAL_TOKENS,
    SINGLE_CHAR_TOKENS,
    TWO_CHAR_TOKENS,
)
from .errors import LexerError
from .helpers import is_digit, is_identifier_part, is_identifier_start
from .indentation import handle_line_start
from .numbers import lex_number
from .strings import lex_string
from .tokens import Token, TokenType


def lex(code: str) -> list[Token]:
    tokens = []
    indent_stack = [0]

    line = 1
    column = 1
    i = 0

    at_line_start = True
    saw_code = False

    while i < len(code):
        char = code[i]

        if at_line_start:
            i, line, column, at_line_start, saw_code = handle_line_start(
                code,
                i,
                line,
                column,
                indent_stack,
                tokens,
                saw_code,
            )

            if i >= len(code):
                break

            if at_line_start:
                continue

            char = code[i]

        if char in " \t":
            i += 1
            column += 1
            continue

        if char == "\r" or char == "\n":
            newline_column = column

            if char == "\r" and i + 1 < len(code) and code[i + 1] == "\n":
                i += 2
            else:
                i += 1

            tokens.append(
                Token(
                    type=TokenType.NEWLINE,
                    value="\n",
                    line=line,
                    column=newline_column,
                )
            )

            line += 1
            column = 1
            at_line_start = True
            continue

        if char == "#":
            while i < len(code) and code[i] not in "\r\n":
                i += 1
                column += 1

            continue

        if char == '"':
            token, i, line, column = lex_string(
                code,
                i,
                line,
                column,
            )

            tokens.append(token)
            saw_code = True
            continue

        if is_identifier_start(char):
            start_line = line
            start_column = column
            start_index = i

            while i < len(code) and is_identifier_part(code[i]):
                i += 1
                column += 1

            word = code[start_index:i]

            if word in LITERAL_TOKENS:
                token_type = LITERAL_TOKENS[word]
            elif word in KEYWORDS:
                token_type = TokenType.KEYWORD
            else:
                token_type = TokenType.IDENTIFIER

            tokens.append(
                Token(
                    type=token_type,
                    value=word,
                    line=start_line,
                    column=start_column,
                )
            )

            saw_code = True
            continue

        if is_digit(char):
            token, i, line, column = lex_number(
                code,
                i,
                line,
                column,
            )

            tokens.append(token)
            saw_code = True
            continue

        if i + 1 < len(code):
            two_char = code[i:i + 2]

            if two_char in TWO_CHAR_TOKENS:
                tokens.append(
                    Token(
                        type=TWO_CHAR_TOKENS[two_char],
                        value=two_char,
                        line=line,
                        column=column,
                    )
                )

                i += 2
                column += 2
                saw_code = True
                continue

        if char in SINGLE_CHAR_TOKENS:
            tokens.append(
                Token(
                    type=SINGLE_CHAR_TOKENS[char],
                    value=char,
                    line=line,
                    column=column,
                )
            )

            i += 1
            column += 1
            saw_code = True
            continue

        raise LexerError(
            f"Unexpected character '{char}' "
            f"at line {line}, column {column}"
        )

    if tokens and tokens[-1].type not in {
        TokenType.NEWLINE,
        TokenType.DEDENT,
    }:
        tokens.append(
            Token(
                type=TokenType.NEWLINE,
                value="\n",
                line=line,
                column=column,
            )
        )

    while len(indent_stack) > 1:
        indent_stack.pop()

        tokens.append(
            Token(
                type=TokenType.DEDENT,
                value="",
                line=line,
                column=1,
            )
        )

    tokens.append(
        Token(
            type=TokenType.EOF,
            value="",
            line=line,
            column=column,
        )
    )

    return tokens