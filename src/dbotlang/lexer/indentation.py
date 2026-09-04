"""
Handles indentation and dedentation of DBotLang source code.
"""
from .errors import LexerError
from .tokens import Token, TokenType


def handle_line_start(
    code: str,
    i: int,
    line: int,
    column: int,
    indent_stack: list[int],
    tokens: list[Token],
    saw_code: bool,
):
    indent = 0

    while i < len(code) and code[i] in " \t":
        if code[i] == "\t":
            raise LexerError(
                f"Tabs are not allowed for indentation "
                f"at line {line}, column {indent + 1}"
            )

        indent += 1
        i += 1

    column = indent + 1

    if i >= len(code):
        return i, line, column, True, saw_code

    char = code[i]

    if char in "\r\n":
        if char == "\r" and i + 1 < len(code) and code[i + 1] == "\n":
            i += 2
        else:
            i += 1

        tokens.append(
            Token(
                type=TokenType.NEWLINE,
                value="\n",
                line=line,
                column=column,
            )
        )

        return i, line + 1, 1, True, saw_code

    if char == "#":
        while i < len(code) and code[i] not in "\r\n":
            i += 1
            column += 1

        if i >= len(code):
            return i, line, column, True, saw_code

        if code[i] == "\r" and i + 1 < len(code) and code[i + 1] == "\n":
            i += 2
        else:
            i += 1

        tokens.append(
            Token(
                type=TokenType.NEWLINE,
                value="\n",
                line=line,
                column=column,
            )
        )

        return i, line + 1, 1, True, saw_code

    if not saw_code and indent > 0:
        raise LexerError(
            f"Unexpected indentation at line {line}, column 1"
        )

    current_indent = indent_stack[-1]

    if indent > current_indent:
        indent_stack.append(indent)

        tokens.append(
            Token(
                type=TokenType.INDENT,
                value="",
                line=line,
                column=1,
            )
        )

    elif indent < current_indent:
        if indent not in indent_stack:
            raise LexerError(
                f"Invalid indentation at line {line}, column 1"
            )

        while indent_stack[-1] > indent:
            indent_stack.pop()

            tokens.append(
                Token(
                    type=TokenType.DEDENT,
                    value="",
                    line=line,
                    column=1,
                )
            )

    return i, line, column, False, saw_code