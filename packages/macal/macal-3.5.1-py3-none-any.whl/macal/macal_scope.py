# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Scope class implementation, this class is used by the interpreter."""

from .macal_variable_types import VariableTypes
from .macal_variable import MacalVariable
from .macal_function import MacalFunction

VARIABLE_COLUMN_WIDTH = 40
TYPE_COLUMN_WIDTH     = 12
VALUE_COLUMN_WIDTH    = 36



class MacalScope:
    """Scope class implements execution branch scope"""
    def __init__(self, name: str, parent):
        self.name = name
        self.variables:     list = []
        self.functions:     list = []
        self.children:      list = []
        self.includes:      list = []
        self.break_flag:    bool       = False
        self.x_halt_flag:   bool       = False
        self.continue_flag: bool       = False
        self.is_loop:       bool       = False
        self.is_function:   bool       = False
        self.parent:        MacalScope = parent
        self.Libraries:     list       = []
        self.can_search:    bool       = True
        self.root:          MacalScope = None
        self.debug:         bool       = False



    def create_child(self, name: str, prop_loop: bool = True):
        child = MacalScope("{}->{}".format(self.name, name), self)
        if prop_loop:
            child.is_loop = self.is_loop
        child.is_function = self.is_function;
        self.children.append(child)
        child.root = self.root
        return child



    def remove_child(self, child):
        self.children.remove(child)
    


    def set_halt(self):
        self.x_halt_flag = True



    def get_halt(self):
        return self.x_halt_flag



    def add_new_variable(self, name: str):
        """Adds a new PVariable to the scope and returns it."""
        variable = MacalVariable(name)
        self.variables.append(variable)
        return variable



    def add_new_function(self, name: str, parameters, block, is_extern, call_extern):
        """Adds a new PFunction to the scope and returns it."""
        func = MacalFunction(name, parameters, block)
        func.is_extern = is_extern
        func.call_extern = call_extern
        self.functions.append(func)
        return func



    def set_continue(self):
        """Sets continue flag"""
        self.continue_flag = True
        if self.parent is not None:
            this = self.parent
            while this is not None and this.is_loop:
                this.continue_flag = True
                this = this.parent



    def reset_continue(self):
        """Resets continue flag, please ensure to always call this from the scope of the loop itself!"""
        if self.is_loop:
            self.continue_flag = False
            if self.children:
                for child in self.children:
                    child.reset_continue()


    
    @staticmethod
    def _obj_first_or_default(lst: list, name: str):
        """Returns the first object in the list that has name, or None if not found."""
        return next((x for x in lst if x.name == name), None)


    
    def _get_variable(self, name: str):
        """Find variable by name in the current scope"""
        return next((x for x in self.variables if x.name == name), None)



    def _get_function(self, name: str):
        """Find function by name in the current scope"""
        return next((x for x in self.functions if x.name == name), None)



    def _get_scope_exitvar(self):
        for var in self.variables:
            if var.name[:8] == "?return_":
                return var
        #this is obsolete if you use find_function_scope..
        #this = self
        #while this.parent != None and this.parent.is_function is True:
        #    this = this.parent
        #if this != None and this.is_function == True:
        #    return this._get_scope_exitvar()
        return None



    def SetReturnValue(self, value, valuetype):
        var = self._get_scope_exitvar()
        if var is None:
            raise Exception(f"This scope has no exitvar! {self}")
        if self.debug:
            print(f"scope set returnvalue: {var.name} -> {value} ({valuetype})")
        var.set_value(value)
        var.set_type(valuetype)



    def _find_variable(self, name: str, scope, override: bool = False):
        """Find variable by name in the current scope. If not found, calls parent scope to do so, if parent is not None"""
        if self.debug:
            print()
            print(f"_find_variable(var: {name}, scope: {scope.name})")
        var = scope._get_variable(name)
        if self.debug:
            print(f"scope._get_variable({name}) : {var}")
        if var is not None:
            return var

        if self.debug:
            print("self.can_search", self.can_search)
            if override and not self.can_search:
                print("self.can_search is overridden")
        if not self.can_search and not override:
            return None
        if len(scope.Libraries) > 0:
            if self.debug:
                print("search in libraries")
            for lib in scope.Libraries:
                var = lib.variable_by_name(name)
                if var  is not None:
                    return var
        if scope.parent is not None:
            if self.debug:
                print("search in parent")
            this = scope.parent
            this.debug = scope.debug
            var = scope._find_variable(name, scope.parent, override)
            this.debug = False
            return var
        else:
            if self.debug:
                print("We are in root, no parent to search in.")
        if len(self.root.includes) > 0:
            if self.debug:
                print("search in root.includes.")
            for incl in self.root.includes:
                if incl != self:
                    var = incl._get_variable(name)
                    if var  is not None:
                        return var
        else:
            if self.debug:
                print("No includes to search.")
        if self.debug:
            print("Really found nothing here.")
        return None



    def _find_function(self, name: str, scope):
        """Find function by name in the current scope. If not found, calls parent scope to do so, if parent is not None"""
        func = scope._get_function(name)
        if func is not None:
            return func

        if len(scope.Libraries) > 0:
            for lib in scope.Libraries:
                func = lib.GetFunction(name)
                if func is not None:
                    return func

        if scope.parent is not None:
            return scope._find_function(name, scope.parent)

        if len(self.root.includes) > 0:
            for incl in self.root.includes:
                if incl != self:
                    func = incl._get_function(name)
                    if func is not None:
                        return func

        return None



    def find_variable(self, name: str, override: bool = False):
        if self.debug:
            print("find_variable Scope: ", self.name, " var to search for: ", name)
        return self._find_variable(name, self, override)



    def find_return_variable(self):
        if self.debug:
            print("find_return_variable")
        return self._get_scope_exitvar()



    def find_variable_outside(self, name):
        # find variable outside is called as part of finding a variable from a function call parameter.
        # kind of a ref parameter. This means that the var itself needs to be found outside the current scope.
        # So the starting point for searching for this var is the parent of the current scope.
        if self.debug:
            print("find_variable_outside Scope: ", self.name, " var to search for: ", name)
        if self.parent is not None:
            this = self.parent
            this.debug = self.debug
            var = this.find_variable(name, True)
            this.debug = False
            return var
        return None
    


    def find_function(self, name: str):
        return self._find_function(name, self)
    


    def find_function_scope(self):
        """This checks if the current scope is set to function, and walks to parent scopes if they are set to function to find the root function scope."""
        if self.is_function:
            this = self
            while this.parent != None and this.parent.is_function:
                this = this.parent
            if this.is_function:
                return this
        return None




    def have_include(self, name: str):
        if len(self.root.includes) > 0:
            for incl in self.root.includes:
                if incl.name == name:
                    return True
        return False



    def has_children(self):
        return len(self.children) > 0



    def has_variables(self):
        return len(self.variables) > 0



    def has_functions(self):
        return len(self.functions) > 0



    def has_includes(self):
        return len(self.root.includes) > 0



    def scopeSetDebug(self, value: bool):
        self.root.childSetDebug(value)



    def childSetDebug(self, value: bool):
        self.debug = value;
        for child in self.children:
            child.childSetDebug(value)        



    def print_variables(self):
        """Displays a table showing all variables in this scope."""
        # define the column width
        variable_size = VARIABLE_COLUMN_WIDTH
        type_size     = TYPE_COLUMN_WIDTH
        value_size    = VALUE_COLUMN_WIDTH
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))
        print("|{}|{}|{}|".format(
            "Variable".ljust(variable_size),
            "Type".ljust(type_size),
            "Value".ljust(value_size)))
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))
        for var in self.variables:
            vt = var.get_type()
            vts = '{}'.format(vt)
            vv = repr(var.get_value())
            if isinstance(vv, MacalFunction):
                vv = vv.name
            print("|{}|{}|{}|".format(var.name.ljust(variable_size), vts.ljust(type_size), '{}'.format(vv).ljust(value_size)))
        print(''.ljust(variable_size + type_size + value_size + 4,'_'))



    def print_functions(self):
        """Displays a table showing all functions in this scope."""
        variable_size = VARIABLE_COLUMN_WIDTH
        print(''.ljust(variable_size + 2,'_'))
        print("|{}|".format("Function".ljust(variable_size)))
        print(''.ljust(variable_size + 2,'_'))
        for fun in self.functions:
            fn = fun.name
            print("|{}|".format(fn.ljust(variable_size)))
        print(''.ljust(variable_size + 2,'_'))



    def print_includes(self):
        """Displays a table showing all includes in this scope."""
        variable_size = VARIABLE_COLUMN_WIDTH
        print(''.ljust(variable_size + 2,'_'))
        print("|{}|".format("Include".ljust(variable_size)))
        print(''.ljust(variable_size + 2,'_'))
        for fun in self.includes:
            fn = fun.name
            print("|{}|".format(fn.ljust(variable_size)))
        print(''.ljust(variable_size + 2,'_'))



    @staticmethod
    def get_value_type(obj):
        """returns a string representing the given object type"""
        result = "unknown"
        if obj is None:
            result = VariableTypes.NIL
        elif isinstance(obj, bool):
            result = VariableTypes.BOOL
        elif isinstance(obj, int):
            result = VariableTypes.INT
        elif isinstance(obj, float):
            result = VariableTypes.FLOAT
        elif isinstance(obj, str):
            result = VariableTypes.STRING
        elif isinstance(obj, list):
            result = VariableTypes.ARRAY
        # ToDo: Add dictionaries to the language.
        elif isinstance(obj, dict):
            result = VariableTypes.RECORD
        # the following types should never happen, but i added them in to be complete.
        elif isinstance(obj, complex):
            result = "complex"
        elif isinstance(obj, tuple):
            result = "tuple"
        elif isinstance(obj, bytes):
            result = "bytes"
        elif isinstance(obj, bytearray):
            result = "bytearray"
        elif isinstance(obj, set):
            result = "set"
        elif isinstance(obj, frozenset):
            result = "frozenset"
        else:
            raise Exception("Unknown type: {}".format(type(obj)))
        return result



    def root(self, scope):
        if scope.parent is not None:
            return self.root(scope.parent)
        else:
            return scope
    


    def print(self, scope):
        print(f"\nScope: {scope.name}, break: {scope.break_flag}, halt: {scope.x_halt_flag}, isLoop: {scope.is_loop}, Libraries: {len(scope.Libraries)}")
        if scope.has_variables():
            scope.print_variables()
        if scope.has_functions():
            scope.print_functions()
        if scope.has_includes():
            scope.print_includes()
        if scope.has_children():
            for child in scope.children:
                self.print(child)



    def printScopeTree(self):
        scope = self.root
        self.printScopeTreeLeaf(scope, "")



    def printScopeTreeLeaf(self, scope, indent):
        parent = "None"
        if scope.parent is not None:
            parent = scope.parent.name
        print("{}Scope: {}, parent: {} break: {}, halt: {}, isLoop: {}, Libraries: {}, Includes: {}, Can search: {}".format(
            indent, 
            scope.name, 
            parent,
            scope.break_flag,
            scope.x_halt_flag,
            scope.is_loop,
            len(scope.Libraries),
            len(scope.includes),
            scope.can_search))
        indent = "{}    ".format(indent)
        print("{}Functions:".format(indent))
        for fun in scope.functions:
            print("{}    {}".format(indent, fun.name))
        print("{}Variables:".format(indent))
        for var in scope.variables:
            print("{}    {}".format(indent, var.name))
        print("{}Includes:".format(indent))
        for incl in scope.includes:
            print("{}    {}".format(indent, incl.name))
        print("{}Children:".format(indent))
        for child in scope.children:
            self.printScopeTreeLeaf(child, "{}    ".format(indent))
        print()



    def __repr__(self):
        return "MacalScope({})".format(self.name)



    def __str__(self):
        parentName = "None"
        if self.parent is not None:
            parentName = self.parent.name
        result = f"\nScope: {self.name}, break: {self.break_flag}, halt: {self.x_halt_flag}, isLoop: {self.is_loop}, Libraries: {len(self.Libraries)}, Includes: {len(self.includes)}, Parent: {parentName}\n"
        if self.has_variables():
            result = f"{result}\nVariables:\n"
            for variable in self.variables:
                result = f"{result}{variable}\n"
        if self.has_functions():
            result = f"{result}\nFunctions:\n"
            for function in self.functions:
                result = f"{result}{function.name}\n"
        if len(self.includes) > 0:
            result = f"{result}\nIncludes:\n"
            for incl in self.includes:
                result = f"{result}{incl.name}\n"
        if self.has_children():
            result = f"{result}\nChildren:\n"
            for child in self.children:
                result = f"{result}{child}\n"
        return result