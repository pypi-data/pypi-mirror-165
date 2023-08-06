# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Implementation for AST external node used and returned by the parser"""

from .macal_parsernodetypes import ParserNodeTypes
from .macal_astnode import AstNode

class ast_External(AstNode):
    """AST Node: external"""
    def __init__(self, lex_token, modulename: str, functionname: str):
        """Initializes external node type"""
        super().__init__(ParserNodeTypes.EXTERNAL, lex_token)
        self.modulename = modulename
        self.functionname = functionname

    def __str__(self):
        return f" external {self.modulename}, {self.functionname};"