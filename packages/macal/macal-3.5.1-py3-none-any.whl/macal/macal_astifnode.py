# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Implementation for AST if node used and returned by the parser, separate because it requires importing expr"""

from .macal_parsernodetypes import ParserNodeTypes
from .macal_astnode import AstNode
from .macal_parsernodes import ast_Block

class ast_Elif_branch(AstNode):
    """AST Node: ElIf"""
    def __init__(self, lex_token, condition, block: ast_Block):
        """Initializes ElIf node type"""
        super().__init__(ParserNodeTypes.ELIF, lex_token)
        self.condition = condition
        self.block = block



    def __str__(self):
        return f" elif {self.condition} {self.block}"



class ast_Else_branch(AstNode):
    """AST Node: Else"""
    def __init__(self, lex_token, block: ast_Block):
        """Initializes else node type"""
        super().__init__(ParserNodeTypes.ELSE, lex_token)
        self.block = block



    def __str__(self):
        return f" else {self.block}"



class ast_If(AstNode):
    """AST Node: If"""
    def __init__(self, lex_token, condition, block: ast_Block):
        """Initializes if node type"""
        super().__init__(ParserNodeTypes.IF, lex_token)
        self.condition = condition
        self.block = block
        self.elif_branch = []
        self.else_branch = None



    def add_elif(self, branch: ast_Elif_branch):
        """adds elif branch to the list"""
        self.elif_branch.append(branch)



    def add_else(self, branch: ast_Else_branch):
        """add else branch"""
        self.else_branch = branch



    def has_elif(self):
        """returns true if there are elif nodes."""
        return len(self.elif_branch) > 0



    def has_else(self):
        """returns true if there is an else statement."""
        return self.else_branch is not None



    def __str__(self):
        result = f" if {self.condition} {self.block}"
        if self.has_elif():
            for branch in self.elif_branch:
                result = f"{result}{branch}"
        if self.has_else():
            result = f"{result}{self.else_branch}"
        return result
