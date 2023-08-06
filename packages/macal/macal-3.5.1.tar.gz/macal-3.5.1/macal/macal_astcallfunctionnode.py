# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Implementation for AST Call Function node used and returned by the parser"""

from .macal_astnode import AstNode
from .macal_parsernodes import ast_function_Param_list
from .macal_parsernodetypes import ParserNodeTypes
from .macal_astvariablenode import ast_Variable

class ast_Call_function(AstNode):
    """AST Node: Call"""
    def __init__(self, tid: ast_Variable, params: ast_function_Param_list):
        """Initializes function call node type"""
        super().__init__(ParserNodeTypes.CALL, tid.token)
        self.ident = tid
        self.params = params

    def count(self):
        """returns the number of parameters in the list"""
        return self.params.count()

    def __str__(self):
        return f" CALL {self.token.token_value}{self.params}"