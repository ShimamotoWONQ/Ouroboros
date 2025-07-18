#!/usr/bin/env python3

from typing import Any, Dict, List
from .lexer import TokenType
from .ast_nodes import *
from .errors import RuntimeError

class Evaluator:
    def __init__(self, variables: Dict[str, Any], functions: Dict[str, Any], stdlib, interpreter):
        self.variables = variables
        self.functions = functions
        self.stdlib = stdlib
        self.interpreter = interpreter
    
    def get_variable(self, name: str) -> Any:
        return self.interpreter.get_variable(name)
    
    def set_variable(self, name: str, value: Any):
        self.interpreter.set_variable(name, value)
    
    def evaluate(self, node: Expression) -> Any:
        if isinstance(node, Literal):
            return node.value
        
        elif isinstance(node, Identifier):
            return self.get_variable(node.name)
        
        elif isinstance(node, BinaryOp):
            return self.evaluate_binary_op(node)
        
        elif isinstance(node, UnaryOp):
            return self.evaluate_unary_op(node)
        
        elif isinstance(node, FunctionCall):
            return self.evaluate_function_call(node)
        
        elif isinstance(node, ArrayAccess):
            array = self.evaluate(node.array)
            index = self.evaluate(node.index)
            
            if isinstance(array, int) and hasattr(self.interpreter, 'memory_manager'):
                # ポインタの場合、メモリから読み取り
                try:
                    return self.interpreter.memory_manager.read_memory(array, int(index))
                except Exception as e:
                    raise RuntimeError(f"Memory access error: {e}")
            elif isinstance(array, list):
                return array[int(index)]
            elif hasattr(array, '__getitem__'):
                # Handle Matrix and other custom types
                return array[int(index)]
            else:
                raise RuntimeError(f"Cannot index non-array value: {type(array)}")
        
        elif isinstance(node, Assignment):
            return self.interpreter.execute_assignment(node)
        
        elif isinstance(node, ArrayInitializer):
            return [self.evaluate(element) for element in node.elements]
        
        elif isinstance(node, PostfixOp):
            return self.evaluate_postfix_op(node)
        
        elif isinstance(node, TypeCast):
            return self.evaluate_type_cast(node)
        
        else:
            raise RuntimeError(f"Unknown expression type: {type(node)}")
    
    def evaluate_binary_op(self, node: BinaryOp) -> Any:
        left = self.evaluate(node.left)
        
        # Short-circuit evaluation for logical operators
        if node.op == TokenType.LOGICAL_AND:
            if not left:
                return 0
            right = self.evaluate(node.right)
            return 1 if left and right else 0
        elif node.op == TokenType.LOGICAL_OR:
            if left:
                return 1
            right = self.evaluate(node.right)
            return 1 if left or right else 0
        
        right = self.evaluate(node.right)
        
        if node.op == TokenType.PLUS:
            return left + right
        elif node.op == TokenType.MINUS:
            return left - right
        elif node.op == TokenType.MULTIPLY:
            return left * right
        elif node.op == TokenType.DIVIDE:
            if right == 0:
                raise RuntimeError("Division by zero")
            return left // right if isinstance(left, int) and isinstance(right, int) else left / right
        elif node.op == TokenType.MODULO:
            return left % right
        elif node.op == TokenType.EQUAL:
            return 1 if left == right else 0
        elif node.op == TokenType.NOT_EQUAL:
            return 1 if left != right else 0
        elif node.op == TokenType.LESS:
            return 1 if left < right else 0
        elif node.op == TokenType.LESS_EQUAL:
            return 1 if left <= right else 0
        elif node.op == TokenType.GREATER:
            return 1 if left > right else 0
        elif node.op == TokenType.GREATER_EQUAL:
            return 1 if left >= right else 0
        elif node.op == TokenType.BITWISE_AND:
            return int(left) & int(right)
        elif node.op == TokenType.BITWISE_OR:
            return int(left) | int(right)
        elif node.op == TokenType.BITWISE_XOR:
            return int(left) ^ int(right)
        else:
            raise RuntimeError(f"Unknown binary operator: {node.op}")
    
    def evaluate_unary_op(self, node: UnaryOp) -> Any:
        operand = node.operand
        
        if node.op == TokenType.MINUS:
            return -self.evaluate(operand)
        elif node.op == TokenType.PLUS:
            return self.evaluate(operand)
        elif node.op == TokenType.LOGICAL_NOT:
            return 1 if not self.evaluate(operand) else 0
        elif node.op == TokenType.DEREFERENCE:
            # ポインタのデリファレンス *ptr
            address = self.evaluate(operand)
            if isinstance(address, int) and hasattr(self.interpreter, 'memory_manager'):
                try:
                    return self.interpreter.memory_manager.read_memory(address, 0)
                except Exception as e:
                    raise RuntimeError(f"Dereference error: {e}")
            else:
                raise RuntimeError("Cannot dereference non-pointer value")
        elif node.op == TokenType.ADDRESS_OF:
            # 変数のアドレス取得 &var
            if isinstance(operand, Identifier):
                # 簡単な実装：変数名のハッシュをアドレスとして使用
                # 実際の実装では変数のメモリ位置を返すべき
                return hash(operand.name) & 0xFFFFFF + 0x1000
            else:
                raise RuntimeError("Cannot take address of non-lvalue")
        elif node.op == TokenType.INCREMENT:
            if isinstance(operand, Identifier):
                current_value = self.get_variable(operand.name)
                new_value = current_value + 1
                self.set_variable(operand.name, new_value)
                return new_value
            else:
                raise RuntimeError("Invalid operand for prefix increment")
        elif node.op == TokenType.DECREMENT:
            if isinstance(operand, Identifier):
                current_value = self.get_variable(operand.name)
                new_value = current_value - 1
                self.set_variable(operand.name, new_value)
                return new_value
            else:
                raise RuntimeError("Invalid operand for prefix decrement")
        else:
            raise RuntimeError(f"Unknown unary operator: {node.op}")
    
    def evaluate_postfix_op(self, node: PostfixOp) -> Any:
        operand = node.operand
        
        if node.op == TokenType.INCREMENT:
            if isinstance(operand, Identifier):
                current_value = self.get_variable(operand.name)
                self.set_variable(operand.name, current_value + 1)
                return current_value
            else:
                raise RuntimeError("Invalid operand for postfix increment")
        elif node.op == TokenType.DECREMENT:
            if isinstance(operand, Identifier):
                current_value = self.get_variable(operand.name)
                self.set_variable(operand.name, current_value - 1)
                return current_value
            else:
                raise RuntimeError("Invalid operand for postfix decrement")
        else:
            raise RuntimeError(f"Unknown postfix operator: {node.op}")
    
    def evaluate_function_call(self, node: FunctionCall) -> Any:
        args = [self.evaluate(arg) for arg in node.args]
        
        if node.name in self.stdlib.functions:
            return self.stdlib.call_function(node.name, args)
        elif node.name in self.functions:
            return self.functions[node.name].call(args, self.interpreter)
        else:
            raise RuntimeError(f"Undefined function: {node.name}")
    
    def evaluate_type_cast(self, node) -> Any:
        """型キャストの評価"""
        value = self.evaluate(node.expression)
        
        if node.pointer_level > 0:
            # ポインタ型へのキャスト
            return int(value)
        elif node.target_type == 'int':
            return int(value)
        elif node.target_type in ['float', 'double']:
            return float(value)
        elif node.target_type == 'char':
            return int(value) & 0xFF
        else:
            return value