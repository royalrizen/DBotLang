from dbotlang.lexer import lex


code = """
bot MyBot

command hello:
    let message = "Hello, world!"
    return message
"""


try:
    tokens = lex(code)

    for token in tokens:
        print(token)

except Exception as e:
    print(f"Lexer error: {e}")