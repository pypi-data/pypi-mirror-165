# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""library development imports module"""

from .macal_interpreterconsts import FuncArg
from .macal_scope             import MacalScope
from .macal_function          import MacalFunction
from .macal_exceptions        import RuntimeError, NilParameterValueError
from .macal_parsernodetypes   import ParserNodeTypes
from .macal_variable_types    import VariableTypes
from .macal_variable          import MacalVariable



__all__ = ['FuncArg', 'MacalScope', 'MacalFunction', 'ParserNodeTypes', 'VariableTypes', 'RuntimeError', 
    'ParamToString', 'ParamByName', 'GetParamType', 'ValidateFunction', 'ValidateParams', 
    'GetParamValue', 'GetVariableFromParam', 'GetIndexedVariableValue', 'MacalVariable',
   'NilParameterValueError']



def ParamToString(param: MacalVariable) -> str:
    """
        Gets value from param and returns it as a string.
        Ensures that boolean values are shown in lower case.
        It also ensures that nil/None show up as 'nil' as the Python print statement would print "None" which we don't want to see.
        This is purely intended for displaying the value only.
    """
    value = param.get_value()
    if value is True:
        value = 'true'
    elif value is False:
        value = 'false'
    elif param.get_type() == VariableTypes.NIL:
        value = 'nil'
    elif value is None:
        value = 'nil'
    elif param.get_type() == VariableTypes.PARAMS:
        value = [v.get_value() for v in value]
    return str(value)



def ParamByName(lst: list, name: str):
    """Retrieves the parameter from the list based on its name"""
    return next((x for x in lst if x.name == name), None)



def ValidateFunction(name: str, fn: MacalFunction, scope: MacalScope):
    """Validate if the function is indeed the one called and raises an exception if not."""
    if name != fn.name:
        raise RuntimeError(f"Invalid function call: {name}, expected {fn} {scope.name}.");
    return True



def _MissingParameter(name: str, param: str, func: MacalFunction, scope: MacalScope):
    if scope is None:
        raise RuntimeError(f"{name}: Function ({func.name}) parameter missing: {param}.")
    else:
        raise RuntimeError(f"{name}: Function ({func.name}) parameter missing: {param}. ({scope.name})")



def ValidateParams(name: str, params: list, scope: MacalScope, func: MacalFunction, allow_literal: bool = False):
    """Validate if all the parameters that where passed are correct."""
    funcparams = func.args
    if len(params) != len(funcparams.params):
        raise RuntimeError(f"{name}: Invalid number of parameters provided: {len(params)}, required: {len(funcparams.params)}. ({scope.name})")
    for funcparam in funcparams.params:
        param = ParamByName(params, funcparam.token.token_value)
        if param is None:
            _MissingParameter(name, funcparam.token.token_value, func, scope)
        pt = param.get_type()
        if  (allow_literal == False
            and pt != funcparam.token.token_type
            and funcparam.token.token_type != VariableTypes.ANY
            and funcparam.token.token_type != VariableTypes.PARAMS
            and funcparam.token.token_type != ParserNodeTypes.VARIABLE
            and pt != VariableTypes.ANY):
            raise RuntimeError(f"{name}: Invalid parameter ({funcparam.token.token_value}) type: {pt}, required: {funcparam.token.token_type}. ({scope.name})")
    return True



def GetParamValue(params: list, name: str):
    """Get the value from a parameter in the params list."""
    param = ParamByName(params, name)
    if param is None:
        raise _MissingParameter("", name, "", None)
    value = param.get_value()
    return value



def GetParamType(params: list, name: str):
    """Get the value from a parameter in the params list."""
    param = ParamByName(params, name)
    if param is None:
        raise _MissingParameter("", name, "", None)
    value = param.get_type()
    return value



def GetVariableFromParam(params: list, scope: MacalScope, name: str):
    """Get a scope variable from a parameter on the parameters list."""
    pv = GetParamValue(params, name)
    # getting a variable from a function call parameter needs to find it outside the scope itself.
    var = scope.find_variable_outside(pv.name)
    if var is None:
        var = scope.find_function(pv.name)
    if var is None:
        raise RuntimeError(f"Variable not found: {pv.name}. ({scope.name})")
    return var, pv.index



def GetIndexedVariableValue(var, index):
    """Get the value of a variable that has one or more indexes. (e.g.: var[index][index2]..."""
    value = var.get_value()
    for idx in index:
        value = value[idx.value]
    return value
