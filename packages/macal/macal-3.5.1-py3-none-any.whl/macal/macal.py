#!/usr/bin/python3
# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""macal Main class implementation"""

from .macal_lexer import MacalTokenizer
from .macal_parser import MacalParser
from .macal_interpreter import MacalInterpreter
from .macal_library import MacalLibrary
from .macal_scope import MacalScope

import os
import pathlib
import glob

from .__about__ import __version__

import pkg_resources

from .macal_exceptions import RuntimeError

class Macal:
    """macal Language"""
    def __init__(self):
        """Initializes macal Language class"""
        self.lexer       = MacalTokenizer()
        self.parser      = MacalParser()
        self.interpreter = MacalInterpreter()
        self.source      = None
        self.tokens      = None
        self.ast_tree    = None
        self.debug       = False
        self.print_tokens= False
        self.print_tree  = False
        self.print_scope = False
        self.scope       = self.interpreter.scope
        self.Libraries:  list = []
        self.scope.Libraries = self.Libraries
        self.interpreter.IncludeRunner = self.run_include
        self.include_folder = 'libraries' # folder where include (libraries) are located.
        self.external_folder = 'external' # folder where include should look for external modules.
        self.version = __version__



    def run_from_file(self, filename, **kwargs):
        """Runs the language using a file as input"""
        if not filename:
            raise RuntimeError("Invalid null argument: filename.")
        try:
            with open (filename, mode = 'r', encoding = 'utf-8') as text_file:
                source = text_file.read()
            return self.run_from_string(source, pathlib.Path(filename).stem, **kwargs)
        except FileNotFoundError:
            raise RuntimeError("File not found: {}".format(filename))



    def register_library(self, lib: MacalLibrary):
        self.Libraries.append(lib)



    def register_variable(self, name: str, value, vartype):
        var = self.interpreter.scope.add_new_variable(name)
        var.set_value(value)
        var.set_type(vartype)
        return var



    def run_from_string(self, source, filename, **kwargs):
        """Runs the language using a string as input"""
        for name, value in kwargs.items():
        	self.register_variable(name, value, MacalScope.get_value_type(value))
        self.source = source
        self.tokens   = self.lexer.lex(self.source, filename)
        if self.debug and self.print_tokens:
            print("Tokens:")
            for token in self.tokens:
                print(token)
            print()
        self.parser.external_folder = self.external_folder
        self.ast_tree = self.parser.parse(self.tokens, filename)
        if self.debug and self.print_tree:
            print(self.ast_tree)
            print()
        result = self.interpreter.interpret(self.ast_tree, filename)
        if self.debug and self.print_scope:
            self.interpreter.scope.print(self.interpreter.scope)
            print()
        return result



    def versions(self):
        """Returns the versions of all individual modules that make up the language."""
        vstr = "Macal version:       {}\r\n".format(__version__)
        vstr = "{}Tokenizer version:   {}\r\n".format(vstr, self.lexer.version)
        vstr = "{}Parser version:      {}\r\n".format(vstr, self.parser.version)
        vstr = "{}interpreter version: {}\r\n\r\n".format(vstr, self.interpreter.version)
        return vstr



    def build_include_list(self):
        return [pathlib.Path(f).stem for f in glob.glob(join(self.include_folder,"*.mcl"))]



    def _try_include_from_pkg(self, include):
        path = 'libraries/{}.mcl'.format(include)
        filepath = pkg_resources.resource_filename(__name__, path)
        check = pathlib.Path(filepath)
        if check.is_file():
            return filepath
        return None



    def _try_include_from_path(self, include):
        path = "{}.mcl".format(include)
        filepath = pathlib.Path(self.include_folder) /  path
        check = pathlib.Path(filepath)
        if check.is_file():
            return filepath
        return None



    def _try_include_from_local(self, include):
        path = f"{include}.mcl"
        filepath = pathlib.Path(os.getcwd()) /  path
        check = pathlib.Path(filepath)
        if check.is_file():
            return filepath
        return None



    def run_include(self, include: str, scope: MacalScope):
        if self.scope.have_include(include) == False:
            if self.debug:
                print("Including: ", include)
            if not include:
                raise RuntimeError("Invalid null argument: include")
            lang = Macal()
            lang.scope.name = include
            lang.scope.parent = scope
            lang.scope.root = scope.root
            lang.scope.can_search = True
            scope.children.append(lang.scope)
            filepath = self._try_include_from_pkg(include)
            if filepath is None:
                filepath = self._try_include_from_path(include)
            if filepath is None:
                filepath = self._try_include_from_local(include)
            if filepath is None:
                raise RuntimeError(f"Include not found: {include}")
            self.scope.root.includes.append(lang.scope)
            kwargs = {}
            lang.include_folder = self.include_folder
            lang.external_folder = self.external_folder
            lang.parser.external_folder = self.external_folder
            lang.run_from_file(filepath, **kwargs)
