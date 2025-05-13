
from typing import Any
class Message(object):
    def __init__(self, handler: Any|None = None,print_level:str|None = None,*args,**kwargs):
        self.handler = handler or print
        self.print_level = print_level or "INFO"
    
    def is_print(self,print_level:str) -> bool:
        print_level_mapping = {
            "DEBUG":0,
            "INFO":1,
            "WARNING":2,
            "ERROR":3,
            "CRITICAL":4,
        }
        return print_level_mapping[print_level] >= print_level_mapping[self.print_level]
    
    def print(self,*args,**kwargs) -> None:
        self.handler(*args,**kwargs)
    
    def debug(self,*args,**kwargs) -> None:
        if self.is_print("DEBUG"):
            self.print(*args,**kwargs)
    
    def info(self,*args,**kwargs) -> None:
        if self.is_print("INFO"):
            self.print(*args,**kwargs)
    
    def warning(self,*args,**kwargs) -> None:
        if self.is_print("WARNING"):
            self.print(*args,**kwargs)
    
    def error(self,*args,**kwargs) -> None:
        if self.is_print("ERROR"):
            self.print(*args,**kwargs)
    
    def critical(self,*args,**kwargs) -> None:
        if self.is_print("CRITICAL"):
            self.print(*args,**kwargs)
    
    def set_print_level(self,print_level:str) -> None:
        self.print_level = print_level
    
    def set_handler(self,handler:Any) -> None:
        self.handler = handler
    
    

message = Message()
