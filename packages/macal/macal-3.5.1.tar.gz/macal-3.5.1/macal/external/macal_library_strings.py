# Filename:       | macal_library_strings.py
# Author:         | Marco Caspers
# Version:        | 3.5.0
# Description:
#
# Macal 2.0 Strings Library                                                                       
#                                                                                                 
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.1.0 22-04-2022: raising excption if null parameter value is passed in.
#
# 3.5.0 16-05-2022: detached from class MacalLibrary and now implemented through include strings.mcl with "external" hooks to this module.
#

"""Strings library implementation"""

from macal.macal_library_external import *
from unidecode import unidecode
from macal.macal_exceptions import NilParameterValueError



def StrLen(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    arg = GetParamValue(params, "arg")
    at = GetParamType(params, "arg")
    if at != VariableTypes.STRING and at != VariableTypes.RECORD and at != VariableTypes.ARRAY and at != VariableTypes.PARAMS:
        raise RuntimeError(f"StrLen: Invalid argument type ({at}).")
    if arg is None:
        raise NilParameterValueError(name, scope, "arg", name)
    result = len(arg)
    scope.SetReturnValue(result, VariableTypes.INT)



def StrLeft(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of left function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    arg = GetParamValue(params, "arg")
    argl = GetParamValue(params, "length")
    if arg is None:
        raise NilParameterValueError(name, scope, "arg", name)
    if argl is None:
        raise NilParameterValueError(name, scope, "length", name)
    result = GetParamValue(params, "arg")[0:argl]
    scope.SetReturnValue(result, VariableTypes.STRING)



def StrMid(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of mid function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    arg = GetParamValue(params, "arg")
    args = GetParamValue(params, "start")
    argl = GetParamValue(params, "length")
    if arg is None:
        raise NilParameterValueError(name, scope, "arg", name)
    if args is None:
        raise NilParameterValueError(name, scope, "start", name)
    if argl is None:
        raise NilParameterValueError(name, scope, "length", name)

    value = GetParamValue(params, "arg")
    start = GetParamValue(params, "start")
    length = GetParamValue(params, "length")
    endpos = start+length-1

    result = value[start:endpos]
    scope.SetReturnValue(result, VariableTypes.STRING);



def ToString(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of ToString function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    argvalue = GetParamValue(params, "arg")
    result = f"{argvalue}"
    scope.SetReturnValue(result, VariableTypes.STRING);



def StrFormat(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of StrFormat function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    result = GetParamValue(params, "format").format(GetParamValue(params, "arg"))
    scope.SetReturnValue(result, VariableTypes.STRING);



def StrReplace(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of StrReplace function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    var = GetParamValue(params, "var")
    if var is None:
       raise NilParameterValueError(name, scope, "var", name) 
    frm = GetParamValue(params, "frm")
    if frm is None:
       raise NilParameterValueError(name, scope, "frm", name) 
    result = var.replace(frm, GetParamValue(params, "with"))
    scope.SetReturnValue(result, VariableTypes.STRING);



def StartsWith(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of StartsWith function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    haystack = GetParamValue(params, "haystack")
    needle = GetParamValue(params, "needle")
    if haystack is None:
       raise NilParameterValueError(name, scope, "haystack", name) 
    if needle is None:
       raise NilParameterValueError(name, scope, "needle", name) 
    scope.SetReturnValue(str.startswith(haystack, needle), VariableTypes.BOOL)



def RemoveNonAscii(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of RemoveNonAscii function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    txt = GetParamValue(params, "text")
    if txt is None:
       raise NilParameterValueError(name, scope, "text", name) 
    result = unidecode(txt)
    scope.SetReturnValue(result, STRING)



def ReplaceEx(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of ReplaceEx function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    var  = GetParamValue(params, "var")
    repl = GetParamValue(params, "repl")
    by   = GetParamValue(params, "by")
    if var is None:
       raise NilParameterValueError(name, scope, "var", name) 
    if repl is None:
       raise NilParameterValueError(name, scope, "repl", name) 
    result = var
    for ch in repl:
        result = result.replace(ch, by)
    scope.SetReturnValue(result, VariableTypes.STRING)



def PadLeft(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of ReplaceEx function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    string = GetParamValue(params, "string")
    char   = GetParamValue(params, "char")
    amount = GetParamValue(params, "amount")
    if string is None:
       raise NilParameterValueError(name, scope, "string", name) 
    if char is None:
       raise NilParameterValueError(name, scope, "char", name) 
    if amount is None:
       raise NilParameterValueError(name, scope, "amount", name) 
    result = string.rjust(amount, char) # this is counter intuitive, but the *just functions in python pad the character on the other end as what their name would imply.
    scope.SetReturnValue(result, VariableTypes.STRING)



def PadRight(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of ReplaceEx function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    string = GetParamValue(params, "string")
    char   = GetParamValue(params, "char")
    amount = GetParamValue(params, "amount")
    if string is None:
       raise NilParameterValueError(name, scope, "string", name) 
    if char is None:
       raise NilParameterValueError(name, scope, "char", name) 
    if amount is None:
       raise NilParameterValueError(name, scope, "amount", name) 
    result = string.ljust(amount, char) # this is counter intuitive, but the *just functions in python pad the character on the other end as what their name would imply.
    scope.SetReturnValue(result, VariableTypes.STRING)
