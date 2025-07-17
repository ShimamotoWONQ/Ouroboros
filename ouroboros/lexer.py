#!/usr/bin/env python3

from enum import Enum
from typing import Optional

class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    CHAR = "CHAR"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    ASSIGN = "ASSIGN"
    
    # Compound assignment operators
    PLUS_ASSIGN = "PLUS_ASSIGN"
    MINUS_ASSIGN = "MINUS_ASSIGN"
    MULTIPLY_ASSIGN = "MULTIPLY_ASSIGN"
    DIVIDE_ASSIGN = "DIVIDE_ASSIGN"
    MODULO_ASSIGN = "MODULO_ASSIGN"
    
    # Increment/Decrement
    INCREMENT = "INCREMENT"
    DECREMENT = "DECREMENT"
    
    # Comparison operators
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # Logical operators
    LOGICAL_AND = "LOGICAL_AND"
    LOGICAL_OR = "LOGICAL_OR"
    LOGICAL_NOT = "LOGICAL_NOT"
    
    # Bitwise operators
    BITWISE_AND = "BITWISE_AND"
    BITWISE_OR = "BITWISE_OR"
    BITWISE_XOR = "BITWISE_XOR"
    
    # Delimiters
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    
    # Keywords
    INT = "INT"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    CHAR_TYPE = "CHAR_TYPE"
    VOID = "VOID"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    FOR = "FOR"
    DO = "DO"
    RETURN = "RETURN"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    SWITCH = "SWITCH"
    CASE = "CASE"
    DEFAULT = "DEFAULT"
    
    # Standard library functions
    PRINTF = "PRINTF"
    SCANF = "SCANF"
    GETS = "GETS"
    PUTS = "PUTS"
    STRLEN = "STRLEN"
    STRCPY = "STRCPY"
    STRCMP = "STRCMP"
    MALLOC = "MALLOC"
    FREE = "FREE"
    
    # Preprocessor
    INCLUDE = "INCLUDE"
    DEFINE = "DEFINE"
    
    # Others
    NEWLINE = "NEWLINE"
    EOF = "EOF"

