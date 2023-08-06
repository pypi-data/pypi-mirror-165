# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""macal Language parser implementation"""

from .macal_lextoken import SelectParam
from .macal_lextokentype import LexTokenTypes
from .macal_lextokentypes import NEW_ARRAY_INDEX

from .macal_keywords import (KW_ARRAY, KW_FOREACH, KW_ELIF, KW_ELSE, KW_IF, KW_BREAK, KW_HALT,
                            KW_RETURN, KW_AS, KW_DISTINCT, KW_SELECT, KW_FROM, KW_MERGE, KW_WHERE, 
                            KW_INTO, KW_RECORD, KW_INCLUDE, TRUE, KW_EXTERNAL, KW_PARAMS, KW_ANY,
                            KW_VARIABLE, KW_CONTINUE)

from .macal_variable_types import VariableTypes
from .macal_expr import Expr
from .macal_expritem import ExpressionItem
from .macal_parsernodes import (ast_list_Index, ast_function_Param_list,
                              ast_Block, ast_Halt, ast_Break, ast_Continue, ast_Return)

from .macal_astifnode import ast_If, ast_Elif_branch, ast_Else_branch
from .macal_astselectnode import ast_Select
from .macal_astforeachnode import ast_Foreach
from .macal_astvariablenode import ast_Variable
from .macal_astfunctionnode import ast_Function_definition
from .macal_astcallfunctionnode import ast_Call_function
from .macal_astassignnode import ast_Assign
from .macal_astincludenode import ast_Include
from .macal_astexternalnode import ast_External
from .macal_exceptions import SyntaxError

import sys
import pkg_resources
from pathlib import Path

from .__about__ import __version__

#expression     → literal
#               | unary
#               | binary
#               | grouping ;

#literal        → NUMBER | STRING | "true" | "false" | "nil" ;
#grouping       → "(" expression ")" ;
#unary          → ( "-" | "!" ) expression ;
#binary         → expression operator expression ;
#operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
#               | "+"  | "-"  | "*" | "/" ;

#expression     → equality ;
#equality       → comparison ( ( "!=" | "==" ) comparison )* ;
#comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
#term           → factor ( ( "-" | "+" ) factor )* ;
#factor         → unary ( ( "/" | "*" ) unary )* ;
#unary          → ( "!" | "-" ) unary
#               | primary ;
#primary        → NUMBER | STRING | "true" | "false" | "nil"
#               | "(" expression ")" ;

#Name	        Operators	    Associates
#Equality	    == !=	        Left
#Comparison	    > >= < <=	    Left
#Term	        - +	            Left
#Factor	        / *	            Left
#Unary	        ! -	            Right



