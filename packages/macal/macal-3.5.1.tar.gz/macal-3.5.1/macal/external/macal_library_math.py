#
# Filename:       | macal_library_math.py
# Author:         | Marco Caspers
# Version:        | 3.5.1
# Description:    |
#
#
# Macal Math Library
#


from macal.macal_library_external import *
from math import floor, ceil, cos, acos, sin, asin, tan, atan, pow, sqrt, log, log2, log10, exp, expm1



def math_round(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    arg = GetParamValue(params, "arg")
    if arg is None:
        raise NilParameterValueError(name, scope, "arg", name)

    if len(params) == 2:
    	digits = GetParamValue(params, 'digits')
    	scope.SetReturnValue(round(arg, digits), VariableTypes.FLOAT)
    else:
    	scope.SetReturnValue(round(arg), VariableTypes.INT)



def math_floor(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    arg = GetParamValue(params, "arg")
    if arg is None:
        raise NilParameterValueError(name, scope, "arg", name)
    scope.SetReturnValue(floor(arg), VariableTypes.INT)



def math_ceil(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    arg = GetParamValue(params, "arg")
    if arg is None:
        raise NilParameterValueError(name, scope, "arg", name)
    scope.SetReturnValue(ceil(arg), VariableTypes.INT)



def math_cos(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(cos(x), VariableTypes.FLOAT)



def math_acos(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(acos(x), VariableTypes.FLOAT)



def math_sin(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(sin(x), VariableTypes.FLOAT)



def math_asin(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(asin(x), VariableTypes.FLOAT)



def math_tan(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(tan(x), VariableTypes.FLOAT)



def math_atan(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(atan(x), VariableTypes.FLOAT)



def math_pow(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    y = GetParamValue(params, "y")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    if y is None:
        raise NilParameterValueError(name, scope, "y", name)
    scope.SetReturnValue(pow(x, y), VariableTypes.FLOAT)



def math_sqrt(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    t = GetParamType(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(sqrt(x), t)



def math_log(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    t = GetParamType(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(log(x), t)



def math_log2(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    t = GetParamType(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(log2(x), t)



def math_log10(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    t = GetParamType(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(log10(x), t)



def math_exp(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    t = GetParamType(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(exp(x), t)



def math_expm1(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    
    x = GetParamValue(params, "x")
    t = GetParamType(params, "x")
    if x is None:
        raise NilParameterValueError(name, scope, "x", name)
    scope.SetReturnValue(expm1(x), t)
