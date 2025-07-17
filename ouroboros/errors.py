#!/usr/bin/env python3

class InterpreterError(Exception):
    pass

class LexerError(InterpreterError):
    def __init__(self, message: str, line: int):
        self.message = message
        self.line = line
        super().__init__(f"Lexer error at line {line}: {message}")

class ParserError(InterpreterError):
    def __init__(self, message: str, line: int):
        self.message = message
        self.line = line
        super().__init__(f"Parser error at line {line}: {message}")

class RuntimeError(InterpreterError):
    def __init__(self, message: str, line: int = None):
        self.message = message
        self.line = line
        if line:
            super().__init__(f"Runtime error at line {line}: {message}")
        else:
            super().__init__(f"Runtime error: {message}")

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value