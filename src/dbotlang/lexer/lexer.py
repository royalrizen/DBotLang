"""
Sep 3, 2026 - finished writing my lexer.

"""

from dataclasses import dataclass
from enum import Enum, auto


# These are the words that have a special meaning in DBotLang. If the lexer encounters one of these words, it will create a KEYWORD token instead of treating the word as a normal identifier.
KEYWORDS = {
    "bot",
    "command",
    "on",
    "if",
    "else",
    "let",
    "return",
    "var",
}

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto() # names created by the programmer, such as: username, message, my_variable

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

    # special tokens for indentation & stuff
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()

    # marks the end of the entire source code
    EOF = auto()


SINGLE_CHAR_TOKENS = {
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "%": TokenType.PERCENT,
    "=": TokenType.EQUAL,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
}


# Some operators consist of two characters. These must be checked before single-character operators. For example, when the lexer sees "==", it needs to create one EQUAL_EQUAL token rather than two EQUAL tokens
TWO_CHAR_TOKENS = {
    "==": TokenType.EQUAL_EQUAL,
    "!=": TokenType.NOT_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    ">=": TokenType.GREATER_EQUAL,
}


# These are literal values that have special meanings. For example: true is not an ordinary identifier. It represents a boolean value.
LITERAL_TOKENS = {
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "null": TokenType.NULL,
}


# Escape sequences are special combinations used inside strings.
#
# For example:
#
#     "hello\nworld"
#
# contains "\n", which represents a newline.
# The dictionary converts the text after the backslash into the actual character it represents.
ESCAPE_SEQUENCES = {
    '"': '"',
    "\\": "\\",
    "n": "\n",
    "t": "\t",
    "r": "\r",
}

# frozen=True means that once a Token is created, its values cannot be changed.
@dataclass(frozen=True)
class Token:    
    type: TokenType # What kind of token this is.
    value: str  # The actual text/value represented by the token.
    line: int # The line where the token appeared.
    column: int   # The column where the token started.


# This is the error type used when the lexer finds invalid source code. Creating a separate error type makes it possible for other parts of DBotLang to specifically catch lexer errors.
class LexerError(Exception):
    pass


# Check whether characters are valid for starting or continuing identifiers, or for representing digits. An identifier is a name created by the programmer.
#
# Examples:
#
#     username
#     message
#     _private
#
# An identifier can start with:
# - an uppercase letter
# - a lowercase letter
# - an underscore
#
# It cannot start with a number.
def _is_identifier_start(char: str) -> bool:
    return "A" <= char <= "Z" or "a" <= char <= "z" or char == "_"


# Checks whether a character can appear after the first character of an identifier. Unlike the first character, numbers are allowed here.
# Therefore:
#
#     player1
#
# is valid, but:
#
#     1player
#
# is not a valid identifier.
def _is_identifier_part(char: str) -> bool:
    return _is_identifier_start(char) or "0" <= char <= "9"


# Checks whether a character is a decimal digit from 0 to 9.
def _is_digit(char: str) -> bool:
    return "0" <= char <= "9"


