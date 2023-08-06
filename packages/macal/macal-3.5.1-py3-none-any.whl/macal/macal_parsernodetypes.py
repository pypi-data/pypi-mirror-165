# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""AST Node type names"""

class ParserNodeType(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError(name)

ParserNodeTypes = ParserNodeType([
	'BLOCK', 
	'ASSIGN', 
	'VARIABLE', 
	'INDEX', 
	'PARAMS', 
	'CALL', 
	'IF', 
	'ELIF', 
	'ELSE',
	'FOREACH',
	'HALT',
	'BREAK',
	'RETURN',
	'SELECT',
	'INCLUDE',
	'EXTERNAL',
	'CONTINUE',
	'FUNCTION'
	])