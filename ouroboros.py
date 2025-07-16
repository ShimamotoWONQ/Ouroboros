#!/usr/bin/env python3
"""
Ouroboros - C language interpreter written in Python
"""

from typing import Dict, List, Any, Optional
from enum import Enum

class TokenType(Enum):
    # リテラル
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    CHAR = "CHAR"
    
    # 演算子
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    MODULO = "MODULO"
    ASSIGN = "ASSIGN"
    
    # 複合代入演算子
    PLUS_ASSIGN = "PLUS_ASSIGN"
    MINUS_ASSIGN = "MINUS_ASSIGN"
    MULTIPLY_ASSIGN = "MULTIPLY_ASSIGN"
    DIVIDE_ASSIGN = "DIVIDE_ASSIGN"
    MODULO_ASSIGN = "MODULO_ASSIGN"
    
    # インクリメント・デクリメント
    INCREMENT = "INCREMENT"
    DECREMENT = "DECREMENT"
    
    # 比較演算子
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    
    # 論理演算子
    LOGICAL_AND = "LOGICAL_AND"
    LOGICAL_OR = "LOGICAL_OR"
    LOGICAL_NOT = "LOGICAL_NOT"
    
    # ビット演算子
    BITWISE_AND = "BITWISE_AND"
    BITWISE_OR = "BITWISE_OR"
    BITWISE_XOR = "BITWISE_XOR"
    
    # 区切り文字
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    
    # キーワード
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
    
    # 標準ライブラリ関数
    PRINTF = "PRINTF"
    SCANF = "SCANF"
    GETS = "GETS"
    PUTS = "PUTS"
    STRLEN = "STRLEN"
    STRCPY = "STRCPY"
    STRCMP = "STRCMP"
    MALLOC = "MALLOC"
    FREE = "FREE"
    
    # プリプロセッサ
    INCLUDE = "INCLUDE"
    DEFINE = "DEFINE"
    
    # その他
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
    """拡張された字句解析器"""
    
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
        """コメントをスキップ"""
        if self.peek() == '/' and self.peek(1) == '/':
            # 単行コメント
            while self.pos < len(self.text) and self.text[self.pos] != '\n':
                self.advance()
        elif self.peek() == '/' and self.peek(1) == '*':
            # 多行コメント
            self.advance()  # skip /
            self.advance()  # skip *
            while self.pos < len(self.text) - 1:
                if self.text[self.pos] == '*' and self.text[self.pos + 1] == '/':
                    self.advance()  # skip *
                    self.advance()  # skip /
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
        self.advance()  # skip opening quote
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
        
        self.advance()  # skip closing quote
        return result
    
    def read_char(self) -> str:
        result = ''
        self.advance()  # skip opening quote
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
        
        self.advance()  # skip closing quote
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
            
            # コメントチェック
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
            
            # 演算子の解析
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
            
            # 区切り文字
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
            
            # プリプロセッサ
            if current_char == '#':
                self.advance()
                return Token(TokenType.INCLUDE, '#', self.line)
            
            self.error(f"Unexpected character: {current_char}")
        
        return Token(TokenType.EOF, '', self.line)

class Function:
    """関数オブジェクト"""
    def __init__(self, name: str, params: List[str], body: List, return_type: str = 'int'):
        self.name = name
        self.params = params
        self.body = body
        self.return_type = return_type

class BreakException(Exception):
    """break文用の例外"""
    pass

class ContinueException(Exception):
    """continue文用の例外"""
    pass

class ReturnException(Exception):
    """return文用の例外"""
    def __init__(self, value):
        self.value = value

