"""
Provides helper functions used by the DBotLang lexer.
"""

def is_identifier_start(char: str) -> bool:
    return "A" <= char <= "Z" or "a" <= char <= "z" or char == "_"


def is_identifier_part(char: str) -> bool:
    return is_identifier_start(char) or "0" <= char <= "9"


def is_digit(char: str) -> bool:
    return "0" <= char <= "9"