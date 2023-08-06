# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Base class for macal Library"""

from .macal_lextoken import LexToken
from .macal_lextokentype import LexTokenTypes
from .macal_variable_types import VariableTypes
from .macal_parsernodes import ast_Block, ast_function_Param_list
from .macal_astvariablenode import ast_Variable
from .macal_function import MacalFunction
from .macal_scope import MacalScope
from .macal_exceptions import RuntimeError
from .macal_variable import MacalVariable
from .macal_keywords import NIL

from deprecated import deprecated

from .__about__ import __version__

def _MissingParameter(name, param, func, scope):
    if scope is None:
        raise RuntimeError(f"{name}: Function ({func.name}) parameter missing: {param}.")
    else:
        raise RuntimeError(f"{name}: Function ({func.name}) parameter missing: {param}. ({scope.name})")

@deprecated("This class is obsolete, use the new style through includes and library_external.")
class MacalLibrary:
    """Base class for Libraries, this is now OBSOLETE"""
    def __init__(self, name):
        self.name : str = name
        self.functions : list = []
        self.variables : list = []
        self.version : str = __version__



    def CreateArg(self, name: str, param_type: str):
        """Create a new parameter for the function"""
        return ast_Variable(LexToken(param_type, name, -1, -1, -1))



    def RegisterFunction(self, name: str, args: list, call_func):
        """Register a new function with the library."""
        prms = ast_function_Param_list(LexToken(LexTokenTypes.LParen, '(', -1, -1, -1))
        for arg in args:
            prms.params.append(self.CreateArg(arg.arg_name, arg.arg_type))
        fun = MacalFunction(name, prms, ast_Block(None))
        fun.is_extern = True
        fun.call_extern = call_func
        self.functions.append(fun)



    def variable_by_name(self, name: str) -> MacalVariable:
        """
            Returns a variable from the local variable list by its name.
            ToDo: Variables and functions need to be in a local scope for the library.
        """
        return next((x for x in self.variables if x.name == name), None)



    def RegisterVariable(self, name: str, value, constant = False):
        """
            Adds a new variable to the list.
            Validates if variable exists or not. If it exists a runtime error is raised.
        """
        var = self.variable_by_name(name)
        if var is not None:
            raise RuntimeError(f"Invalid register variable ({name}), variable already exists.")
        var = MacalVariable(name)
        var.set_value(value)
        var.set_type(MacalScope.get_value_type(value))
        var.constant = constant
        self.variables.append(var)



    def ValidateFunction(self, name: str, fn: MacalFunction, scope: MacalScope):
        """Validate if the function exists."""
        if name != fn.name:
            raise RuntimeError(f"Invalid function call: {name}, expected {fn} {scope.name}.");
        return True



    def ParamByName(self, lst: list, name: str):
        """Retrieves an item from the list based on its name"""
        return next((x for x in lst if x.name == name), None)



    def ValidateParams(self, name: str, params: list, scope: MacalScope, func: MacalFunction):
        """Validate if all the parameters that where passed are correct."""
        funcparams = func.args
        if len(params) != len(funcparams.params):
            raise RuntimeError(f"{name}: Invalid number of parameters provided: {len(params)}, required: {len(funcparams.params)}. ({scope.name})")
        for funcparam in funcparams.params:
            param = self.ParamByName(params, funcparam.token.token_value)
            if param is None:
                _MissingParameter(name, funcparam.token.token_value, func, scope)
            pt = param.get_type()
            if pt != funcparam.token.token_type and funcparam.token.token_type != VariableTypes.ANY and funcparam.token.token_type != VariableTypes.PARAMS and pt != VariableTypes.ANY:
                raise RuntimeError(f"{name}: Invalid parameter ({funcparam.token.token_value}) type: {pt}, required: {funcparam.token.token_type}. ({scope.name})")
        return True



    def GetParamValue(self, params: list, name: str):
        """Get the value from a parameter in the params list."""
        param = self.ParamByName(params, name)
        if param is None:
            raise _MissingParameter("", name, "", None)
        value = param.get_value()
        return value



    def GetVariableFromParam(self, params: list, scope: MacalScope, name: str):
        """Get a scope variable from a parameter on the parameters list."""
        pv = self.GetParamValue(params, name)
        var = scope.find_variable(pv.name)
        if var is None:
            raise RuntimeError(f"Variable not found: {pv.name}. ({scope.name})")
        return var, pv.index



    def GetIndexedVariableValue(self, var, index):
        value = var.get_value()
        for idx in index:
            value = value[idx.value]
        return value



    def GetFunction(self, name: str):
        """
            Returns a function from the local functions list by its name.
            ToDo: Variables and functions need to be in a local scope for the library.
        """
        return next((x for x in self.functions if x.name == name), None)



    @staticmethod
    def ParamToString(param) -> str:
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
        elif param.get_type() == NIL:
            value = 'nil'
        elif value is None:
            value = 'nil'
        return str(value)


