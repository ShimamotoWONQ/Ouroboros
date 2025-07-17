#!/usr/bin/env python3
"""
Ouroboros - C language interpreter written in Python
"""

from typing import Dict, List, Any, Optional
from .core import TokenType, Token, Lexer, Function, BreakException, ContinueException, ReturnException

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
            result = self.factor()
            return 1 if not result else 0
        
        # 前置インクリメント・デクリメント
        elif token.type == TokenType.INCREMENT:
            self.eat(TokenType.INCREMENT)
            if self.current_token.type != TokenType.IDENTIFIER:
                self.error("Expected identifier after ++")
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            current_value = self.get_variable(var_name)
            new_value = current_value + 1
            self.set_variable(var_name, new_value)
            return new_value
        
        elif token.type == TokenType.DECREMENT:
            self.eat(TokenType.DECREMENT)
            if self.current_token.type != TokenType.IDENTIFIER:
                self.error("Expected identifier after --")
            var_name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            current_value = self.get_variable(var_name)
            new_value = current_value - 1
            self.set_variable(var_name, new_value)
            return new_value
        
        else:
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
        
        while self.current_token.type in (TokenType.EQUAL, TokenType.NOT_EQUAL, 
                                        TokenType.LESS, TokenType.LESS_EQUAL,
                                        TokenType.GREATER, TokenType.GREATER_EQUAL):
            token = self.current_token
            if token.type == TokenType.EQUAL:
                self.eat(TokenType.EQUAL)
                result = result == self.arithmetic_expression()
            elif token.type == TokenType.NOT_EQUAL:
                self.eat(TokenType.NOT_EQUAL)
                result = result != self.arithmetic_expression()
            elif token.type == TokenType.LESS:
                self.eat(TokenType.LESS)
                result = result < self.arithmetic_expression()
            elif token.type == TokenType.LESS_EQUAL:
                self.eat(TokenType.LESS_EQUAL)
                result = result <= self.arithmetic_expression()
            elif token.type == TokenType.GREATER:
                self.eat(TokenType.GREATER)
                result = result > self.arithmetic_expression()
            elif token.type == TokenType.GREATER_EQUAL:
                self.eat(TokenType.GREATER_EQUAL)
                result = result >= self.arithmetic_expression()
        
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
        
        # 複合代入演算子
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
        
        # インクリメント・デクリメント（後置）の場合
        elif self.current_token.type == TokenType.INCREMENT:
            self.eat(TokenType.INCREMENT)
            current_value = self.get_variable(var_name)
            self.set_variable(var_name, current_value + 1)
            return current_value
        
        elif self.current_token.type == TokenType.DECREMENT:
            self.eat(TokenType.DECREMENT)
            current_value = self.get_variable(var_name)
            self.set_variable(var_name, current_value - 1)
            return current_value
        
        # 単純な変数参照の場合（式文として）
        else:
            return self.get_variable(var_name)
    
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
        
        # 初期化付き宣言の場合
        if self.current_token.type == TokenType.ASSIGN:
            self.eat(TokenType.ASSIGN)
            value = self.expression()
            self.set_variable(var_name, value)
            return value
        else:
            # デフォルト値で初期化
            if var_type == 'int':
                self.set_variable(var_name, 0)
            elif var_type in ['float', 'double']:
                self.set_variable(var_name, 0.0)
            elif var_type == 'char':
                self.set_variable(var_name, '\0')
            else:
                self.set_variable(var_name, None)
            return None

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
        """for文の解析（修正版）"""
        self.eat(TokenType.FOR)
        self.eat(TokenType.LPAREN)
        
        # 初期化式
        if self.current_token.type != TokenType.SEMICOLON:
            if self.current_token.type in (TokenType.INT, TokenType.FLOAT, TokenType.DOUBLE, TokenType.CHAR_TYPE):
                # 変数宣言の場合
                self.declaration_statement()
            else:
                # 代入文または式の場合
                if self.current_token.type == TokenType.IDENTIFIER:
                    self.assignment_statement()
                else:
                    self.expression()
        self.eat(TokenType.SEMICOLON)
        
        # 条件式を保存
        condition_tokens = []
        while self.current_token.type != TokenType.SEMICOLON and self.current_token.type != TokenType.EOF:
            condition_tokens.append((self.current_token.type, self.current_token.value))
            self.current_token = self.lexer.get_next_token()
        self.eat(TokenType.SEMICOLON)
        
        # 更新式を保存
        update_tokens = []
        while self.current_token.type != TokenType.RPAREN and self.current_token.type != TokenType.EOF:
            update_tokens.append((self.current_token.type, self.current_token.value))
            self.current_token = self.lexer.get_next_token()
        self.eat(TokenType.RPAREN)
        
        self.skip_newlines()
        
        # ボディの位置を記録
        body_start_pos = self.lexer.pos
        body_start_line = self.lexer.line
        body_start_token = self.current_token
        
        # ボディをスキップして終了位置を記録
        if self.current_token.type == TokenType.LBRACE:
            self.skip_block()
        else:
            self.skip_statement()
        
        body_end_pos = self.lexer.pos
        
        result = None
        iteration_count = 0
        max_iterations = 10000  # 無限ループ防止
        
        try:
            while iteration_count < max_iterations:
                iteration_count += 1
                
                # 条件式の評価
                condition = True
                if condition_tokens:
                    condition = self.evaluate_token_sequence(condition_tokens)
                
                if not condition:
                    break
                
                # ボディの実行
                self.lexer.pos = body_start_pos
                self.lexer.line = body_start_line
                self.current_token = body_start_token
                
                if body_start_token.type == TokenType.LBRACE:
                    result = self.block_statement()
                else:
                    result = self.statement()
                
                # 更新式の実行
                if update_tokens:
                    self.execute_token_sequence(update_tokens)
        
        except BreakException:
            pass
        except ContinueException:
            pass
        
        # 元の位置を復元
        self.lexer.pos = body_end_pos
        self.current_token = self.lexer.get_next_token()
        
        return result

    def evaluate_token_sequence(self, tokens):
        """トークンシーケンスを評価"""
        if not tokens:
            return True
        
        # トークンシーケンスから文字列を再構築
        text = ' '.join(token[1] for token in tokens)
        
        # 新しいlexerで評価
        saved_lexer = self.lexer
        saved_token = self.current_token
        
        try:
            temp_lexer = Lexer(text)
            self.lexer = temp_lexer
            self.current_token = self.lexer.get_next_token()
            
            result = self.expression()
            return result
        except:
            return False
        finally:
            self.lexer = saved_lexer
            self.current_token = saved_token

    def execute_token_sequence(self, tokens):
        """トークンシーケンスを実行"""
        if not tokens:
            return
        
        # トークンシーケンスから文字列を再構築
        text = ' '.join(token[1] for token in tokens)
        
        # 新しいlexerで実行
        saved_lexer = self.lexer
        saved_token = self.current_token
        
        try:
            temp_lexer = Lexer(text)
            self.lexer = temp_lexer
            self.current_token = self.lexer.get_next_token()
            
            if self.current_token.type == TokenType.IDENTIFIER:
                # 次のトークンをチェックして代入文かどうか判定
                next_pos = self.lexer.pos
                next_token = self.lexer.get_next_token()
                
                # 位置を戻す
                self.lexer.pos = 0
                self.current_token = self.lexer.get_next_token()
                
                if next_token.type in (TokenType.ASSIGN, TokenType.PLUS_ASSIGN, 
                                    TokenType.MINUS_ASSIGN, TokenType.INCREMENT, 
                                    TokenType.DECREMENT):
                    self.assignment_statement()
                else:
                    self.expression()
            else:
                self.expression()
        except:
            pass  # 更新式エラーは無視
        finally:
            self.lexer = saved_lexer
            self.current_token = saved_token
            
    def block_statement(self):
        """ブロック文の解析"""
        self.eat(TokenType.LBRACE)
        self.skip_newlines()
        
        self.push_scope()
        result = None
        
        try:
            while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
                if self.current_token.type == TokenType.NEWLINE:
                    self.eat(TokenType.NEWLINE)
                    continue
                
                result = self.statement()
                
                # セミコロンがあれば消費
                if self.current_token.type == TokenType.SEMICOLON:
                    self.eat(TokenType.SEMICOLON)
                
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
        paren_depth = 0
        brace_depth = 0
        
        while self.current_token.type != TokenType.EOF:
            if self.current_token.type == TokenType.LPAREN:
                paren_depth += 1
            elif self.current_token.type == TokenType.RPAREN:
                paren_depth -= 1
                if paren_depth < 0:
                    break
            elif self.current_token.type == TokenType.LBRACE:
                brace_depth += 1
            elif self.current_token.type == TokenType.RBRACE:
                brace_depth -= 1
                if brace_depth < 0:
                    break
            elif (self.current_token.type in (TokenType.SEMICOLON, TokenType.NEWLINE) 
                and paren_depth == 0 and brace_depth == 0):
                if self.current_token.type == TokenType.SEMICOLON:
                    self.eat(TokenType.SEMICOLON)
                break
            
            self.current_token = self.lexer.get_next_token()
    
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
                identifier = self.current_token.value
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
        
        # 前置インクリメント・デクリメント
        elif self.current_token.type in (TokenType.INCREMENT, TokenType.DECREMENT):
            return self.expression()

        # EOF、NEWLINEではNoneを返す
        elif self.current_token.type in (TokenType.EOF, TokenType.NEWLINE):
            return None
        
        else:
            try:
                result = self.expression()
                return result
            except:
                self.error(f"Unexpected token: {self.current_token.type}")

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
