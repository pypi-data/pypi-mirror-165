# Filename:       | macal_library_system.py
# Author:         | Marco Caspers
# Version:        | 3.5
# Description:
#
# Macal System Library
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.5.0 14-05-2022: detached from class MacalLibrary and now implemented through include system.mcl with "external" hooks to this module.
#

"""System library implementation"""

from macal.macal_library_external import *
import platform

from macal.__about__ import __version__, __author__, __credits__



def console(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of console function"""
    ValidateFunction(name, func, scope)
    out_str = ""
    # Since the param is type PARAMS we can have any number of arguments passed into us as an array.
    param_list = params[0].get_value()
    if len(param_list) > 0:
        if param_list[0].format:
            console_fmt(param_list)
            return
        for param in param_list:
            out_str = f"{out_str}{ParamToString(param)}"
        print(out_str)
    else:
        print()

def console_fmt(args):
    """Console string formatting function"""
    fmt  = args[0].get_value()
    args = args[1:]
    arg_count = len(args)
    fmt_count = fmt.count("{}")
    if arg_count != fmt_count:
        raise RuntimeError("Console(args): Number of arguments ({}) mismatch with format string ({})".format(arg_count, fmt_count))
    argv = []
    for arg in args:
        argv.append(ParamToString(arg))
    print(fmt.format(*argv))



def record_has_field(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    fieldname = GetParamValue(params, "fieldname")
    record = GetParamValue(params, "rec")
    result =  fieldname in record
    scope.SetReturnValue(result, VariableTypes.BOOL)



def Type(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type()
    scope.SetReturnValue(result, VariableTypes.STRING)



def IsString(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.STRING
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsInt(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.INT
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsFloat(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.FLOAT
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsBool(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.BOOL
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsRecord(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.RECORD
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsArray(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.ARRAY
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsAny(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.ANY
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsParams(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.PARAMS
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsFunction(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.FUNCTION
    scope.SetReturnValue(result, VariableTypes.BOOL)



def IsNil(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        result = MacalScope.get_value_type(GetIndexedVariableValue(var, index))
    else:
        result = var.get_type() == VariableTypes.NIL
    scope.SetReturnValue(result, VariableTypes.BOOL)



def create_list(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of create_list function"""
    ValidateFunction(name, func, scope)
    result = []
    param_list = params[0].get_value()
    if len(param_list) > 0:
        for param in param_list:
            result.append(param.get_value())
    else:
        raise RuntimeError("List requires at least one argument.")
    scope.SetReturnValue(result, VariableTypes.ARRAY)



def GetPlatform(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of platform function"""
    ValidateFunction(name, func, scope)
    scope.SetReturnValue(platform.system(), VariableTypes.STRING)


        
def ShowVersion(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of ShowVersion function"""
    ValidateFunction(name, func, scope)
    print("Version: ",__version__)
    print("Author:  ", __author__)
    print("Credits:")
    print(__credits__)



def Items(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Items function used in conjunction with foreach for iterating over records.  Items returns key/value pairs."""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict):
        raise RuntimeError("Items requires a record as argument.")
    pv = [{key: value} for key, value in value.items()]
    scope.SetReturnValue(pv,VariableTypes.ARRAY)



def RecordKeyValue(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Key function used in conjunction the Items function that returns key/value pairs. Key returns the key part of a key value pair."""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict) or len(value) > 1:
        raise RuntimeError("Key requires a key/value pair that is returned when doing a foreach over items(x).")
    for k, v in value.items(): #there are different ways, but this is by far the most simple and safe way to do it.
        key = k
    scope.SetReturnValue(key,VariableTypes.STRING)



def RecordKeys(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Key function used in conjunction the Items function that returns key/value pairs. Key returns the key part of a key value pair."""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict):
        raise RuntimeError("Keys requires a record as input.")
    val = [k for k in value.keys()]
    scope.SetReturnValue(val,VariableTypes.ARRAY)

    

def RecordItemValue(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Value function used in conjunction the Items function that returns key/value pairs. Value returns the value part of a key value pair."""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict) or len(value) > 1:
        raise RuntimeError("Value requires a key/value pair that is returned when doing a foreach over items(x).")
    for k, v in value.items(): #there are different ways, but this is by far the most simple and safe way to do it.
        val = v
    scope.SetReturnValue(val,VariableTypes.STRING)



def RecordValues(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Value function used in conjunction the Items function that returns key/value pairs. Value returns the value part of a key value pair."""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        value = GetIndexedVariableValue(var, index)
    else:
        value = var.get_value()
    if not isinstance(value, dict):
        raise RuntimeError("Values requires a record as input.")
    val = [v for v in value.values()]
    scope.SetReturnValue(val,VariableTypes.ARRAY)



def GetVariableValue(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        vv = GetIndexedVariableValue(var, index)
    else:
        vv = var.get_value()
    if isinstance(vv, MacalVariable):
        finalvar = scope.find_variable_outside(vv.name)
        fvv = finalvar.get_value()
        fvt = finalvar.get_type()
        scope.SetReturnValue(fvv, fvt)
    else:
        raise RuntimeError("Invalid use of getValue. GetValue can only be used inside a function on an argument marked as variable.")



def GetVariableType(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of record_has_field function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func)
    var, index = GetVariableFromParam(params, scope, "var")
    if len(index) > 0:
        vv = GetIndexedVariableValue(var, index)
    else:
        vv = var.get_value()
    if isinstance(vv, MacalVariable):
        finalvar = scope.find_variable_outside(vv.name)
        fvt = finalvar.get_type()
        scope.SetReturnValue(fvt, VariableTypes.STRING)
    else:
        raise RuntimeError("Invalid use of getValue. GetValue can only be used inside a function on an argument marked as variable.")
