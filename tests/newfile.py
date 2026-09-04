from dbotlang.lexer import lex

code = "command ping:"

tokens = lex(code)

print(tokens)