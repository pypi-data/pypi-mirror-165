# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Expression class implementation, this class is used by the parser."""

from .macal_lextokentype import LexTokenTypes
from .macal_lextoken     import LexToken
from .macal_exprtypes import ExpressionTypes
from .macal_parsernodetypes import ParserNodeTypes
from .macal_keywords import NIL
from .macal_expritem import ExpressionItem



class Expr:
    """Expression class with static methods to instantiate specific expr node types."""
    def __init__(self, token: LexToken):
        """Base initializer for Expr class"""
        self.expr_type  = None
        self.left       = ExpressionItem(None, NIL)
        self.operator   = None
        self.right      = ExpressionItem(None, NIL)
        self.token      = token



    def set_right(self, value):
        """set right parameter"""
        self.right = value



    def binary(self, left, operator, right):
        """Instantiates Expr node of type binary"""
        instance = self
        instance.expr_type = ExpressionTypes.BINARY
        instance.left = ExpressionItem(left, Expr)
        instance.operator = operator
        instance.right = ExpressionItem(right, Expr)
        return instance



    def unary(self, operator, right):
        """Instantiates Expr node of type unary"""
        instance = self
        instance.expr_type = ExpressionTypes.UNARY
        instance.operator = operator
        instance.right = ExpressionItem(right, Expr)
        return instance
    


    def literal(self, left):
        """Instantiates Expr node of type literal"""
        instance = self
        instance.expr_type = ExpressionTypes.LITERAL
        instance.left = left
        return instance



    def grouping(self, grouping):
        """Instantiates Expr node of type grouping"""
        instance = self
        instance.expr_type = ExpressionTypes.GROUPING
        instance.left = ExpressionItem(grouping, ExpressionTypes.GROUPING)
        return instance
    


    def variable(self, var):
        """Instantiates Expr node of type variable"""
        instance = self
        instance.expr_type = ExpressionTypes.VARIABLE
        instance.left = ExpressionItem(var, ExpressionTypes.VARIABLE)
        return instance



    def index(self, index):
        """Instantiates Expr node of type variableindex"""
        instance = self
        instance.expr_type = ExpressionTypes.INDEX
        instance.left = ExpressionItem(index, ExpressionTypes.INDEX)
        return instance



    def function(self, fun):
        """Instantiates Expr node of type function call"""
        instance = self
        instance.expr_type = ExpressionTypes.FUNCTION
        instance.left = ExpressionItem(fun, ParserNodeTypes.CALL)
        instance.operator = ParserNodeTypes.CALL
        return instance



    def param_list(self):
        """Instantiates Expr node of type parameter list."""
        instance = self
        instance.expr_type = ExpressionTypes.PARAMS
        instance.left = ExpressionItem([], ExpressionTypes.PARAMS)
        return instance
    


    def print(self, expr):
        """Recursive printing function to display the entire expression"""
        if expr is None:
            return ""
        result = ""
        if isinstance(expr, tuple):
            if expr[0] == LexTokenTypes.Identifier:
                result = expr[1]
            else:
                result = "Unknown {}".format(expr[0])
        elif not isinstance(expr, Expr) and expr is not None:
            result = expr.print("")
        elif expr.expr_type == ExpressionTypes.BINARY:
            result = "( {} op: {} {})".format(self.print(expr.left.value),
                                              expr.operator, self.print(expr.right.value))
        elif expr.expr_type == ExpressionTypes.UNARY:
            uop = expr.operator
            uright = expr.right.value
            result = "(unop: {} {})".format(uop, self.print(uright))
        elif expr.expr_type == ExpressionTypes.LITERAL:
            result = repr("literal {}: {}".format(expr.left.item_type, expr.left.value))
        elif expr.expr_type == ExpressionTypes.GROUPING:
            result = "( {} )".format(self.print(expr.left.value))
        elif expr.expr_type == ExpressionTypes.INDEX:
            result = "Index [ {} ]".format(expr.left.value)
        elif expr.expr_type == ExpressionTypes.FUNCTION:
            result =self.print(expr.left.value)
        #elif (expr.expr_type == ExpressionTypes.VARIABLE):
        #    result = expr.print()
        #elif (expr.expr_type == ExpressionTypes.PARAMS):
        #    result = expr.print()
        else:
            result = "Unknown {}".format(expr.expr_type)
        return result



    def __str__(self):
        result = ""
        if self.expr_type is None:
            return result
        if self.expr_type == ExpressionTypes.BINARY:
            result = f"{self.left.value} {self.operator} {self.right.value}"
        elif self.expr_type == ExpressionTypes.UNARY:
            result = f"{self.operator}{self.right.value}"
        elif self.expr_type == ExpressionTypes.LITERAL:
            result = f"{self.left.value} ({self.left.item_type})"
        elif self.expr_type == ExpressionTypes.GROUPING:
            result = f"({self.left.value})"
        elif self.expr_type == ExpressionTypes.INDEX:
            result = f"[{self.left.value}]"
        elif self.expr_type == ExpressionTypes.FUNCTION:
            result = f"{self.left.value}"
        elif self.expr_type == ExpressionTypes.VARIABLE:
            result = f"{self.left.value}"
        else:
            result = f"unhandled expr type {self.expr_type}"
        return result
