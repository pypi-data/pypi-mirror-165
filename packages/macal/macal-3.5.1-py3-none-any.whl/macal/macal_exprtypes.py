# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""constants used as type names for expression nodes."""



class ExpressionType(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError(name)



ExpressionTypes = ExpressionType([
	"BINARY",
	"UNARY",
	"LITERAL",
	"GROUPING",
	"VARIABLE",
	"INDEX",
	"PARAMS",
	"FUNCTION",
	"CALL",
	])