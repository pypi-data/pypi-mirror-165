#
# Filename:       | macal_library_csv.py
# Author:         | Marco Caspers
# Version:        | 3.5.0
# Description:    |
#
#
# Macal 2.0 CSV Library
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.5.0 16-05-2022: detached from class MacalLibrary and now implemented through include csv.mcl with "external" hooks to this module.
#

"""CSV library implementation"""

from macal.macal_library_external import *

def HeadersToCsv(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of HeadersToCsv function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    rec = GetParamValue(params, "rec")
    result = None
    try:
        separator = '","'
        result = f'"{separator.join(rec)}"'
    except Exception as e:
        raise RuntimeError(e)
    scope.SetReturnValue(result, VariableTypes.STRING)



def ValuesToCsv(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of ValuesToCsv function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    rec = GetParamValue(params, "rec")
    result = None
    try:
        temp = []
        for fld in rec:
            temp.append(f'"{rec[fld]}"')
        separator = ','
        result = separator.join(temp)
    except Exception as e:
        raise RuntimeError(e)
    scope.SetReturnValue(result, VariableTypes.STRING)



def ArrayToCsv(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of ArrayToCsv function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    arr = GetParamValue(params, "arr")
    try:
        temp = []
        for fld in arr:
            temp.append(f'"{fld}"')
        separator = ','
        result = separator.join(temp)
    except Exception as e:
        raise RuntimeError(e)
    scope.SetReturnValue(result, VariableTypes.STRING)
