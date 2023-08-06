# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Implementation for AST foreach node used and returned by the parser, separate because it requires importing expr"""

from .macal_astnode import AstNode
from .macal_parsernodes import ast_Block
from .macal_parsernodetypes import ParserNodeTypes

class ast_Foreach(AstNode):
    """AST Node: ForEach"""
    def __init__(self, lex_token, expression, block: ast_Block):
        """Initializes foreach node type"""
        super().__init__(ParserNodeTypes.FOREACH, lex_token)
        self.expr = expression
        self.block = block
        self.iterator_var = None

    def __str__(self):
        return f" FOREACH {self.expr} {self.block}"
