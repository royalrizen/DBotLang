from dbotlang.lexer import lex, LexerError, TokenType


tests = [
    # Keywords
    "bot command on if else let return var",

    # Literals
    "true false null",

    # Identifiers
    "hello _hello hello123 hello_world",

    # Numbers
    "0 1 123 3.14 0.5 999.999",

    # Operators
    "+ - * / % = == != < > <= >=",

    # Punctuation
    ": , . ( ) [ ] { }",

    # Strings
    '"hello"',
    '"hello world"',
    '""',
    r'"hello\nworld"',
    r'"hello\tworld"',
    r'"hello\rworld"',
    r'"say \"hello\""',
    r'"backslash \\"',

    # Comments
    '# this is a comment\nbot "Test"',

    # Indentation
    'command ping:\n    reply "Pong!"',

    # Nested indentation
    'command ping:\n    if true:\n        reply "yes"\n    reply "done"',

    # Multiline string
    '"hello\nworld"',
]


invalid_indentation_tests = [
    # Indent does not match expected level
    'command ping:\n   reply "wrong"',

    # Indent is too deep
    'command ping:\n        reply "wrong"',

    # Unexpected dedent
    'command ping:\n    reply "ok"\n  reply "wrong"',

    # Dedent to an indentation level that never existed
    'command ping:\n    if true:\n        reply "yes"\n      reply "wrong"',

    # Inconsistent indentation
    'command ping:\n    reply "one"\n     reply "two"',

    # Multiple inconsistent levels
    'command ping:\n    if true:\n        reply "yes"\n   reply "wrong"',

    # Indentation without a previous block
    '    reply "wrong"',
]


for number, code in enumerate(tests, 1):
    print("=" * 60)
    print(f"TEST {number}")
    print("=" * 60)
    print(repr(code))

    try:
        tokens = lex(code)

        for token in tokens:
            print(token)

        if not tokens:
            raise AssertionError("Lexer returned no tokens")

        if tokens[-1].type != TokenType.EOF:
            raise AssertionError(
                "Lexer did not produce an EOF token"
            )

        print("PASS")

    except LexerError as error:
        print("LEXER ERROR:")
        print(error)

    except AssertionError as error:
        print("TEST FAILED:")
        print(error)


print()
print("=" * 60)
print("INVALID INDENTATION TESTS")
print("=" * 60)


for number, code in enumerate(invalid_indentation_tests, 1):
    print()
    print(f"INVALID TEST {number}")
    print("=" * 60)
    print(repr(code))

    try:
        tokens = lex(code)

        print("FAILED: Lexer accepted invalid indentation")

        for token in tokens:
            print(token)

    except LexerError as error:
        print("PASS: LexerError")
        print(error)