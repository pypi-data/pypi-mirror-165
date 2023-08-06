# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.
#                   Created SyntaxError exception.
#                   Renamed LexException to LexError.
#                   Removed all other exceptions in favor of pushing them into one of the 3: LexError, SyntaxError or RuntimeError.
#                   This is to simplify exception handling for applications that use macal.

"""Exceptions classes for macal"""

from .macal_scope import MacalScope



class RuntimeError(Exception):
    def __init__(self, message: str):
        self.Message = message
        
    def __str__(self):
        return f"Runtime Error: {self.Message}"



class SyntaxError(Exception):
    def __init__(self, message: str):
        self.Message = message
        
    def __str__(self):
        return f"Syntax Error: {self.Message}"



class LexError(Exception):
    def __init__(self, message: str, line: int, offset: int, filename: str):
        self.message = message
        self.line = line
        self.offset = offset
        self.filename = filename

    def __repr__(self):
        return f"""LexError("{self.message}", {self.line}, {self.offset}, {self.filename})"""

    def __str__(self):
        return f"Lex Exception: {self.message} @ {self.line} , {self.offset} In: {self.filename}"



class NilParameterValueError(Exception):
    def __init__(self, name: str, scope: MacalScope, paramname: str, funcname: str = ""):
        self.Name = name
        self.Scope = scope
        self.FuncName = funcname
        self.ParamName = paramname

    def __str__(self):
        if self.Scope is None:
            return f"{self.Name}: Error passing nil value in parameter: {self.ParamName}. Function: {self.FuncName}."
        else:
            return f"{self.Name}: Error passing nil value in parameter: {self.ParamName}. Scope: {self.Scope.name}. Function: {self.FuncName}."



class InvalidVariableTypeException(Exception):
    def __init__(self, name: str, scope: MacalScope, invalid_type: str, required_type: str):
        self.Name = name
        self.Scope = scope
        self.InvalidType = invalid_type
        self.RequiredType = required_type
        
    def __str__(self):
        return f"Exception: Invalid variable ({self.Name}) type: {self.InvalidType}, required: {self.RequiredType}. ({self.Scope.name})"
