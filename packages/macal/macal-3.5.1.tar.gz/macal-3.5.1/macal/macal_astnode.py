# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Base class AstNode used as a base for various ast node types."""

from .macal_lextoken import LexToken

class AstNode:
    """node ancestor for all other node types"""
    def __init__(self, node_type: str, lex_token: LexToken):
        """Base AST node, all other node types inherit this one."""
        self.type : str = node_type
        self.token : LexToken = lex_token

    def name(self):
        """returns token name"""
        return self.token.token_value

    def node_type(self):
        """returns node type"""
        return self.type
