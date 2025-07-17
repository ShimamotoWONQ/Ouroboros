#!/usr/bin/env python3

from typing import Dict, List, Any, Optional
from .lexer import Lexer, TokenType
from .parser import Parser
from .ast_nodes import *
from .evaluator import Evaluator
from .stdlib import StandardLibrary
from .errors import RuntimeError, BreakException, ContinueException, ReturnException

class Function:
    def __init__(self, name: str, params: List[Parameter], body: Block, return_type: str = 'int'):
        self.name = name
        self.params = params
        self.body = body
        self.return_type = return_type
    
    def call(self, args: List[Any], interpreter) -> Any:
        interpreter.push_scope()
        
        for i, param in enumerate(self.params):
            if i < len(args):
                interpreter.set_variable(param.name, args[i])
            else:
                interpreter.set_variable(param.name, 0)
        
        try:
            result = interpreter.execute_statement(self.body)
            return result if result is not None else 0
        except ReturnException as e:
            return e.value
        finally:
            interpreter.pop_scope()

class OuroborosInterpreter:
    def __init__(self):
        self.global_variables: Dict[str, Any] = {}
        self.local_variables: List[Dict[str, Any]] = []
        self.functions: Dict[str, Function] = {}
        self.stdlib = StandardLibrary()
        self.evaluator = None
    
    def get_variables(self) -> Dict[str, Any]:
        if self.local_variables:
            return self.local_variables[-1]
        return self.global_variables
    
    def set_variable(self, name: str, value: Any):
        variables = self.get_variables()
        variables[name] = value
    
    def get_variable(self, name: str) -> Any:
        for scope in reversed(self.local_variables):
            if name in scope:
                return scope[name]
        
        if name in self.global_variables:
            return self.global_variables[name]
        
        raise RuntimeError(f"Undefined variable: {name}")
    
    def push_scope(self):
        self.local_variables.append({})
    
    def pop_scope(self):
        if self.local_variables:
            self.local_variables.pop()
    
    def execute_statement(self, node: Statement) -> Any:
        if isinstance(node, Block):
            return self.execute_block(node)
        
        elif isinstance(node, Declaration):
            return self.execute_declaration(node)
        
        elif isinstance(node, Assignment):
            return self.execute_assignment(node)
        
        elif isinstance(node, IfStatement):
            return self.execute_if_statement(node)
        
        elif isinstance(node, WhileStatement):
            return self.execute_while_statement(node)
        
        elif isinstance(node, ForStatement):
            return self.execute_for_statement(node)
        
        elif isinstance(node, ReturnStatement):
            return self.execute_return_statement(node)
        
        elif isinstance(node, BreakStatement):
            raise BreakException()
        
        elif isinstance(node, ContinueStatement):
            raise ContinueException()
        
        elif isinstance(node, FunctionDef):
            return self.execute_function_def(node)
        
        elif isinstance(node, ExpressionStatement):
            return self.evaluator.evaluate(node.expression)
        
        elif isinstance(node, PreprocessorDirective):
            return None
        
        else:
            raise RuntimeError(f"Unknown statement type: {type(node)}")
    
    def execute_block(self, node: Block) -> Any:
        result = None
        for statement in node.statements:
            result = self.execute_statement(statement)
        return result
    
    def execute_declaration(self, node: Declaration) -> Any:
        if node.initializer:
            # Array initialization with initializer list
            elements = self.evaluator.evaluate(node.initializer)
            self.set_variable(node.name, elements)
            return elements
        
        elif node.size:
            # Array declaration with size
            size = self.evaluator.evaluate(node.size)
            if node.var_type == 'int':
                array = [0] * int(size)
            elif node.var_type == 'float':
                array = [0.0] * int(size)
            elif node.var_type == 'char':
                array = ['\0'] * int(size)
            else:
                array = [None] * int(size)
            self.set_variable(node.name, array)
            return array
        
        elif node.value:
            # Variable declaration with value
            value = self.evaluator.evaluate(node.value)
            
            # Handle string to char array conversion
            if node.var_type == 'char' and isinstance(value, str):
                char_array = [ord(c) for c in value] + [0]  # null-terminated
                self.set_variable(node.name, char_array)
                return char_array
            else:
                self.set_variable(node.name, value)
                return value
        
        else:
            # Default initialization
            if node.var_type == 'int':
                self.set_variable(node.name, 0)
            elif node.var_type in ['float', 'double']:
                self.set_variable(node.name, 0.0)
            elif node.var_type == 'char':
                self.set_variable(node.name, '\0')
            else:
                self.set_variable(node.name, None)
            return None
    
    def execute_assignment(self, node: Assignment) -> Any:
        value = self.evaluator.evaluate(node.value)
        
        if isinstance(node.target, Identifier):
            if node.op == TokenType.ASSIGN:
                self.set_variable(node.target.name, value)
            elif node.op == TokenType.PLUS_ASSIGN:
                current = self.get_variable(node.target.name)
                self.set_variable(node.target.name, current + value)
            elif node.op == TokenType.MINUS_ASSIGN:
                current = self.get_variable(node.target.name)
                self.set_variable(node.target.name, current - value)
            elif node.op == TokenType.MULTIPLY_ASSIGN:
                current = self.get_variable(node.target.name)
                self.set_variable(node.target.name, current * value)
            elif node.op == TokenType.DIVIDE_ASSIGN:
                current = self.get_variable(node.target.name)
                if value == 0:
                    raise RuntimeError("Division by zero")
                self.set_variable(node.target.name, current // value if isinstance(current, int) and isinstance(value, int) else current / value)
            elif node.op == TokenType.MODULO_ASSIGN:
                current = self.get_variable(node.target.name)
                self.set_variable(node.target.name, current % value)
            
            return self.get_variable(node.target.name)
        
        elif isinstance(node.target, ArrayAccess):
            array = self.evaluator.evaluate(node.target.array)
            index = self.evaluator.evaluate(node.target.index)
            if isinstance(array, list):
                array[int(index)] = value
                return value
            else:
                raise RuntimeError("Cannot index non-array value")
        
        else:
            raise RuntimeError(f"Invalid assignment target: {type(node.target)}")
    
    def execute_if_statement(self, node: IfStatement) -> Any:
        condition = self.evaluator.evaluate(node.condition)
        
        if condition:
            return self.execute_statement(node.then_stmt)
        elif node.else_stmt:
            return self.execute_statement(node.else_stmt)
        
        return None
    
    def execute_while_statement(self, node: WhileStatement) -> Any:
        result = None
        try:
            while self.evaluator.evaluate(node.condition):
                result = self.execute_statement(node.body)
        except BreakException:
            pass
        except ContinueException:
            pass
        
        return result
    
    def execute_for_statement(self, node: ForStatement) -> Any:
        result = None
        
        self.push_scope()
        
        try:
            if node.init:
                self.execute_statement(node.init)
            
            while True:
                if node.condition and not self.evaluator.evaluate(node.condition):
                    break
                
                result = self.execute_statement(node.body)
                
                if node.update:
                    self.evaluator.evaluate(node.update)
        except BreakException:
            pass
        except ContinueException:
            if node.update:
                self.evaluator.evaluate(node.update)
        finally:
            self.pop_scope()
        
        return result
    
    def execute_return_statement(self, node: ReturnStatement) -> Any:
        value = 0
        if node.value:
            value = self.evaluator.evaluate(node.value)
        raise ReturnException(value)
    
    def execute_function_def(self, node: FunctionDef) -> Any:
        function = Function(node.name, node.params, node.body, node.return_type)
        self.functions[node.name] = function
        
        if node.name == 'main':
            try:
                return function.call([], self)
            except ReturnException as e:
                return e.value
        
        return None
    
    def interpret(self, text: str) -> List[Any]:
        lexer = Lexer(text)
        parser = Parser(lexer)
        ast = parser.parse()
        
        self.evaluator = Evaluator(self.global_variables, self.functions, self.stdlib, self)
        
        results = []
        for statement in ast.statements:
            try:
                result = self.execute_statement(statement)
                if result is not None:
                    results.append(result)
            except (BreakException, ContinueException, ReturnException) as e:
                if isinstance(e, ReturnException):
                    results.append(e.value)
                break
        
        return results