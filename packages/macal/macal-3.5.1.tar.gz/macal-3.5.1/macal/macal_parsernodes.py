# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Implementations for AST nodes used and returned by the parser"""

from .macal_parsernodetypes import ParserNodeTypes
from .macal_astnode import AstNode
from .macal_lextoken import LexToken



class ast_Block(AstNode):
    """Node for a block of instructions can contain 0 or more instructions."""
    def __init__(self, lex_token):
        """Initializes block node type"""
        super().__init__(ParserNodeTypes.BLOCK, lex_token)
        self.closelex_token = None
        self.instruction_list = []



    def close(self, lex_token):
        """closes the node"""
        self.closelex_token = lex_token



    def add_instruction(self, instruction):
        """Adds an instruction to the list of instructions"""
        self.instruction_list.append(instruction)



    def count(self):
        """Returns the number of instructions in the list."""
        return len(self.instruction_list)



    def is_root(self):
        """Returns true if this is the root block, false if it is not."""
        return self.token is None



    def __str__(self):
        block = "{\n"
        for instr in self.instruction_list:
            block = f"{block}{instr}\n"
        return f"{block}}}"



class ast_list_Index(AstNode):
    """AST Node: Index"""
    def __init__(self, lex_token, expression, closelex_token):
        """Initializes index node type"""
        super().__init__(ParserNodeTypes.INDEX, lex_token)
        self.expr = expression
        self.closelex_token = closelex_token

    def __str__(self):
        return f"[{self.expr}]"



class ast_function_Param_list(AstNode):
    """AST Node: Parameter list"""
    def __init__(self, lex_token: LexToken):
        """Initializes parameter list node type"""
        super().__init__(ParserNodeTypes.PARAMS, lex_token)
        self.closelex_token = None
        self.params = []



    def close(self, lex_token: LexToken):
        """closes the node"""
        self.closelex_token = lex_token



    def add_parameter(self, expression):
        """adds a parameter to the list"""
        self.params.append(expression)


        
    def count(self):
        """returns the number of parameters on the list"""
        return len(self.params)



    def __str__(self):
        result = "("
        i = 0
        if len(self.params) > 0:
            i = 2
        for expr in self.params:
            result = f"{result}{expr}, "
        return f"{result[:(len(result)-i)]})"



class ast_Break(AstNode):
    """AST Node: Break"""
    def __init__(self, lex_token):
        """Initializes break node type"""
        super().__init__(ParserNodeTypes.BREAK, lex_token)


    
    def __str__(self):
        return f" BREAK;"



class ast_Halt(AstNode):
    """AST Node: Halt"""
    def __init__(self, lex_token, expression):
        """Initializes halt node type"""
        super().__init__(ParserNodeTypes.HALT, lex_token)
        self.expr = expression



    def __str__(self):
        return f" HALT {self.expr};"



class ast_Continue(AstNode):
    """AST Node: Continue"""
    def __init__(self, lex_token):
        """Initializes break node type"""
        super().__init__(ParserNodeTypes.CONTINUE, lex_token)


    
    def __str__(self):
        return f" Continue;"



class ast_Return(AstNode):
    """AST Node: Return"""
    def __init__(self, lex_token, expression):
        """Initializes return node type"""
        super().__init__(ParserNodeTypes.RETURN, lex_token)
        self.expr = expression



    def __str__(self):
        return f" RETURN {self.expr};"
