#!/usr/bin/env python3

import sys
from .interpreter import OuroborosInterpreter
from .errors import InterpreterError

def main():
    if len(sys.argv) != 2:
        print("Usage: python -m ouroboros <file.c>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        interpreter = OuroborosInterpreter()
        results = interpreter.interpret(code)
        
        for result in results:
            if result is not None:
                print(f"Result: {result}")
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except InterpreterError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def run_code(code: str):
    try:
        interpreter = OuroborosInterpreter()
        results = interpreter.interpret(code)
        return results
    except InterpreterError as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    main()