class Token:
    def __init__(self, type_: TokenType, value: str, line: int = 1):
        self.type = type_
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.keywords = {
            'int': TokenType.INT,
            'float': TokenType.FLOAT,
            'double': TokenType.DOUBLE,
            'char': TokenType.CHAR_TYPE,
            'void': TokenType.VOID,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'while': TokenType.WHILE,
            'for': TokenType.FOR,
            'do': TokenType.DO,
            'return': TokenType.RETURN,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'switch': TokenType.SWITCH,
            'case': TokenType.CASE,
            'default': TokenType.DEFAULT,
            'printf': TokenType.PRINTF,
            'scanf': TokenType.SCANF,
            'gets': TokenType.GETS,
            'puts': TokenType.PUTS,
            'strlen': TokenType.STRLEN,
            'strcpy': TokenType.STRCPY,
            'strcmp': TokenType.STRCMP,
            'malloc': TokenType.MALLOC,
            'free': TokenType.FREE,
            'include': TokenType.INCLUDE,
            'define': TokenType.DEFINE,
        }
    
    def error(self, message: str):
        raise SyntaxError(f"Lexer error at line {self.line}: {message}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.text):
            return self.text[pos]
        return None
    
    def advance(self):
        if self.pos < len(self.text) and self.text[self.pos] == '\n':
            self.line += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.pos < len(self.text) and self.text[self.pos] in ' \t':
            self.pos += 1
    
    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            while self.pos < len(self.text) and self.text[self.pos] != '\n':
                self.advance()
        elif self.peek() == '/' and self.peek(1) == '*':
            self.advance()
            self.advance()
            while self.pos < len(self.text) - 1:
                if self.text[self.pos] == '*' and self.text[self.pos + 1] == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()
    
    def read_number(self) -> str:
        result = ''
        has_dot = False
        while self.pos < len(self.text):
            char = self.text[self.pos]
            if char.isdigit():
                result += char
                self.advance()
            elif char == '.' and not has_dot:
                has_dot = True
                result += char
                self.advance()
            else:
                break
        return result
    
    def read_identifier(self) -> str:
        result = ''
        while (self.pos < len(self.text) and 
               (self.text[self.pos].isalnum() or self.text[self.pos] == '_')):
            result += self.text[self.pos]
            self.advance()
        return result
    
    def read_string(self) -> str:
        result = ''
        self.advance()
        while self.pos < len(self.text) and self.text[self.pos] != '"':
            if self.text[self.pos] == '\\':
                self.advance()
                if self.pos < len(self.text):
                    escape_char = self.text[self.pos]
                    if escape_char == 'n':
                        result += '\n'
                    elif escape_char == 't':
                        result += '\t'
                    elif escape_char == 'r':
                        result += '\r'
                    elif escape_char == '\\':
                        result += '\\'
                    elif escape_char == '"':
                        result += '"'
                    elif escape_char == '0':
                        result += '\0'
                    else:
                        result += escape_char
                    self.advance()
            else:
                result += self.text[self.pos]
                self.advance()
        
        if self.pos >= len(self.text):
            self.error("Unterminated string")
        
        self.advance()
        return result
    
    def read_char(self) -> str:
        result = ''
        self.advance()
        if self.text[self.pos] == '\\':
            self.advance()
            escape_char = self.text[self.pos]
            if escape_char == 'n':
                result = '\n'
            elif escape_char == 't':
                result = '\t'
            elif escape_char == '\\':
                result = '\\'
            elif escape_char == "'":
                result = "'"
            else:
                result = escape_char
            self.advance()
        else:
            result = self.text[self.pos]
            self.advance()
        
        if self.pos >= len(self.text) or self.text[self.pos] != "'":
            self.error("Unterminated character")
        
        self.advance()
        return result
    
    def get_next_token(self) -> Token:
        while self.pos < len(self.text):
            current_char = self.text[self.pos]
            
            if current_char in ' \t':
                self.skip_whitespace()
                continue
            
            if current_char == '\n':
                token = Token(TokenType.NEWLINE, current_char, self.line)
                self.advance()
                return token
            
            if current_char == '/' and self.peek(1) in ['/', '*']:
                self.skip_comment()
                continue
            
            if current_char.isdigit():
                return Token(TokenType.NUMBER, self.read_number(), self.line)
            
            if current_char.isalpha() or current_char == '_':
                identifier = self.read_identifier()
                token_type = self.keywords.get(identifier, TokenType.IDENTIFIER)
                return Token(token_type, identifier, self.line)
            
            if current_char == '"':
                return Token(TokenType.STRING, self.read_string(), self.line)
            
            if current_char == "'":
                return Token(TokenType.CHAR, self.read_char(), self.line)
            
            if current_char == '+':
                if self.peek(1) == '+':
                    self.advance()
                    self.advance()
                    return Token(TokenType.INCREMENT, '++', self.line)
                elif self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.PLUS_ASSIGN, '+=', self.line)
                else:
                    self.advance()
                    return Token(TokenType.PLUS, '+', self.line)
            
            if current_char == '-':
                if self.peek(1) == '-':
                    self.advance()
                    self.advance()
                    return Token(TokenType.DECREMENT, '--', self.line)
                elif self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.MINUS_ASSIGN, '-=', self.line)
                else:
                    self.advance()
                    return Token(TokenType.MINUS, '-', self.line)
            
            if current_char == '*':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.MULTIPLY_ASSIGN, '*=', self.line)
                else:
                    self.advance()
                    return Token(TokenType.MULTIPLY, '*', self.line)
            
            if current_char == '/':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.DIVIDE_ASSIGN, '/=', self.line)
                else:
                    self.advance()
                    return Token(TokenType.DIVIDE, '/', self.line)
            
            if current_char == '%':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.MODULO_ASSIGN, '%=', self.line)
                else:
                    self.advance()
                    return Token(TokenType.MODULO, '%', self.line)
            
            if current_char == '=':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.EQUAL, '==', self.line)
                else:
                    self.advance()
                    return Token(TokenType.ASSIGN, '=', self.line)
            
            if current_char == '!':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.NOT_EQUAL, '!=', self.line)
                else:
                    self.advance()
                    return Token(TokenType.LOGICAL_NOT, '!', self.line)
            
            if current_char == '<':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.LESS_EQUAL, '<=', self.line)
                else:
                    self.advance()
                    return Token(TokenType.LESS, '<', self.line)
            
            if current_char == '>':
                if self.peek(1) == '=':
                    self.advance()
                    self.advance()
                    return Token(TokenType.GREATER_EQUAL, '>=', self.line)
                else:
                    self.advance()
                    return Token(TokenType.GREATER, '>', self.line)
            
            if current_char == '&':
                if self.peek(1) == '&':
                    self.advance()
                    self.advance()
                    return Token(TokenType.LOGICAL_AND, '&&', self.line)
                else:
                    self.advance()
                    return Token(TokenType.BITWISE_AND, '&', self.line)
            
            if current_char == '|':
                if self.peek(1) == '|':
                    self.advance()
                    self.advance()
                    return Token(TokenType.LOGICAL_OR, '||', self.line)
                else:
                    self.advance()
                    return Token(TokenType.BITWISE_OR, '|', self.line)
            
            if current_char == '^':
                self.advance()
                return Token(TokenType.BITWISE_XOR, '^', self.line)
            
            if current_char == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';', self.line)
            
            if current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.line)
            
            if current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line)
            
            if current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line)
            
            if current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.line)
            
            if current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.line)
            
            if current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, '[', self.line)
            
            if current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, ']', self.line)
            
            if current_char == '#':
                self.advance()
                return Token(TokenType.INCLUDE, '#', self.line)
            
            self.error(f"Unexpected character: {current_char}")
        
        return Token(TokenType.EOF, '', self.line)