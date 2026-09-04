from dataclasses import dataclass
from typing import Optional
from lexer import TokenType


class Node:
    pass
class Statement(Node):
    pass
class Expression(Node):
    pass


@dataclass
class Program(Node):
    statements: list[Statement]


@dataclass
class Bot(Statement):
    name: str
    body: list[Statement]


@dataclass
class Command(Statement):
    name: str
    parameters: list[str]
    body: list[Statement]


@dataclass
class Event(Statement):
    name: str
    body: list[Statement]


@dataclass
class If(Statement):
    condition: Expression
    body: list[Statement]
    else_body: Optional[list[Statement]] = None


@dataclass
class VariableDeclaration(Statement):
    name: str
    value: Expression
    mutable: bool


@dataclass
class Return(Statement):
    value: Optional[Expression] = None


@dataclass
class ExpressionStatement(Statement):
    expression: Expression


@dataclass
class Assignment(Statement):
    target: Expression
    value: Expression


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class StringLiteral(Expression):
    value: str


@dataclass
class NumberLiteral(Expression):
    value: str


@dataclass
class BooleanLiteral(Expression):
    value: bool


@dataclass
class NullLiteral(Expression):
    pass


@dataclass
class ArrayLiteral(Expression):
    elements: list[Expression]


@dataclass
class UnaryExpression(Expression):
    operator: TokenType
    operand: Expression


@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: TokenType
    right: Expression


@dataclass
class CallExpression(Expression):
    function: Expression
    arguments: list[Expression]


@dataclass
class MemberExpression(Expression):
    object: Expression
    name: str