# The lexer takes raw DBotLang source code as a string
# and converts it into a list of Tokens.
#
# Example:
#
#     let x = 10
#
# becomes something similar to:
#
#     KEYWORD("let")
#     IDENTIFIER("x")
#     EQUAL("=")
#     NUMBER("10")
#
# The parser can then use these tokens to understand the structure and meaning of the program.
def lex(code: str) -> list[Token]:

    # This list will contain every token produced by the lexer.
    tokens = []

    # This stack keeps track of indentation levels. The first value is 0 because the beginning of the program is considered to have no indentation. Example:
    #
    #     bot:
    #         command:
    #
    # The stack might temporarily look like:
    #
    #     [0, 4, 8]
    #
    # This allows the lexer to generate INDENT and DEDENT tokens.
    indent_stack = [0] # keeps track of indentation levels. It starts at 0, meaning the lexer begins at the outermost level

    # Line and column numbers are used so that errors can tell the programmer exactly where something went wrong. Both start at 1 because programmers normally count lines and columns starting from 1.
    line = 1
    column = 1

    # i is the current position inside the source code string. It acts like a cursor that moves through the source code one character at a time.
    i = 0

    # This tells the lexer whether it is currently at the beginning of a line. This is important because indentation is only meaningful at the beginning of a line.
    at_line_start = True

    # Used to determine whether actual source code has appeared yet. This helps detect indentation before the first piece of code.
    saw_code = False

    # Continue processing until the cursor reaches the end of the source code.
    while i < len(code):
        char = code[i] #  the character currently being examined

        # Special processing is required at the beginning of every line because this is where indentation is determined.
        if at_line_start:
            indent = 0
            while i < len(code) and code[i] in " \t":
                # DBotLang does not allow tabs for indentation. This keeps indentation consistent and avoids different editors displaying tabs differently.
                if code[i] == "\t":
                    raise LexerError(
                        f"Tabs are not allowed for indentation at line {line}, column {indent + 1}"
                    )
                indent += 1 # Each space increases the indentation level by one.
                i += 1

            # The first non-indentation character is now at this column.
            column = indent + 1

            # If there is nothing left after the indentation, the line has reached the end of the file.
            if i >= len(code):
                break

            # Update char because i has moved while counting indentation.
            char = code[i]

            # Check whether this is a completely blank line.
            if char in "\r\n":

                # Windows-style line endings are represented by "\r\n". Treat them as one newline instead of two.
                if char == "\r" and i + 1 < len(code) and code[i + 1] == "\n":
                    i += 2
                else:
                    i += 1

                # Blank lines still produce a NEWLINE token.
                tokens.append(
                    Token(type=TokenType.NEWLINE, value="\n", line=line, column=column,))

                # Move to the next line.
                line += 1
                column = 1
                at_line_start = True
                continue

            # If the first non-space character is "#", the entire line is a comment.
            if char == "#":

                # Move forward until the end of the comment.
                while i < len(code) and code[i] not in "\r\n":
                    i += 1
                    column += 1

                # If the comment reaches the end of the file, there is no newline left to process.
                if i >= len(code):
                    break

                # Handle Windows "\r\n" or a normal newline.
                if code[i] == "\r" and i + 1 < len(code) and code[i + 1] == "\n":
                    i += 2
                else:
                    i += 1

                # The comment line produces a NEWLINE token.
                tokens.append(
                    Token(
                        type=TokenType.NEWLINE,value="\n",line=line,column=column,))

                # Move to the next line.
                line += 1
                column = 1
                at_line_start = True
                continue

            # Code cannot suddenly begin indented when no previous code has established an indentation level.
            if not saw_code and indent > 0:
                raise LexerError(
                    f"Unexpected indentation at line {line}, column 1"
                )

            # Get the indentation level of the previous/current block.
            current_indent = indent_stack[-1]

            # If the new indentation is greater than the previous level, a new block has started.
            if indent > current_indent:

                # Store the new indentation level.
                indent_stack.append(indent)

                # Tell the parser that an indented block has started.
                tokens.append(
                    Token(type=TokenType.INDENT,value="",line=line,column=1,))

            # If the indentation became smaller, one or more blocks have ended.
            elif indent < current_indent:

                # The indentation must match an indentation level that already exists in the stack. For example, going from 8 spaces to 3 spaces would be invalid if there was never a 3-space indentation.
                if indent not in indent_stack:
                    raise LexerError(
                        f"Invalid indentation at line {line}, column 1"
                    )

                # Remove indentation levels until we reach the indentation of the current line.
                while indent_stack[-1] > indent:
                    indent_stack.pop()

                    # Every removed indentation level represents a block that has ended.
                    tokens.append(
                        Token(type=TokenType.DEDENT,value="",line=line,column=1,))

            # The lexer is no longer at the beginning of this line.
            at_line_start = False

            # Update char because the cursor may have moved while processing indentation.
            char = code[i]

        # Spaces and tabs inside normal code are ignored.
        if char in " \t":
            i += 1
            column += 1
            continue

        # Handle a newline encountered while processing normal code.
        if char == "\r" or char == "\n":

            # Save the column where the newline started.
            newline_column = column

            # Again, treat "\r\n" as one newline.
            if char == "\r" and i + 1 < len(code) and code[i + 1] == "\n":
                i += 2
            else:
                i += 1

            # Add a NEWLINE token so the parser knows that one source line has ended.
            tokens.append(
                Token(
                    type=TokenType.NEWLINE,
                    value="\n",
                    line=line,
                    column=newline_column,
                )
            )

            # Move to the next line.
            line += 1
            column = 1
            at_line_start = True
            continue

        # A "#" starts a comment. Everything after "#" on the same line is ignored.
        if char == "#":
            while i < len(code) and code[i] not in "\r\n":
                i += 1
                column += 1
            continue

        # A double quote starts a string.
        if char == '"':
            start_line = line
            start_column = column
            # Skip the opening quote.
            i += 1
            column += 1
            
            # Characters belonging to the string are collected here.
            value = []

            # Continue until the closing quote is found.
            while i < len(code):
                char = code[i]
                if char == '"':

                    # Skip the closing quote.
                    i += 1
                    column += 1
                    tokens.append(
                        Token(
                            type=TokenType.STRING,
                            value="".join(value),
                            line=start_line,
                            column=start_column,
                        )
                    )
                    break

                # Strings cannot continue onto another line.
                if char == "\r" or char == "\n":
                    raise LexerError(
                        f"Unterminated string at line {start_line}, "
                        f"column {start_column}"
                    )

                # A backslash starts an escape sequence.
                if char == "\\":

                    # Remember where the escape sequence started so an error can point to the correct location.
                    escape_line = line
                    escape_column = column

                    # Skip the backslash.
                    i += 1
                    column += 1

                    # A backslash at the end of the file means that the escape sequence was never completed.
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

            # If the loop ended without finding a closing quote, the string was never properly terminated.
            else:
                raise LexerError(
                    f"Unterminated string at line {start_line}, "
                    f"column {start_column}"
                )
            continue

        if _is_identifier_start(char):
            start_line = line
            start_column = column
            start_index = i

            # Keep reading characters while they are valid parts of an identifier.
            while i < len(code) and _is_identifier_part(code[i]):
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

        if _is_digit(char):
            start_line = line
            start_column = column
            start_index = i
            while i < len(code) and _is_digit(code[i]):
                i += 1
                column += 1

            if i < len(code) and code[i] == ".":
                if i + 1 < len(code) and _is_digit(code[i + 1]):
                    i += 1
                    column += 1
                    while i < len(code) and _is_digit(code[i]):
                        i += 1
                        column += 1

                # Two consecutive dots after a number are invalid here.
                elif i + 1 < len(code) and code[i + 1] == ".":
                    invalid_value = code[start_index:i + 2]

                    raise LexerError(
                        f"Invalid number '{invalid_value}' "
                        f"at line {start_line}, column {start_column}"
                    )

            # If a number is immediately followed by an identifier character, treat the entire thing as an invalid number. For example: 123abc is rejected instead of becoming NUMBER("123") + IDENTIFIER("abc").
            if i < len(code) and _is_identifier_start(code[i]):
                while i < len(code) and _is_identifier_part(code[i]):
                    i += 1
                    column += 1

                invalid_value = code[start_index:i]

                raise LexerError(
                    f"Invalid number '{invalid_value}' "
                    f"at line {start_line}, column {start_column}"
                )

            tokens.append(
                Token(
                    type=TokenType.NUMBER,
                    value=code[start_index:i],
                    line=start_line,
                    column=start_column,
                )
            )

            saw_code = True
            continue

        # Check for two-character operators. This happens before single-character operators so that something like "==" is recognized as one token.
        if i + 1 < len(code):
            two_char = code[i:i + 2]

            # If the two-character sequence is a known operator, create the corresponding token.
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

        # If it wasn't a two-character operator, check whether it is one of the supported single-character tokens.
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

        # If none of the cases above recognized the character, then DBotLang does not currently know what to do with it.
        raise LexerError(
            f"Unexpected character '{char}' "
            f"at line {line}, column {column}"
        )

    # If the final token isn't already a NEWLINE or DEDENT, add a NEWLINE automatically. This makes the end of the source code behave consistently with a line that actually ended with a newline.
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

    # When the source code ends while still inside one or more indentation levels, close all of those blocks. For example, if the indentation stack is: [0, 4, 8] , two DEDENT tokens are needed before EOF.
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

    # Return the complete list of tokens to whoever called lex().
    return tokens
    
    """
    things i will add in future -
    single-quoted strings, exponent notation, strict float validation (123., 1.2.3), Unicode identifiers, logical operators (&&, ||), semicolon token, bracket-aware newline/indentation handling
    """