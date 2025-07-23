#!/usr/bin/env python3

import sys
from .interpreter import OuroborosInterpreter
from .errors import InterpreterError
from .logger import Logger

def main():
    if len(sys.argv) != 2:
        Logger.info("Usage: python -m ouroboros <file.c>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r') as f:
            code = f.read()
        
        interpreter = OuroborosInterpreter()
        results = interpreter.interpret(code)
        
        for result in results:
            if result is not None:
                Logger.info(f"Result: {result}")
    
    except FileNotFoundError:
        Logger.error(f"File '{filename}' not found")
        sys.exit(1)
    except InterpreterError as e:
        Logger.error(f"{e}")
        sys.exit(1)
    except Exception as e:
        Logger.error(f"Unexpected error: {e}")
        sys.exit(1)

def feed_to_ouroboros(code: str):
    try:
        interpreter = OuroborosInterpreter()
        results = interpreter.interpret(code)
        return results
    except InterpreterError as e:
        Logger.error(f"{e}")
        return []

if __name__ == "__main__":
    main()