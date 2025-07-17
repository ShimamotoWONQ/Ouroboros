#!/usr/bin/env python3

from typing import List, Any

class StandardLibrary:
    def __init__(self):
        self.functions = {
            'printf': self.printf,
            'scanf': self.scanf,
            'puts': self.puts,
            'gets': self.gets,
            'strlen': self.strlen,
            'strcpy': self.strcpy,
            'strcmp': self.strcmp,
            'malloc': self.malloc,
            'free': self.free,
        }
    
    def printf(self, args: List[Any]) -> int:
        if not args:
            return 0
        
        format_str = str(args[0])
        arg_index = 1
        
        result = ""
        i = 0
        while i < len(format_str):
            if format_str[i] == '%' and i + 1 < len(format_str):
                spec = format_str[i + 1]
                if spec == 'd':
                    if arg_index < len(args):
                        result += str(int(args[arg_index]))
                        arg_index += 1
                    else:
                        result += '0'
                elif spec == 'f':
                    if arg_index < len(args):
                        result += str(float(args[arg_index]))
                        arg_index += 1
                    else:
                        result += '0.0'
                elif spec == 'c':
                    if arg_index < len(args):
                        result += chr(int(args[arg_index]))
                        arg_index += 1
                    else:
                        result += '\0'
                elif spec == 's':
                    if arg_index < len(args):
                        result += str(args[arg_index])
                        arg_index += 1
                    else:
                        result += ''
                elif spec == '%':
                    result += '%'
                else:
                    result += format_str[i:i+2]
                i += 2
            else:
                result += format_str[i]
                i += 1
        
        print(result, end='')
        return 0
    
    def scanf(self, args: List[Any]) -> int:
        try:
            user_input = input()
            if user_input.isdigit() or (user_input.startswith('-') and user_input[1:].isdigit()):
                return int(user_input)
            else:
                try:
                    return float(user_input)
                except ValueError:
                    return 0
        except:
            return 0
    
    def puts(self, args: List[Any]) -> int:
        if args:
            print(str(args[0]))
        else:
            print()
        return 0
    
    def gets(self, args: List[Any]) -> str:
        try:
            return input()
        except:
            return ""
    
    def strlen(self, args: List[Any]) -> int:
        if args:
            return len(str(args[0]))
        return 0
    
    def strcpy(self, args: List[Any]) -> str:
        if len(args) >= 2:
            return str(args[1])
        return ""
    
    def strcmp(self, args: List[Any]) -> int:
        if len(args) >= 2:
            str1 = str(args[0])
            str2 = str(args[1])
            if str1 < str2:
                return -1
            elif str1 > str2:
                return 1
            else:
                return 0
        return 0
    
    def malloc(self, args: List[Any]) -> List[Any]:
        if args:
            size = int(args[0])
            return [0] * size
        return []
    
    def free(self, args: List[Any]) -> int:
        return 0
    
    def call_function(self, name: str, args: List[Any]) -> Any:
        if name in self.functions:
            return self.functions[name](args)
        else:
            raise NameError(f"Undefined standard library function: {name}")