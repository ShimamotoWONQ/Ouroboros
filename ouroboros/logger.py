from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass
import shutil

class LogLevel(Enum):
    PRINT = "PRINT"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARN"
    ERROR = "ERROR"


class Style:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class LogEntry:
    level: LogLevel
    message: str
    data: Optional[Dict[str, Any]] = None


class Logger:
    _instance = None
    _log_level: LogLevel = LogLevel.DEBUG
    _enabled: bool = True
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_level(cls, level: LogLevel):
        """ Set log level of logger """
        cls._log_level = level
    
    @classmethod
    def set_enabled(cls, enabled: bool = True):
        """ Set activation of logger """
        cls._enabled = enabled
    
    @classmethod
    def _should_log(cls, level: LogLevel) -> bool:
        """ Format message to log """
        if not cls._enabled:
            return False
        
        level_order = {
            LogLevel.PRINT: 0,
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3,
        }
        
        return level_order.get(level, 0) >= level_order.get(cls._log_level, 0)
    
    @classmethod
    def _format_message(cls, level: LogLevel, message: str) -> str:
        """ Format message to log """
        color_map = {
            LogLevel.PRINT: Style.WHITE,
            LogLevel.DEBUG: Style.CYAN,
            LogLevel.INFO: Style.GREEN,
            LogLevel.WARNING: Style.YELLOW,
            LogLevel.ERROR: Style.RED,
        }
        
        color = color_map.get(level, Style.WHITE)

        if level == LogLevel.PRINT:
            return f"{color}{message}{Style.RESET}"
        else:
            return f"{color}{level.value}{Style.RESET}:\t{message}"
    
    @classmethod
    def print(cls, message: str, **kwargs):
        """ Print a normal log """
        if cls._should_log(LogLevel.PRINT):
            formatted_msg = cls._format_message(LogLevel.PRINT, message)
            print(formatted_msg)
    
    @classmethod
    def debug(cls, message: str, **kwargs):
        """ Print a debug log """
        if cls._should_log(LogLevel.DEBUG):
            formatted_msg = cls._format_message(LogLevel.DEBUG, message)
            print(formatted_msg)
    
    @classmethod
    def info(cls, message: str, **kwargs):
        """ Print a info log """
        if cls._should_log(LogLevel.INFO):
            formatted_msg = cls._format_message(LogLevel.INFO, message)
            print(formatted_msg)
    
    @classmethod
    def warning(cls, message: str, **kwargs):
        """ Print a warning log """
        if cls._should_log(LogLevel.WARNING):
            formatted_msg = cls._format_message(LogLevel.WARNING, message)
            print(formatted_msg)
    
    @classmethod
    def error(cls, message: str, **kwargs):
        """ Print a error log """
        if cls._should_log(LogLevel.ERROR):
            formatted_msg = cls._format_message(LogLevel.ERROR, message)
            print(formatted_msg)
    
    @classmethod
    def section_start(cls, title: str):
        """ Print a divider for start of section """
        if cls._should_log(LogLevel.INFO):
            print(f"\n{Style.BOLD}{Style.GREEN}--- {title} ---{Style.RESET}")
    
    @classmethod
    def section_end(cls, title: str):
        """ Print a divider for end of section """
        if cls._should_log(LogLevel.INFO):
            print(f"{Style.BOLD}{Style.GREEN}--- {title} ---{Style.RESET}\n")
    
    @classmethod
    def header(cls, title: str):
        """ Print a header """
        if cls._should_log(LogLevel.INFO):
            print(f"\n{Style.BLUE}=== {title} ==={Style.RESET}")
    
    @classmethod
    def divider(cls, title: str = ""):
        """ Print a divider """
        length = shutil.get_terminal_size().columns
        
        print("")
        if title:
            remaining_length = length - len(title) - 2
            if remaining_length > 0:
                print(f"{title} {'-' * remaining_length}")
            else:
                print(title)
        else:
            print("-" * length)
        print("")

    @classmethod
    def marker(cls):
        """ Print a marker """
        print(f"\n-*-*-*-*-*-\n")
    
    @classmethod
    def title(cls):
        
        ascii_title = """
     OURO   BO  RO  SOURO    BORO   SOURO    BORO   SOURO    BORO    SOURO      
    BO  RO  SO  UR  OB  OR  OS  OU  RO  BO  RO  SO  UR  BO  RO  SO  UR     
    OB  OR  OS  OU  ROBORO  SO  UR  OBORO   SO  UR  OBOROS  OU  RO   BORO  
    SO  UR  OB  OR  OS OU   RO  BO  RO  SO  UR  OB  OR OS   OU  RO      BO 
     ROSO    UROB   OR  OS   OURO   BOROS    OURO   BO  RO   SOUR   OBORO   S
        """

    #     ascii_logo = """
    #      _
    #    __|\____
    #   /# ~>    \ 
    #  /#/¯|/¯¯¯\ \ 
    #  |#| ¯  _ | |
    #  \#\___/|_/ /
    #   \#### <~ /
    #    ¯¯¯¯\|¯¯    
    #         ¯
    #     """
        
        required_width = max(len(line) for line in ascii_title.splitlines())
        console_width = shutil.get_terminal_size().columns

        if console_width >= required_width:
            print(ascii_title)
            # print(ascii_logo)
            print("C language interpreter written in Python written in C.")
        else:
            print("Ouroboros")
