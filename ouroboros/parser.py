#!/usr/bin/env python3

from typing import List, Optional, Tuple
from .lexer import Lexer, Token, TokenType
from .ast_nodes import *
from .errors import ParserError

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self, message: str):
        line = self.current_token.line if self.current_token else 0
        raise ParserError(message, line)
    
    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type}")
    
    def skip_newlines(self):
        while self.current_token.type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)
    
    def parse(self) -> Program:
        return self.program()
    
    def program(self) -> Program:
        statements = []
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
                continue
            
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
            
            self.skip_newlines()
        
        return Program(statements)
    
    def statement(self) -> Optional[Statement]:
        self.skip_newlines()
        
        if self.current_token.type == TokenType.EOF:
            return None
        
        if self.current_token.type == TokenType.INCLUDE:
            return self.preprocessor_directive()
        
        if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.DOUBLE, 
                                      TokenType.CHAR_TYPE, TokenType.VOID):
            return self.declaration_or_function()
        
        if self.current_token.type == TokenType.IF:
            return self.if_statement()
        
        if self.current_token.type == TokenType.WHILE:
            return self.while_statement()
        
        if self.current_token.type == TokenType.FOR:
            return self.for_statement()
        
        if self.current_token.type == TokenType.RETURN:
            return self.return_statement()
        
        if self.current_token.type == TokenType.BREAK:
            self.eat(TokenType.BREAK)
            return BreakStatement()
        
        if self.current_token.type == TokenType.CONTINUE:
            self.eat(TokenType.CONTINUE)
            return ContinueStatement()
        
        if self.current_token.type == TokenType.LBRACE:
            return self.block_statement()
        
        return self.expression_statement()
    
    def parse_type_with_pointers(self) -> Tuple[str, int]:
        """型とポインタレベルを解析"""
        var_type = self.current_token.value
        self.eat(self.current_token.type)
        
        pointer_level = 0
        while self.current_token.type == TokenType.MULTIPLY:
            pointer_level += 1
            self.eat(TokenType.MULTIPLY)
        
        return var_type, pointer_level
    
    def preprocessor_directive(self) -> PreprocessorDirective:
        self.eat(TokenType.INCLUDE)
        
        if self.current_token.type == TokenType.IDENTIFIER:
            directive = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            value = ""
            if self.current_token.type == TokenType.STRING:
                value = self.current_token.value
                self.eat(TokenType.STRING)
            elif self.current_token.type == TokenType.LESS:
                self.eat(TokenType.LESS)
                if self.current_token.type == TokenType.IDENTIFIER:
                    value = self.current_token.value
                    self.eat(TokenType.IDENTIFIER)
                if self.current_token.type == TokenType.GREATER:
                    self.eat(TokenType.GREATER)
            
            return PreprocessorDirective(directive, value)
        
        return PreprocessorDirective("include")
    
    def declaration_or_function(self) -> Statement:
        var_type, pointer_level = self.parse_type_with_pointers()
        
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        if self.current_token.type == TokenType.LPAREN:
            return self.function_definition(var_type, name, pointer_level)
        else:
            return self.multiple_variable_declaration(var_type, name, pointer_level)
    
    def multiple_variable_declaration(self, var_type: str, first_name: str, pointer_level: int = 0) -> Block:
        """Handle multiple variable declarations like: int a = 1, b = 2, c;"""
        declarations = []
        
        # First variable
        declarations.append(self.variable_declaration(var_type, first_name, pointer_level))
        
        # Additional variables
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            
            # Parse additional pointer levels for this variable
            var_pointer_level = pointer_level
            while self.current_token.type == TokenType.MULTIPLY:
                var_pointer_level += 1
                self.eat(TokenType.MULTIPLY)
            
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            declarations.append(self.variable_declaration(var_type, var_name, var_pointer_level))
        
        if len(declarations) == 1:
            return declarations[0]
        else:
            return Block(declarations)
    
    def variable_declaration(self, var_type: str, name: str, pointer_level: int = 0) -> Declaration:
        dimensions = []
        value = None
        initializer = None
        
        # Handle multi-dimensional arrays
        while self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            if self.current_token.type != TokenType.RBRACKET:
                dimensions.append(self.expression())
            else:
                dimensions.append(None)
            self.eat(TokenType.RBRACKET)
        
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            if self.current_token.type == TokenType.LBRACE:
                initializer = self.array_initializer()
            else:
                value = self.expression()
        
        # For backward compatibility
        size = dimensions[0] if dimensions else None
        
        return Declaration(var_type, name, value, size, initializer, dimensions, pointer_level)
    
    def array_initializer(self) -> ArrayInitializer:
        self.eat(TokenType.LBRACE)
        elements = []
        
        if self.current_token.type != TokenType.RBRACE:
            if self.current_token.type == TokenType.LBRACE:
                # Nested array initializer (flatten for now)
                nested = self.array_initializer()
                elements.extend(nested.elements)
            else:
                elements.append(self.expression())
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                if self.current_token.type == TokenType.RBRACE:
                    break
                if self.current_token.type == TokenType.LBRACE:
                    # Nested array initializer
                    nested = self.array_initializer()
                    elements.extend(nested.elements)
                else:
                    elements.append(self.expression())
        
        self.eat(TokenType.RBRACE)
        return ArrayInitializer(elements)
    
    def function_definition(self, return_type: str, name: str, pointer_level: int = 0) -> FunctionDef:
        self.eat(TokenType.LPAREN)
        
        params = []
        if self.current_token.type != TokenType.RPAREN:
            param_type, param_pointer_level = self.parse_type_with_pointers()
            param_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            params.append(Parameter(param_type, param_name, pointer_level=param_pointer_level))
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                param_type, param_pointer_level = self.parse_type_with_pointers()
                param_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                params.append(Parameter(param_type, param_name, pointer_level=param_pointer_level))
        
        self.eat(TokenType.RPAREN)
        self.skip_newlines()
        
        body = self.block_statement()
        
        return FunctionDef(return_type, name, params, body)
    
    def if_statement(self) -> IfStatement:
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        self.skip_newlines()
        condition = self.expression()
        self.skip_newlines()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        then_stmt = self.statement()
        
        else_stmt = None
        self.skip_newlines()
        if self.current_token.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.skip_newlines()
            else_stmt = self.statement()
        
        return IfStatement(condition, then_stmt, else_stmt)
    
    def while_statement(self) -> WhileStatement:
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        body = self.statement()
        
        return WhileStatement(condition, body)
    
    def for_statement(self) -> ForStatement:
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)
        
        init = None
        if self.current_token.type != TokenType.SEMICOLON:
            if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.DOUBLE, TokenType.CHAR_TYPE):
                init = self.declaration_or_function()
            else:
                init = self.expression_statement()
        self.eat(TokenType.SEMICOLON)
        
        condition = None
        if self.current_token.type != TokenType.SEMICOLON:
            condition = self.expression()
        self.eat(TokenType.SEMICOLON)
        
        update = None
        if self.current_token.type != TokenType.RPAREN:
            update = self.expression()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        body = self.statement()
        
        return ForStatement(init, condition, update, body)
    
    def return_statement(self) -> ReturnStatement:
        self.eat(TokenType.RETURN)
        
        value = None
        if self.current_token.type not in (TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.EOF):
            value = self.expression()
        
        return ReturnStatement(value)
    
    def block_statement(self) -> Block:
        self.eat(TokenType.LBRACE)
        self.skip_newlines()
        
        statements = []
        while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
                continue
            
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
            
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
            
            self.skip_newlines()
        
        self.eat(TokenType.RBRACE)
        return Block(statements)
    
    def expression_statement(self) -> ExpressionStatement:
        expr = self.assignment_expression()
        return ExpressionStatement(expr)

    
    def expression(self) -> Expression:
        return self.assignment_expression()
    
    def assignment_expression(self) -> Expression:
        node = self.logical_or()
        
        if self.current_token.type in (TokenType.ASSIGN, TokenType.PLUS_ASSIGN,
                                     TokenType.MINUS_ASSIGN, TokenType.MULTIPLY_ASSIGN,
                                     TokenType.DIVIDE_ASSIGN, TokenType.MODULO_ASSIGN):
            token = self.current_token
            self.eat(self.current_token.type)
            self.skip_newlines()
            value = self.assignment_expression()
            return Assignment(node, value, token.type)
        
        return node
    
    def logical_or(self) -> Expression:
        node = self.logical_and()
        
        while self.current_token.type == TokenType.LOGICAL_OR:
            token = self.current_token
            self.eat(TokenType.LOGICAL_OR)
            self.skip_newlines()
            right = self.logical_and()
            node = BinaryOp(node, token.type, right)
        
        return node
    
    def logical_and(self) -> Expression:
        node = self.equality()
        
        while self.current_token.type == TokenType.LOGICAL_AND:
            token = self.current_token
            self.eat(TokenType.LOGICAL_AND)
            self.skip_newlines()
            right = self.equality()
            node = BinaryOp(node, token.type, right)
        
        return node
    
    def equality(self) -> Expression:
        node = self.relational()
        
        while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL):
            token = self.current_token
            self.eat(self.current_token.type)
            self.skip_newlines()
            right = self.relational()
            node = BinaryOp(node, token.type, right)
        
        return node
    
    def relational(self) -> Expression:
        node = self.additive()
        
        while self.current_token.type in (TokenType.LESS, TokenType.LESS_EQUAL,
                                         TokenType.GREATER, TokenType.GREATER_EQUAL):
            token = self.current_token
            self.eat(self.current_token.type)
            self.skip_newlines()
            right = self.additive()
            node = BinaryOp(node, token.type, right)
        
        return node
    
    def additive(self) -> Expression:
        node = self.multiplicative()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            self.eat(self.current_token.type)
            self.skip_newlines()
            right = self.multiplicative()
            node = BinaryOp(node, token.type, right)
        
        return node
    
    def multiplicative(self) -> Expression:
        node = self.unary()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            token = self.current_token
            self.eat(self.current_token.type)
            self.skip_newlines()
            right = self.unary()
            node = BinaryOp(node, token.type, right)
        
        return node
    
    def unary(self) -> Expression:
        if self.current_token.type in (TokenType.PLUS, TokenType.MINUS, TokenType.LOGICAL_NOT):
            token = self.current_token
            self.eat(self.current_token.type)
            return UnaryOp(token.type, self.unary())
        
        if self.current_token.type in (TokenType.INCREMENT, TokenType.DECREMENT):
            token = self.current_token
            self.eat(self.current_token.type)
            return UnaryOp(token.type, self.postfix())
        
        # ポインタ演算子
        if self.current_token.type == TokenType.MULTIPLY:
            # デリファレンス演算子 *ptr
            token = self.current_token
            self.eat(TokenType.MULTIPLY)
            return UnaryOp(TokenType.DEREFERENCE, self.unary())
        
        if self.current_token.type == TokenType.BITWISE_AND:
            # アドレス演算子 &var
            token = self.current_token
            self.eat(TokenType.BITWISE_AND)
            return UnaryOp(TokenType.ADDRESS_OF, self.unary())
        
        if self.current_token.type == TokenType.SIZEOF:
            # sizeof演算子
            self.eat(TokenType.SIZEOF)
            self.eat(TokenType.LPAREN)
            if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.DOUBLE, TokenType.CHAR_TYPE):
                # sizeof(type)
                type_name = self.current_token.value
                self.eat(self.current_token.type)
                # ポインタレベルをチェック
                while self.current_token.type == TokenType.MULTIPLY:
                    self.eat(TokenType.MULTIPLY)
                self.eat(TokenType.RPAREN)
                return Literal(4)  # 簡単のため、すべて4バイトとする
            else:
                # sizeof(expression)
                expr = self.expression()
                self.eat(TokenType.RPAREN)
                return Literal(4)  # 簡単のため、すべて4バイトとする
        
        return self.postfix()
    
    def postfix(self) -> Expression:
        node = self.primary()
        
        while True:
            if self.current_token.type == TokenType.LBRACKET:
                # Handle multi-dimensional array access
                while self.current_token.type == TokenType.LBRACKET:
                    self.eat(TokenType.LBRACKET)
                    self.skip_newlines()
                    index = self.expression()
                    self.skip_newlines()
                    self.eat(TokenType.RBRACKET)
                    node = ArrayAccess(node, index)
            
            elif self.current_token.type == TokenType.LPAREN:
                if isinstance(node, Identifier):
                    self.eat(TokenType.LPAREN)
                    self.skip_newlines()
                    args = []
                    if self.current_token.type != TokenType.RPAREN:
                        args.append(self.expression())
                        while self.current_token.type == TokenType.COMMA:
                            self.eat(TokenType.COMMA)
                            self.skip_newlines()
                            args.append(self.expression())
                    self.skip_newlines()
                    self.eat(TokenType.RPAREN)
                    node = FunctionCall(node.name, args)
                else:
                    break
            
            elif self.current_token.type in (TokenType.INCREMENT, TokenType.DECREMENT):
                token = self.current_token
                self.eat(self.current_token.type)
                node = PostfixOp(node, token.type)
            
            else:
                break
        
        return node
    
    def primary(self) -> Expression:
        # Skip newlines in expressions
        self.skip_newlines()
        
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            value = float(token.value) if '.' in token.value else int(token.value)
            return Literal(value)
        
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return Literal(token.value)
        
        elif token.type == TokenType.CHAR:
            self.eat(TokenType.CHAR)
            return Literal(ord(token.value))
        
        elif token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Identifier(token.value)
        
        elif token.type in (TokenType.PRINTF, TokenType.SCANF, TokenType.PUTS, TokenType.GETS,
                           TokenType.STRLEN, TokenType.STRCPY, TokenType.STRCMP, TokenType.MALLOC,
                           TokenType.FREE, TokenType.REALLOC):
            func_name = token.value
            self.eat(token.type)
            return Identifier(func_name)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            self.skip_newlines()
            
            # 型キャストは無視してそのまま括弧式として処理
            # 通常の括弧式
            node = self.expression()
            self.skip_newlines()
            self.eat(TokenType.RPAREN)
            return node
        
        else:
            self.error(f"Unexpected token in expression: {token.type}")