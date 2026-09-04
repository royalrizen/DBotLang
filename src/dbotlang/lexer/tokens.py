"""
Defines the token types and token structure used by the DBotLang lexer.
"""

from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()

    STRING = auto()
    NUMBER = auto()

    TRUE = auto()
    FALSE = auto()
    NULL = auto()

    COLON = auto()
    COMMA = auto()
    DOT = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()

    EQUAL = auto()
    EQUAL_EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()

    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()

    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: str
    line: int
    column: int