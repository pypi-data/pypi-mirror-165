# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Implementation for AST Include command node used and returned by the parser"""

from .macal_astnode import AstNode
from .macal_parsernodetypes import ParserNodeTypes



class ast_Include(AstNode):
    """AST Node: Include"""
    def __init__(self, lex_token, params: list):
        """Initializes function call node type"""
        super().__init__(ParserNodeTypes.INCLUDE, lex_token)
        self.params = params

    def __str__(self):
        result = " INCLUDE "
        first = True
        for token in self.params:
            if first:
                result = f"{result}{token.token_value}"
                first = False
            else:
                result = f"{result},{token.token_value}"
        return result