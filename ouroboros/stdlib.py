#!/usr/bin/env python3

from typing import List, Any

class StandardLibrary:
    def __init__(self, memory_manager=None):
        self.memory_manager = memory_manager
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
            'realloc': self.realloc,
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
                        val = args[arg_index]
                        if isinstance(val, int):
                            result += chr(val)
                        else:
                            result += str(val)
                        arg_index += 1
                    else:
                        result += '\0'
                elif spec == 's':
                    if arg_index < len(args):
                        val = args[arg_index]
                        if isinstance(val, list):
                            # char array to string
                            char_str = ""
                            for char in val:
                                if char == 0:
                                    break
                                char_str += chr(char) if isinstance(char, int) else str(char)
                            result += char_str
                        else:
                            result += str(val)
                        arg_index += 1
                    else:
                        result += ''
                elif spec == 'p':
                    # ポインタ表示
                    if arg_index < len(args):
                        val = args[arg_index]
                        if isinstance(val, int):
                            result += f"0x{val:08x}"
                        else:
                            result += str(val)
                        arg_index += 1
                    else:
                        result += '0x00000000'
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
            arg = args[0]
            if isinstance(arg, str):
                return len(arg)
            elif isinstance(arg, list):
                # null-terminated char array
                for i, char in enumerate(arg):
                    if char == 0:
                        return i
                return len(arg)
            elif isinstance(arg, int) and self.memory_manager:
                # ポインタの場合、メモリから読み取り
                try:
                    length = 0
                    while True:
                        char = self.memory_manager.read_memory(arg, length)
                        if char == 0:
                            break
                        length += 1
                    return length
                except:
                    return 0
        return 0
    
    def strcpy(self, args: List[Any]) -> Any:
        if len(args) >= 2:
            dest = args[0]
            src = args[1]
            
            if isinstance(dest, int) and self.memory_manager:
                # ポインタの場合
                if isinstance(src, str):
                    for i, char in enumerate(src):
                        self.memory_manager.write_memory(dest, i, ord(char))
                    self.memory_manager.write_memory(dest, len(src), 0)  # null terminator
                elif isinstance(src, list):
                    for i, char in enumerate(src):
                        self.memory_manager.write_memory(dest, i, char)
                        if char == 0:
                            break
                return dest
            else:
                return str(src) if src else ""
        return ""
    
    def strcmp(self, args: List[Any]) -> int:
        if len(args) >= 2:
            str1 = self._get_string_value(args[0])
            str2 = self._get_string_value(args[1])
            
            if str1 < str2:
                return -1
            elif str1 > str2:
                return 1
            else:
                return 0
        return 0
    
    def malloc(self, args: List[Any]) -> int:
        """メモリを確保し、アドレスを返す"""
        if not args or not self.memory_manager:
            return 0
        
        try:
            size = int(args[0])
            address = self.memory_manager.malloc(size)
            return address
        except Exception as e:
            print(f"malloc error: {e}")
            return 0
    
    def free(self, args: List[Any]) -> int:
        """メモリを解放"""
        if not args or not self.memory_manager:
            return 0
        
        try:
            address = int(args[0])
            if address == 0:  # NULL pointer
                return 0
            self.memory_manager.free(address)
            return 0
        except Exception as e:
            print(f"free error: {e}")
            return -1
    
    def realloc(self, args: List[Any]) -> int:
        """メモリを再確保"""
        if len(args) < 2 or not self.memory_manager:
            return 0
        
        try:
            address = int(args[0])
            new_size = int(args[1])
            new_address = self.memory_manager.realloc(address, new_size)
            return new_address
        except Exception as e:
            print(f"realloc error: {e}")
            return 0
    
    def _get_string_value(self, arg: Any) -> str:
        """引数から文字列値を取得するヘルパー関数"""
        if isinstance(arg, str):
            return arg
        elif isinstance(arg, list):
            # null-terminated char array
            result = ""
            for char in arg:
                if char == 0:
                    break
                result += chr(char) if isinstance(char, int) else str(char)
            return result
        elif isinstance(arg, int) and self.memory_manager:
            # ポインタの場合、メモリから読み取り
            try:
                result = ""
                offset = 0
                while True:
                    char = self.memory_manager.read_memory(arg, offset)
                    if char == 0:
                        break
                    result += chr(char) if isinstance(char, int) else str(char)
                    offset += 1
                return result
            except:
                return ""
        else:
            return str(arg)
    
    def call_function(self, name: str, args: List[Any]) -> Any:
        if name in self.functions:
            return self.functions[name](args)
        else:
            raise NameError(f"Undefined standard library function: {name}")