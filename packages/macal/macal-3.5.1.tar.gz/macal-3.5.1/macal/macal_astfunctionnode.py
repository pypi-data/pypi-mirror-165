# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Implementation for AST Function node used and returned by the parser"""

from .macal_astnode import AstNode
from .macal_parsernodes import ast_Block, ast_function_Param_list
from .macal_variable_types import VariableTypes
from .macal_astvariablenode import ast_Variable
from .macal_lextoken import LexToken

class ast_Function_definition(AstNode):
    """AST Node: Function"""
    def __init__(self, tid: ast_Variable, opLex: LexToken, params: ast_function_Param_list,
                 block: ast_Block):
        """Initializes function definition node type"""
        super().__init__(VariableTypes.FUNCTION, tid.token)
        self.operand = opLex
        self.ident = tid
        self.params = params
        self.block = block
        self.is_extern = False
        self.call_extern = None



    def count(self):
        """returns the number of parameters in the list"""
        return self.params.count()



    def __str__(self):
        return f"FUNCTION {self.token.token_value} => {self.params} {self.is_extern} {self.call_extern} \n{self.block}"
