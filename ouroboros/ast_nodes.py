#!/usr/bin/env python3

from typing import List, Optional, Any
from .lexer import TokenType

class ASTNode:
    pass

class Expression(ASTNode):
    pass

class Statement(ASTNode):
    pass

class BinaryOp(Expression):
    def __init__(self, left: Expression, op: TokenType, right: Expression):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(Expression):
    def __init__(self, op: TokenType, operand: Expression):
        self.op = op
        self.operand = operand

class Literal(Expression):
    def __init__(self, value: Any):
        self.value = value

class Identifier(Expression):
    def __init__(self, name: str):
        self.name = name

class FunctionCall(Expression):
    def __init__(self, name: str, args: List[Expression]):
        self.name = name
        self.args = args

class ArrayAccess(Expression):
    def __init__(self, array: Expression, index: Expression):
        self.array = array
        self.index = index

class PostfixOp(Expression):
    def __init__(self, operand: Expression, op: TokenType):
        self.operand = operand
        self.op = op

class Assignment(Statement):
    def __init__(self, target: Expression, value: Expression, op: TokenType = TokenType.ASSIGN):
        self.target = target
        self.value = value
        self.op = op

class ArrayInitializer(Expression):
    def __init__(self, elements: List[Expression]):
        self.elements = elements

class Declaration(Statement):
    def __init__(self, var_type: str, name: str, value: Optional[Expression] = None, 
                 size: Optional[Expression] = None, initializer: Optional[ArrayInitializer] = None,
                 dimensions: Optional[List[Expression]] = None):
        self.var_type = var_type
        self.name = name
        self.value = value
        self.size = size
        self.initializer = initializer
        self.dimensions = dimensions or []

class IfStatement(Statement):
    def __init__(self, condition: Expression, then_stmt: Statement, else_stmt: Optional[Statement] = None):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

class ForStatement(Statement):
    def __init__(self, init: Optional[Statement], condition: Optional[Expression], 
                 update: Optional[Expression], body: Statement):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class ReturnStatement(Statement):
    def __init__(self, value: Optional[Expression] = None):
        self.value = value

class BreakStatement(Statement):
    pass

class ContinueStatement(Statement):
    pass

class Block(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression):
        self.expression = expression

class Parameter:
    def __init__(self, var_type: str, name: str):
        self.var_type = var_type
        self.name = name

class FunctionDef(Statement):
    def __init__(self, return_type: str, name: str, params: List[Parameter], body: Block):
        self.return_type = return_type
        self.name = name
        self.params = params
        self.body = body

class PreprocessorDirective(Statement):
    def __init__(self, directive: str, value: str = ""):
        self.directive = directive
        self.value = value

class Program(ASTNode):
    def __init__(self, statements: List[Statement]):
        self.statements = statements