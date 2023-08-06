# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Implementation for AST Assign node used and returned by the parser"""

from .macal_astnode import AstNode
from .macal_parsernodetypes import ParserNodeTypes
from .macal_astvariablenode import ast_Variable

class ast_Assign(AstNode):
    """AST Node: Assign"""
    def __init__(self, operand, tid: ast_Variable, expression):
        """Initializes assign node type"""
        super().__init__(ParserNodeTypes.ASSIGN, tid.token)
        self.operand = operand
        self.ident = tid
        self.expr = expression
        self.ref = False
        self.ref_token = None

    def __str__(self):
        return f""" {"REF " if self.ref is True else ""}{self.ident} {self.operand.token_value} {self.expr}"""