class MacalParser:
    """macal Parser class"""
    def __init__(self):
        """Initializes language parser for macal"""
        self.tokens: list = []
        self.length: int = 0
        self.nodes: list = []
        self.pos: int = -1
        self.version: str = __version__
        self.external_folder = '' # folder where the python files for "external" libraries are located.
        self._filename: str = ''



    def reset(self):
        """resets the current state, do not use!
       This is here for the linter only"""
        self.tokens = []
        self.length = 0
        self.nodes = []
        self.pos = -1



    def _peek(self, look_ahead_count=0):
        if self.pos >= 0 and self.pos < self.length - look_ahead_count:
            return self.tokens[self.pos + look_ahead_count]
        return None



    def _pred(self):
        if self.tokens is not None and len(self.tokens) > 0 and self.pos > 0 and self.pos < self.length:
            return self.tokens[self.pos - 1]



    def _chk(self, ttype):
        peek = self._peek()
        if peek is not None and peek.token_type == ttype:
            return True
        return False



    def _check(self, ttype):
        return not self._eof() and self._chk(ttype)



    def _eof(self):
        return self.pos >= self.length



    def _match(self, *args):
        if self._eof():
            return False
        if self._peek().token_type in args:
            self._advance()
            return True
        return False



    def _match_kw(self, *args):
        tkwd = self._peek().token_value
        if tkwd in args:
            self._advance()
            return True
        return False


    
    def _advance(self):
        if not self._eof():
            self.pos += 1
        return self._previous()



    def _previous(self):
        if self.pos > 0:
            return self.tokens[self.pos -1]
        return None



    def _expression(self):
        return self._boolean()



    def _boolean(self):
        expr = self._equality()
        while self._match(LexTokenTypes.OpAnd, LexTokenTypes.OpOr):
            operator = self._previous().token_value
            right = self._equality()
            expr = Expr(self._previous()).binary(expr, operator, right)
        return expr



    def _equality(self):
        expr = self._comparison()
        while self._match(LexTokenTypes.OpNe, LexTokenTypes.OpEqual):
            operator = self._previous().token_value
            right = self._comparison()
            expr = Expr(self._previous()).binary(expr, operator, right)
        return expr



    def _comparison(self):
        expr = self._term()
        while self._match(LexTokenTypes.OpGt, LexTokenTypes.OpGte, LexTokenTypes.OpLt, LexTokenTypes.OpLte):
            operator = self._previous().token_value
            right = self._term()
            expr = Expr(self._previous()).binary(expr, operator, right)
        return expr



    def _term(self):
        expr = self._factor()
        while self._match(LexTokenTypes.OpSub, LexTokenTypes.OpAdd):
            operator = self._previous().token_value
            right = self._factor()
            expr = Expr(self._previous()).binary(expr, operator, right)
        return expr



    def _factor(self):
        expr = self._unary()
        if self._match(LexTokenTypes.OpAssign):
            self._raise_error("Invalid assignment, expected ==");
        while self._match(LexTokenTypes.OpDiv, LexTokenTypes.OpMul):
            operator = self._previous().token_value
            right = self._unary()
            expr = Expr(self._previous()).binary(expr, operator, right)
        return expr



    def _unary(self):
        if self._match(LexTokenTypes.OpNot, LexTokenTypes.OpSub, LexTokenTypes.OpRef, LexTokenTypes.OpFormat):
            operator = self._previous().token_value
            right = self._primary()
            return Expr(self._previous()).unary(operator, right)
        return self._primary()



    def _primary(self):
        result = None
        if self._match(LexTokenTypes.BoolType):
            result = Expr(self._previous()).literal(ExpressionItem(self._previous().token_value == TRUE, VariableTypes.BOOL, self._previous().location))
        elif self._match(LexTokenTypes.StringType):
            result = Expr(self._previous()).literal(ExpressionItem(self._previous().token_value, VariableTypes.STRING, self._previous().location))
        elif self._match(LexTokenTypes.IntType): 
            result = Expr(self._previous()).literal(ExpressionItem(self._previous().token_value, VariableTypes.INT, self._previous().location))
        elif self._match(LexTokenTypes.FloatType):
            result = Expr(self._previous()).literal(ExpressionItem(self._previous().token_value, VariableTypes.FLOAT, self._previous().location))
        elif self._match(LexTokenTypes.NilType):
            result = Expr(self._previous()).literal(ExpressionItem(None, VariableTypes.NIL, self._previous().location))
        elif self._match(LexTokenTypes.Identifier):
            result = self._variable_or_function()
        elif self._match(LexTokenTypes.LParen):
            result = self._grouping()
        elif self._match_kw(KW_ARRAY):
            if self._match(LexTokenTypes.Identifier):
                result = self._variable(self._previous())
                result.token.token_type = VariableTypes.ARRAY
            else:
                result = Expr(self._previous()).literal(ExpressionItem([], VariableTypes.ARRAY, self._previous().location))
        elif self._match_kw(KW_RECORD):
            if self._match(LexTokenTypes.Identifier):
                result = self._variable(self._previous())
                result.token.token_type = VariableTypes.RECORD
            else:
                result = Expr(self._previous()).literal(ExpressionItem({}, VariableTypes.RECORD, self._previous().location))
        elif self._match_kw(KW_PARAMS):
            if self._match(LexTokenTypes.Identifier):
                result = self._variable(self._previous())
                result.token.token_type = VariableTypes.PARAMS
            else:
                self._raise_error("Params needs to be followed by identifier, got: {}".format(self._peek().token_type))
        elif self._match_kw(KW_VARIABLE):
            if self._match(LexTokenTypes.Identifier):
                result = self._variable(self._previous())
                result.token.token_type = VariableTypes.VARIABLE
            else:
                self._raise_error("Variable needs to be followed by identifier, got: {}".format(self._peek().token_type))
        elif self._match_kw(KW_ANY):
            result = self._variable(self._previous())
            result.token.token_type = VariableTypes.ANY
        if result is None:
            self._raise_error(f"unknown token in expression: {self._peek()}")
        return result



    def _variable_or_function(self):
        expr = None
        if self._check(LexTokenTypes.LParen):
            call = ast_Call_function(self._variable(self._previous()), self._param_list())
            expr = Expr(self._previous()).function(call)
        else:
            expr = self._variable(self._previous())
        return expr



    def _grouping(self):
        expr = self._expression()
        self._consume(LexTokenTypes.RParen, "Expect ')' after expression.")
        return Expr(self._previous()).grouping(expr)



    @staticmethod
    def _format_error(token, message, filename):
        if token is None:
            fmt_msg = f"{message}. In ({filename})."
        else:
            fmt_msg = f"{message} {token.location} ({token.token_value}). In ({filename})"
        return fmt_msg



    def _raise_error(self, message):
        raise SyntaxError(self._format_error(self._peek(), message, self._filename))



    def _raise_error_ex(self, message, token):
        raise SyntaxError(self._format_error(token, message, self._filename))



    def _consume(self, ttype, message: str):
        if self._check(ttype):
            validated = self._advance()
            if validated is not None:
                return validated
        self._raise_error(message)
        return None



    def _consume_keyword(self, kwd, message):
        if self._check(LexTokenTypes.Keyword) and self._peek().token_value == kwd:
            return self._advance()
        self._raise_error(message)
        return None

    def _parse_variable_array_index(self, node: ast_Variable):
        while self._check(LexTokenTypes.LIndex):
            index_token = self._advance()
            if self._check(LexTokenTypes.RIndex):
                expr = Expr(self._previous()).literal(ExpressionItem(NEW_ARRAY_INDEX, VariableTypes.ARRAY, self._previous().location))
            else:
                expr = self._expression()
            node.add_index(ast_list_Index(index_token, expr,
                            self._consume(LexTokenTypes.RIndex, "Expected ']'")))



    def _variable(self, tid):
        node = ast_Variable(tid)
        if self._check(LexTokenTypes.LIndex):
            self._parse_variable_array_index(node)
        return node



    def _param_list(self):
        node = ast_function_Param_list(self._consume(LexTokenTypes.LParen, "Expected '(' before parameter list"))
        if self._check(LexTokenTypes.RParen):
            node.close(self._advance())
            return node
        expr = self._expression()
        if expr is None:
            self._raise_error("Expected parameter(expression)")
        node.add_parameter(expr)
        while self._check(LexTokenTypes.Comma):
            self._advance()
            nexpr = self._expression()
            if nexpr is None:
                self._raise_error("Expected parameter(expression)")
            node.add_parameter(nexpr)
        node.close(self._consume(LexTokenTypes.RParen, "Expected ')' after parameter list"))
        return node



    def _parse_function_call(self, tid):
        node = ast_Call_function(tid, self._param_list())
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        return node



    def _check_module_exists(self, filepath, modulename):
        filename = "{}.py".format(modulename)
        check_module_exists = Path(filepath) / filename
        return check_module_exists.is_file()



    def _try_include_from_pkg(self, modulename, functionname):
        filepath = pkg_resources.resource_filename(__name__, 'external')
        if self._check_module_exists(filepath, modulename):
            if filepath not in sys.path:
                sys.path.insert(0, filepath)
            module = __import__(modulename, locals(), globals() , [functionname])
            return module
        else:
            return None



    def _try_include_from_path(self, modulename, functionname):
        filepath = self.external_folder
        if self._check_module_exists(filepath, modulename):
            if filepath not in sys.path:
                sys.path.insert(0, filepath)
            module = __import__(modulename, locals(), globals() , [functionname])
            return module
        else:
            return None



    def _parse_function_definition(self, tid):
        oplex  = self._consume(LexTokenTypes.OpDefine, "Expected '=>'")
        params = self._param_list()
        token = self._peek()
        extern_call = None
        isextern = False
        if token.token_type == LexTokenTypes.Keyword and token.token_value == KW_EXTERNAL:
            block = self._parse_external()
            modulename = block.modulename.token_value
            functionname = block.functionname.token_value
            module = self._try_include_from_pkg(modulename, functionname)
            if module is None:
                module = self._try_include_from_path(modulename, functionname)
            if module is None:
                self._raise_error("Include external module '{}' not found.".format(modulename))            
            if not hasattr(module, functionname):
                self._raise_error("Function name '{}' not found in module '{}'.".format(functionname, modulename))
            extern_call = getattr(module, functionname)
            isextern = True
        else:
            block = self._parse_block()



        node = ast_Function_definition(tid, oplex, params, block)
        node.is_extern = isextern
        node.call_extern = extern_call
        return node




    def _parse_assign(self, tid):
        node = ast_Assign(self._consume(LexTokenTypes.OpAssign, "Expected '='"), tid,  self._expression())
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        return node



    #ToDo: Remove this as we don't need it anymore, it's an artefact of pre-3.0. But we need to rework, lexer, parser and interpreter for this.
    def _parse_assign_ref(self):
        ref = self._consume(LexTokenTypes.OpRef, "Expected '&'")
        tid = self._variable(self._consume(LexTokenTypes.Identifier, "identifier expected in instruction"))
        node = self._parse_assign(tid)
        node.ref = True
        node.ref_token = ref
        return node



    def _parse_block(self):
        node = ast_Block(self._consume(LexTokenTypes.LBracket, "{ expected"))
        while not self._check(LexTokenTypes.RBracket) and not self._eof():
            instr = self._parse_instruction()
            if instr is None:
                self._raise_error("Instruction returned None")
            if instr != LexTokenTypes.Comment:
                node.add_instruction(instr)
        node.close(self._consume(LexTokenTypes.RBracket, "} expected"))
        return node



    def _parse_identifier(self):
        tid = self._variable(self._consume(LexTokenTypes.Identifier, "identifier expected in instruction"))
        result = None
        peek = self._peek()
        if peek.token_type == LexTokenTypes.LParen:
            result = self._parse_function_call(tid)
        elif peek.token_type == LexTokenTypes.OpAssign:
            result = self._parse_assign(tid)
        elif peek.token_type == LexTokenTypes.OpDefine:
            result = self._parse_function_definition(tid)
        if result is None:
            self._raise_error(f"Unexpected token after identifier ({tid.token.token_value}) ")
        return result



    def _parse_instruction(self):
        result = None
        if self._eof():
            return result
        peek = self._peek()
        if peek.token_type == LexTokenTypes.Identifier:
            result = self._parse_identifier()
        elif peek.token_type == LexTokenTypes.OpRef: #todo remove because obsolete.
            result = self._parse_assign_ref()
        elif peek.token_type == LexTokenTypes.LBracket:
            result = self._parse_block()
        elif peek.token_type == LexTokenTypes.Keyword:
            result = self._parse_keyword()
        elif peek.token_type == LexTokenTypes.Comment:
            self._consume(LexTokenTypes.Comment, "") # We skip comments
            result = LexTokenTypes.Comment # still we have to signal our caller we did encounter one.
        if result is None:
            self._raise_error("Unknown character")
        return result



    def _parse_if(self):
        keyword = self._consume_keyword(KW_IF, "Expected 'if'")
        expr = self._expression()
        if expr is None:
            self._raise_error("Expected parameter(expression)")
            return None
        node = ast_If(keyword, expr, self._parse_block())
        while not self._eof() and self._peek().token_value == KW_ELIF:
            kwei = self._advance()
            expr = self._expression()
            if expr is None:
                self._raise_error("Expected parameter(expression)")
                return None
            node.add_elif(ast_Elif_branch(kwei, expr, self._parse_block()))
        if not self._eof() and self._peek().token_value == KW_ELSE:
            node.add_else(ast_Else_branch(self._advance(), self._parse_block()))
        return node



    def _parse_foreach(self):
        keyword = self._consume_keyword(KW_FOREACH, "Expected 'foreach'")
        token = self._peek()
        
        if token is not None and token.token_value == '(':
            self._raise_error_ex("Foreach is not a function, expected a variable", token)

        expr = self._expression()
        if expr is None:
            self._raise_error("Expected parameter(expression)")
        
        node = ast_Foreach(keyword, expr, self._parse_block())
        return node



    def _parse_break(self):
        node = ast_Break(self._consume_keyword(KW_BREAK, "Expected 'break'"))
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        return node



    def _parse_halt(self):
        keyword = self._consume_keyword(KW_HALT, "Expected 'halt'")
        expr = self._expression()
        if expr is None:
            self._raise_error("Expected parameter(expression)")
        node = ast_Halt(keyword, expr)
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        return node



    def _parse_continue(self):
        node = ast_Continue(self._consume_keyword(KW_CONTINUE, "Expected 'continue'"))
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        return node



    def _parse_return(self):
        keyword = self._consume_keyword(KW_RETURN, "Expected 'return'")
        token = self._peek()
        if token is not None and token.token_value == ';':
            node = ast_Return(keyword, None)
        else:
            expr = self._expression()
            if expr is None:
                self._raise_error("Expected parameter(expression)")
            node = ast_Return(keyword, expr)
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        return node



    def _parse_select_param(self):
        token = self._advance()
        astok = None
        asv = None
        if self._peek().token_value == KW_AS:
            astok = self._consume_keyword(KW_AS, "Expected 'as'")
            asv = self._advance()
        return SelectParam(token, astok, asv)



    def _parse_select(self):
        keyword = self._consume_keyword(KW_SELECT, "Expected 'select'")
        distinct = False
        peek = self._peek()
        if peek.token_value == KW_DISTINCT:
            self._advance()# skip distinct kw
            distinct = True
        params = []
        param = self._parse_select_param()
        params.append(param)
        while not self._eof() and self._check(LexTokenTypes.Comma):
            self._advance() # skip ,
            wparam = self._parse_select_param()
            params.append(wparam)
        _ = self._consume_keyword(KW_FROM, "Expected 'from'")
        sfrom = self._expression()
        wheretoken = None
        swhere = None
        if self._peek().token_value == KW_WHERE:
            wheretoken = self._consume_keyword(KW_WHERE, "Expected 'where'")
            swhere = self._expression()
        smerge = False
        if self._peek().token_value == KW_MERGE:
            smerge = True
            self._advance() # skip merge keyword
        _ = self._consume_keyword(KW_INTO, "Expected 'into'")
        sinto = self._expression()
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        node = ast_Select(keyword, params, sfrom, sinto)
        node.set_distinct(distinct)
        node.set_where(wheretoken, swhere)
        node.set_merge(smerge)
        return node



    def _parse_include(self):
        keyword = self._consume_keyword(KW_INCLUDE, "Expected 'include'");
        params = []
        token = self._advance()
        params.append(token)
        while not self._eof() and self._check(LexTokenTypes.Comma):
            self._advance() # skip the comma.
            token = self._advance()
            params.append(token)
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        node = ast_Include(keyword, params)
        return node



    def _expect_string_literal(self):
        token = self._advance()
        if token.token_type != LexTokenTypes.StringType:
            self._raise_error("Expected 'STRING' literal but got '{}'".format(token.token_type))
            return None
        return token



    def _parse_external(self):
        keyword = self._consume_keyword(KW_EXTERNAL, "Expected 'external'");
        paraml = self._expect_string_literal()
        self._consume(LexTokenTypes.Comma, "Expected ','")
        paramr = self._expect_string_literal()
        self._consume(LexTokenTypes.Semicolon, "Expected ';'")
        return ast_External(keyword, paraml, paramr)



    def _parse_keyword(self):
        name = self._peek().token_value
        result = None
        if name == KW_IF:
            result = self._parse_if()
        elif name == KW_FOREACH:
            result = self._parse_foreach()
        elif name == KW_HALT:
            result = self._parse_halt()
        elif name == KW_BREAK:
            result = self._parse_break()
        elif name == KW_CONTINUE:
            result = self._parse_continue()
        elif name == KW_SELECT:
            result = self._parse_select()
        elif name == KW_RETURN:
            result = self._parse_return()
        elif name == KW_INCLUDE:
            result = self._parse_include()
        if result is None:
            self._raise_error("Unknown or invalid use of keyword")
        return result



    def parse(self, tokens, filename) -> ast_Block:
        """Parses the given list of tokens into an AST tree and returns that."""
        self._filename = filename;
        if tokens is None:
            self._raise_error("Unexpected EOF.")
        self.tokens = tokens
        self.length = len(tokens)
        self.pos = 0
        root = ast_Block(None)
        while not self._eof():
            instr = self._parse_instruction()
            if instr != LexTokenTypes.Comment:
                root.add_instruction(instr)
        return root
