# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""macal variable type constants"""



class VariableType(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError(name)



VariableTypes = VariableType([
	'ANY',
	'ARRAY',
	'BOOL',
	'FLOAT',
	'FUNCTION',
	'INT',
	'NIL',
	'PARAMS',
	'RECORD',
	'STRING',
	'VARIABLE'
	])