class OuroborosInterpreter:
    """拡張されたOuroborosインタープリター"""
    
    def __init__(self):
        self.global_variables: Dict[str, Any] = {}
        self.local_variables: List[Dict[str, Any]] = []
        self.functions: Dict[str, Function] = {}
        self.lexer: Optional[Lexer] = None
        self.current_token: Optional[Token] = None
        
        # 標準ライブラリの初期化
        self.init_stdlib()
    
    def init_stdlib(self):
        """標準ライブラリ関数の初期化"""
        self.stdlib_functions = {
            'printf', 'scanf', 'puts', 'gets', 'strlen', 'strcpy', 'strcmp'
        }
    
    def get_variables(self) -> Dict[str, Any]:
        """現在のスコープの変数を取得"""
        if self.local_variables:
            return self.local_variables[-1]
        return self.global_variables
    
    def set_variable(self, name: str, value: Any):
        """変数を設定"""
        variables = self.get_variables()
        variables[name] = value
    
    def get_variable(self, name: str) -> Any:
        """変数を取得"""
        # ローカルスコープから検索
        for scope in reversed(self.local_variables):
            if name in scope:
                return scope[name]
        
        # グローバルスコープから検索
        if name in self.global_variables:
            return self.global_variables[name]
        
        raise NameError(f"Undefined variable: {name}")
    
    def push_scope(self):
        """新しいスコープをプッシュ"""
        self.local_variables.append({})
    
    def pop_scope(self):
        """スコープをポップ"""
        if self.local_variables:
            self.local_variables.pop()
    
    def error(self, message: str):
        line = self.current_token.line if self.current_token else "unknown"
        raise SyntaxError(f"Parser error at line {line}: {message}")
    
    def eat(self, token_type: TokenType):
        """指定されたトークンタイプを消費"""
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected {token_type}, got {self.current_token.type}")
    
    def skip_newlines(self):
        """改行をスキップ"""
        while self.current_token.type == TokenType.NEWLINE:
            self.eat(TokenType.NEWLINE)
    
    def factor(self):
        """因子の解析"""
        token = self.current_token
        
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return float(token.value) if '.' in token.value else int(token.value)
        
        elif token.type == TokenType.CHAR:
            self.eat(TokenType.CHAR)
            return ord(token.value)
        
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return token.value
        
        elif token.type == TokenType.IDENTIFIER:
            var_name = token.value
            self.eat(TokenType.IDENTIFIER)
            
            # 関数呼び出しチェック
            if self.current_token.type == TokenType.LPAREN:
                return self.function_call(var_name)
            
            # 配列アクセスチェック
            if self.current_token.type == TokenType.LBRACKET:
                self.eat(TokenType.LBRACKET)
                index = self.expression()
                self.eat(TokenType.RBRACKET)
                array = self.get_variable(var_name)
                if isinstance(array, list):
                    return array[int(index)]
                else:
                    self.error(f"Cannot index non-array variable: {var_name}")
            
            # インクリメント・デクリメント（後置）
            if self.current_token.type == TokenType.INCREMENT:
                self.eat(TokenType.INCREMENT)
                current_value = self.get_variable(var_name)
                self.set_variable(var_name, current_value + 1)
                return current_value
            
            if self.current_token.type == TokenType.DECREMENT:
                self.eat(TokenType.DECREMENT)
                current_value = self.get_variable(var_name)
                self.set_variable(var_name, current_value - 1)
                return current_value
            
            return self.get_variable(var_name)
        
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expression()
            self.eat(TokenType.RPAREN)
            return result
        
        elif token.type == TokenType.MINUS:
            self.eat(TokenType.MINUS)
            return -self.factor()
        
        elif token.type == TokenType.LOGICAL_NOT:
            self.eat(TokenType.LOGICAL_NOT)
            return not self.factor()
        
        # 前置インクリメント・デクリメント
        elif token.type == TokenType.INCREMENT:
            self.eat(TokenType.INCREMENT)
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            current_value = self.get_variable(var_name)
            new_value = current_value + 1
            self.set_variable(var_name, new_value)
            return new_value
        
        elif token.type == TokenType.DECREMENT:
            self.eat(TokenType.DECREMENT)
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            current_value = self.get_variable(var_name)
            new_value = current_value - 1
            self.set_variable(var_name, new_value)
            return new_value
        
        self.error(f"Unexpected token in expression: {token.type}")
    
    def term(self):
        """項の解析（乗算・除算・剰余）"""
        result = self.factor()
        
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            token = self.current_token
            if token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
                result = result * self.factor()
            elif token.type == TokenType.DIVIDE:
                self.eat(TokenType.DIVIDE)
                divisor = self.factor()
                if divisor == 0:
                    self.error("Division by zero")
                result = result // divisor if isinstance(result, int) and isinstance(divisor, int) else result / divisor
            elif token.type == TokenType.MODULO:
                self.eat(TokenType.MODULO)
                result = result % self.factor()
        
        return result
    
    def arithmetic_expression(self):
        """算術式の解析（加算・減算）"""
        result = self.term()
        
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result = result + self.term()
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
                result = result - self.term()
        
        return result
    
    def comparison_expression(self):
        """比較式の解析"""
        result = self.arithmetic_expression()
        
        if self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL, 
                                     TokenType.LESS, TokenType.LESS_EQUAL,
                                     TokenType.GREATER, TokenType.GREATER_EQUAL):
            token = self.current_token
            if token.type == TokenType.EQUAL:
                self.eat(TokenType.EQUAL)
                return result == self.arithmetic_expression()
            elif token.type == TokenType.NOT_EQUAL:
                self.eat(TokenType.NOT_EQUAL)
                return result != self.arithmetic_expression()
            elif token.type == TokenType.LESS:
                self.eat(TokenType.LESS)
                return result < self.arithmetic_expression()
            elif token.type == TokenType.LESS_EQUAL:
                self.eat(TokenType.LESS_EQUAL)
                return result <= self.arithmetic_expression()
            elif token.type == TokenType.GREATER:
                self.eat(TokenType.GREATER)
                return result > self.arithmetic_expression()
            elif token.type == TokenType.GREATER_EQUAL:
                self.eat(TokenType.GREATER_EQUAL)
                return result >= self.arithmetic_expression()
        
        return result
    
    def logical_expression(self):
        """論理式の解析"""
        result = self.comparison_expression()
        
        while self.current_token.type in (TokenType.LOGICAL_AND, TokenType.LOGICAL_OR):
            token = self.current_token
            if token.type == TokenType.LOGICAL_AND:
                self.eat(TokenType.LOGICAL_AND)
                result = result and self.comparison_expression()
            elif token.type == TokenType.LOGICAL_OR:
                self.eat(TokenType.LOGICAL_OR)
                result = result or self.comparison_expression()
        
        return result
    
    def expression(self):
        """式の解析"""
        return self.logical_expression()
    
    def function_call(self, func_name: str):
        """関数呼び出しの解析"""
        self.eat(TokenType.LPAREN)
        
        # 標準ライブラリ関数の処理
        if func_name in self.stdlib_functions:
            return self.call_stdlib_function(func_name)
        
        # ユーザー定義関数の処理
        if func_name not in self.functions:
            self.error(f"Undefined function: {func_name}")
        
        function = self.functions[func_name]
        args = []
        
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.expression())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.expression())
        
        self.eat(TokenType.RPAREN)
        
        # 関数実行
        return self.execute_function(function, args)
    
    def call_stdlib_function(self, func_name: str):
        """標準ライブラリ関数の呼び出し"""
        args = []
        
        if self.current_token.type != TokenType.RPAREN:
            args.append(self.expression())
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.expression())
        
        self.eat(TokenType.RPAREN)
        
        if func_name == 'printf':
            if args:
                format_str = str(args[0])
                # 簡単なprintf実装
                for i, arg in enumerate(args[1:], 1):
                    format_str = format_str.replace('%d', str(int(arg)), 1)
                    format_str = format_str.replace('%f', str(float(arg)), 1)
                    format_str = format_str.replace('%c', chr(int(arg)), 1)
                    format_str = format_str.replace('%s', str(arg), 1)
                print(format_str, end='')
            return 0
        
        elif func_name == 'puts':
            if args:
                print(str(args[0]))
            return 0
        
        elif func_name == 'strlen':
            if args:
                return len(str(args[0]))
            return 0
        
        elif func_name == 'scanf':
            # 簡単なscanf実装
            try:
                user_input = input()
                return int(user_input) if user_input.isdigit() else 0
            except:
                return 0
        
        return 0
    
    def execute_function(self, function: Function, args: List[Any]):
        """ユーザー定義関数の実行"""
        self.push_scope()
        
        # 引数をローカル変数に設定
        for i, param in enumerate(function.params):
            if i < len(args):
                self.set_variable(param, args[i])
            else:
                self.set_variable(param, 0)
        
        try:
            result = 0  # デフォルト戻り値
            
            # 関数ボディを再パース・実行
            saved_lexer = self.lexer
            saved_token = self.current_token
            
            # 関数ボディを新しいlexerで解析
            body_lexer = Lexer(function.body)
            self.lexer = body_lexer
            self.current_token = self.lexer.get_next_token()
            
            # ボディを実行
            while self.current_token.type != TokenType.EOF:
                if self.current_token.type == TokenType.NEWLINE:
                    self.eat(TokenType.NEWLINE)
                    continue
                
                stmt_result = self.statement()
                if stmt_result is not None:
                    result = stmt_result
                
                # セミコロンがあれば消費
                if self.current_token.type == TokenType.SEMICOLON:
                    self.eat(TokenType.SEMICOLON)
                
                self.skip_newlines()
            
            # lexerを復元
            self.lexer = saved_lexer
            self.current_token = saved_token
            
        except ReturnException as e:
            result = e.value
        finally:
            self.pop_scope()
        
        return result
    
    def execute_statement(self, statement):
        """文の実行（ASTノードから）"""
        # ここではシンプルに文字列として処理
        # 実際の実装ではASTノードを作成すべき
        pass
    
    def assignment_statement(self):
        """代入文の解析"""
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # 配列代入の場合
        if self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            index = self.expression()
            self.eat(TokenType.RBRACKET)
            
            if self.current_token.type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                value = self.expression()
                array = self.get_variable(var_name)
                if isinstance(array, list):
                    array[int(index)] = value
                else:
                    self.error(f"Cannot index non-array variable: {var_name}")
                return value
        
        # 通常の代入
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            value = self.expression()
            self.set_variable(var_name, value)
            return value
        
        # 複合代入演算子（拡張版）
        elif self.current_token.type == TokenType.PLUS_ASSIGN:
            self.eat(TokenType.PLUS_ASSIGN)
            current_value = self.get_variable(var_name)
            new_value = current_value + self.expression()
            self.set_variable(var_name, new_value)
            return new_value
        
        elif self.current_token.type == TokenType.MINUS_ASSIGN:
            self.eat(TokenType.MINUS_ASSIGN)
            current_value = self.get_variable(var_name)
            new_value = current_value - self.expression()
            self.set_variable(var_name, new_value)
            return new_value
        
        elif self.current_token.type == TokenType.MULTIPLY_ASSIGN:
            self.eat(TokenType.MULTIPLY_ASSIGN)
            current_value = self.get_variable(var_name)
            new_value = current_value * self.expression()
            self.set_variable(var_name, new_value)
            return new_value
        
        elif self.current_token.type == TokenType.DIVIDE_ASSIGN:
            self.eat(TokenType.DIVIDE_ASSIGN)
            current_value = self.get_variable(var_name)
            divisor = self.expression()
            if divisor == 0:
                self.error("Division by zero")
            new_value = current_value // divisor if isinstance(current_value, int) and isinstance(divisor, int) else current_value / divisor
            self.set_variable(var_name, new_value)
            return new_value
        
        elif self.current_token.type == TokenType.MODULO_ASSIGN:
            self.eat(TokenType.MODULO_ASSIGN)
            current_value = self.get_variable(var_name)
            new_value = current_value % self.expression()
            self.set_variable(var_name, new_value)
            return new_value
        
        else:
            self.error(f"Expected assignment operator after {var_name}")
            
    def declaration_statement(self):
        """変数宣言文の解析"""
        var_type = self.current_token.value
        self.eat(self.current_token.type)  # int, float, char, etc.
        
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        # 配列宣言の場合
        if self.current_token.type == TokenType.LBRACKET:
            self.eat(TokenType.LBRACKET)
            size = self.expression()
            self.eat(TokenType.RBRACKET)
            
            # 配列の初期化
            if var_type == 'int':
                array = [0] * int(size)
            elif var_type == 'float':
                array = [0.0] * int(size)
            elif var_type == 'char':
                array = ['\0'] * int(size)
            else:
                array = [None] * int(size)
            
            self.set_variable(var_name, array)
            return array
        
        # 通常の変数宣言
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            value = self.expression()
            self.set_variable(var_name, value)
        else:
            # デフォルト値
            if var_type == 'int':
                self.set_variable(var_name, 0)
            elif var_type in ['float', 'double']:
                self.set_variable(var_name, 0.0)
            elif var_type == 'char':
                self.set_variable(var_name, '\0')
            else:
                self.set_variable(var_name, None)
    
    def if_statement(self):
        """if文の解析"""
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        
        # if文のボディ
        if condition:
            if self.current_token.type == TokenType.LBRACE:
                return self.block_statement()
            else:
                return self.statement()
        else:
            # if文をスキップ
            if self.current_token.type == TokenType.LBRACE:
                self.skip_block()
            else:
                self.skip_statement()
            
            # else文があるかチェック
            self.skip_newlines()
            if self.current_token.type == TokenType.ELSE:
                self.eat(TokenType.ELSE)
                self.skip_newlines()
                if self.current_token.type == TokenType.LBRACE:
                    return self.block_statement()
                else:
                    return self.statement()
        
        return None
    
    def while_statement(self):
        """while文の解析"""
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        
        # 条件式の位置を記録
        condition_start = self.lexer.pos
        condition_line = self.current_token.line
        
        condition = self.expression()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        
        result = None
        try:
            while condition:
                # ループボディの実行
                if self.current_token.type == TokenType.LBRACE:
                    result = self.block_statement()
                else:
                    result = self.statement()
                
                # 条件を再評価
                saved_pos = self.lexer.pos
                saved_line = self.lexer.line
                saved_token = self.current_token
                
                self.lexer.pos = condition_start
                self.lexer.line = condition_line
                self.current_token = self.lexer.get_next_token()
                condition = self.expression()
                
                # 元の位置に戻る（ボディの開始位置）
                self.lexer.pos = saved_pos
                self.lexer.line = saved_line
                self.current_token = saved_token
        
        except BreakException:
            pass
        except ContinueException:
            pass
        
        return result
    
    def for_statement(self):
        """for文の解析"""
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)
        
        # 初期化式
        if self.current_token.type != TokenType.SEMICOLON:
            self.statement()
        self.eat(TokenType.SEMICOLON)
        
        # 条件式の位置を記録
        condition_start = self.lexer.pos
        condition_line = self.current_token.line
        
        # 条件式
        condition = True
        if self.current_token.type != TokenType.SEMICOLON:
            condition = self.expression()
        self.eat(TokenType.SEMICOLON)
        
        # 更新式の位置を記録
        update_start = self.lexer.pos
        update_line = self.current_token.line
        
        # 更新式をスキップ（後で実行）
        if self.current_token.type != TokenType.RPAREN:
            self.expression()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        
        result = None
        try:
            while condition:
                # ループボディの実行
                if self.current_token.type == TokenType.LBRACE:
                    result = self.block_statement()
                else:
                    result = self.statement()
                
                # 更新式の実行
                saved_pos = self.lexer.pos
                saved_line = self.lexer.line
                saved_token = self.current_token
                
                self.lexer.pos = update_start
                self.lexer.line = update_line
                self.current_token = self.lexer.get_next_token()
                if self.current_token.type != TokenType.RPAREN:
                    self.expression()
                
                # 条件式の再評価
                self.lexer.pos = condition_start
                self.lexer.line = condition_line
                self.current_token = self.lexer.get_next_token()
                if self.current_token.type != TokenType.SEMICOLON:
                    condition = self.expression()
                
                # 元の位置に戻る
                self.lexer.pos = saved_pos
                self.lexer.line = saved_line
                self.current_token = saved_token
        
        except BreakException:
            pass
        except ContinueException:
            pass
        
        return result
    
    def block_statement(self):
        """ブロック文の解析"""
        self.eat(TokenType.LBRACE)
        self.skip_newlines()
        
        self.push_scope()
        result = None
        
        try:
            while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
                result = self.statement()
                self.skip_newlines()
        finally:
            self.pop_scope()
        
        self.eat(TokenType.RBRACE)
        return result
    
    def skip_block(self):
        """ブロックをスキップ"""
        self.eat(TokenType.LBRACE)
        brace_count = 1
        
        while brace_count > 0 and self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.LBRACE:
                brace_count += 1
            elif self.current_token.type == TokenType.RBRACE:
                brace_count -= 1
            self.current_token = self.lexer.get_next_token()
    
    def skip_statement(self):
        """文をスキップ"""
        while (self.current_token.type not in (TokenType.SEMICOLON, TokenType.NEWLINE, 
                                              TokenType.EOF, TokenType.RBRACE)):
            self.current_token = self.lexer.get_next_token()
        if self.current_token.type == TokenType.SEMICOLON:
            self.eat(TokenType.SEMICOLON)
    
    # 1. function_definition()メソッドの修正
    def function_definition(self):
        """関数定義の解析"""
        return_type = self.current_token.value
        self.eat(self.current_token.type)  # return type
        
        func_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.LPAREN)
        
        # パラメータの解析
        params = []
        if self.current_token.type != TokenType.RPAREN:
            # パラメータタイプをスキップ
            self.eat(self.current_token.type)
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                self.eat(self.current_token.type)  # param type
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        
        self.eat(TokenType.RPAREN)
        self.skip_newlines()
        
        # 関数ボディの解析（簡単化のため、文字列として保存）
        body_start = self.lexer.pos
        self.skip_block()
        body_end = self.lexer.pos
        
        body_text = self.lexer.text[body_start:body_end-1]  # excluding final }
        
        function = Function(func_name, params, body_text, return_type)
        self.functions[func_name] = function
        
        # main関数の場合は自動実行
        if func_name == 'main':
            try:
                return self.execute_function(function, [])
            except ReturnException as e:
                return e.value
        
        # 関数定義の場合はNoneを返す（結果に含めない）
        return None
    
    def return_statement(self):
        """return文の解析"""
        self.eat(TokenType.RETURN)
        
        value = 0
        if self.current_token.type not in (TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.EOF):
            value = self.expression()
        
        raise ReturnException(value)
    
    def break_statement(self):
        """break文の解析"""
        self.eat(TokenType.BREAK)
        raise BreakException()
    
    def continue_statement(self):
        """continue文の解析"""
        self.eat(TokenType.CONTINUE)
        raise ContinueException()
    
    def preprocessor_directive(self):
        """プリプロセッサディレクティブの解析"""
        self.eat(TokenType.INCLUDE)
        
        if self.current_token.type == TokenType.IDENTIFIER:
            directive = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            if directive == 'include':
                # #include の処理（スキップ）
                if self.current_token.type == TokenType.LESS:
                    self.eat(TokenType.LESS)
                    header = self.current_token.value
                    self.eat(TokenType.IDENTIFIER)
                    if self.current_token.type == TokenType.GREATER:
                        self.eat(TokenType.GREATER)
                elif self.current_token.type == TokenType.STRING:
                    header = self.current_token.value
                    self.eat(TokenType.STRING)
                
                print(f"// Including header: {header}")
            
            elif directive == 'define':
                # #define の処理（スキップ）
                macro_name = self.current_token.value
                self.eat(TokenType.IDENTIFIER)
                print(f"// Defining macro: {macro_name}")
    
    def statement(self):
        """文の解析"""
        self.skip_newlines()
        
        if self.current_token.type == TokenType.EOF:
            return None
        
        # プリプロセッサディレクティブ
        elif self.current_token.type == TokenType.INCLUDE:
            self.preprocessor_directive()
            return None
        
        # 変数宣言
        elif self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.DOUBLE, TokenType.CHAR_TYPE):
            # 関数定義かチェック
            saved_pos = self.lexer.pos
            saved_line = self.lexer.line
            saved_token = self.current_token
            
            self.eat(self.current_token.type)  # type
            if self.current_token.type == TokenType.IDENTIFIER:
                self.eat(TokenType.IDENTIFIER)
                if self.current_token.type == TokenType.LPAREN:
                    # 関数定義
                    self.lexer.pos = saved_pos
                    self.lexer.line = saved_line
                    self.current_token = saved_token
                    result = self.function_definition()
                    return result  # main関数の場合は実行結果、その他はNone
            
            # 変数宣言
            self.lexer.pos = saved_pos
            self.lexer.line = saved_line
            self.current_token = saved_token
            self.declaration_statement()
            return None
        
        # 制御文
        elif self.current_token.type == TokenType.IF:
            return self.if_statement()
        
        elif self.current_token.type == TokenType.WHILE:
            return self.while_statement()
        
        elif self.current_token.type == TokenType.FOR:
            return self.for_statement()
        
        elif self.current_token.type == TokenType.RETURN:
            return self.return_statement()
        
        elif self.current_token.type == TokenType.BREAK:
            return self.break_statement()
        
        elif self.current_token.type == TokenType.CONTINUE:
            return self.continue_statement()
        
        elif self.current_token.type == TokenType.LBRACE:
            return self.block_statement()
        
        # 標準ライブラリ関数呼び出し
        elif self.current_token.type in (TokenType.PRINTF, TokenType.SCANF, TokenType.PUTS):
            func_name = self.current_token.value
            self.eat(self.current_token.type)
            if self.current_token.type == TokenType.LPAREN:
                return self.function_call(func_name)
        
        # 代入文または式文
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.assignment_statement()
        
        else:
            # 式文として処理
            result = self.expression()
            return result
    
    def program(self):
        """プログラム全体の解析"""
        results = []
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
                continue
            
            try:
                result = self.statement()
                # Noneでない結果のみを追加
                if result is not None:
                    results.append(result)
            except (BreakException, ContinueException, ReturnException) as e:
                if isinstance(e, ReturnException):
                    results.append(e.value)
                break
            
            # セミコロンがあれば消費
            if self.current_token.type == TokenType.SEMICOLON:
                self.eat(TokenType.SEMICOLON)
            
            self.skip_newlines()
        
        return results
    
    def interpret(self, text: str):
        """インタープリター実行"""
        self.lexer = Lexer(text)
        self.current_token = self.lexer.get_next_token()
        return self.program()

def load_c_file(filename: str) -> str:
    """C言語ファイルを読み込み"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return ""
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def main():
    print("🐍 Ouroboros - Enhanced C Language Interpreter")
    print("C言語で書かれたコードをPythonで実行します")
    print("-" * 60)
    
    interpreter = OuroborosInterpreter()
    
    # より本格的なサンプルプログラム
    sample_programs = [
        """// 基本的な計算プログラム

int main() {
    int a = 10;
    int b = 20;
    int sum = a + b;
    printf("Sum: %d\\n", sum);
    return 0;
}""",
        
        """// ループを使ったプログラム

int main() {
    int i;
    int factorial = 1;
    int n = 5;
    
    for(i = 1; i <= n; i++) {
        factorial *= i;
    }
    
    printf("Factorial of %d is %d\\n", n, factorial);
    return 0;
}""",
        
        """// 配列を使ったプログラム

int main() {
    int numbers[5];
    int i = 0;
    int sum = 0;
    
    // 配列に値を代入
    for(i = 0; i < 5; i++) {
        numbers[i] = (i + 1) * 10;
    }
    
    // 合計を計算
    for(i = 0; i < 5; i++) {
        sum += numbers[i];
        printf("numbers[%d] = %d\\n", i, numbers[i]);
    }
    
    printf("Total sum: %d\\n", sum);
    return 0;
}"""
    ]
    
    print("\n📝 サンプルC言語プログラム:")
    for i, program in enumerate(sample_programs, 1):
        print(f"\n--- Sample {i} ---")
        print(program)
        print(f"\n🚀 実行結果:")
        try:
            # 新しいインタープリターインスタンスで実行
            test_interpreter = OuroborosInterpreter()
            results = test_interpreter.interpret(program)
            if results:
                print(results)
                print(f"Program returned: {results[-1]}")
        except Exception as e:
            print(f"エラー: {e}")
        
        print("-" * 40)
    
    print("\n" + "="*60)
    print("対話モードまたはファイル実行モード:")
    print("- C言語コードを直接入力")
    print("- 'load filename.c' でファイルを読み込み")
    print("- 'exit' で終了")
    
    while True:
        try:
            line = input("ouroboros> ").strip()
            if line.lower() in ('exit', 'quit'):
                break
            if not line:
                continue
            
            # ファイル読み込みコマンド
            if line.startswith('load '):
                filename = line[5:].strip()
                code = load_c_file(filename)
                if code:
                    print(f"Loading {filename}...")
                    print("🚀 実行結果:")
                    results = interpreter.interpret(code)
                    if results:
                        print(f"Program returned: {results[-1]}")
                continue
            
            # 直接コード実行
            results = interpreter.interpret(line)
            if results:
                for result in results:
                    print(f"=> {result}")
                    
        except KeyboardInterrupt:
            print("\n終了します...")
            break
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    main()