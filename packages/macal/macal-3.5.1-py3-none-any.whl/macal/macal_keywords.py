# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.


"""macal Keyword Names"""

KW_IF          = 'if'
KW_ELSE        = 'else'
KW_ELIF        = 'elif'

KW_SELECT      = 'select'
KW_DISTINCT    = 'distinct'
KW_AS          = 'as'
KW_FROM        = 'from'
KW_WHERE       = 'where'
KW_MERGE       = 'merge'
KW_INTO        = 'into'

KW_FOREACH     = 'foreach'

KW_BREAK       = 'break'
KW_HALT        = 'halt'
KW_RETURN      = 'return'
KW_CONTINUE    = 'continue'

KW_INCLUDE     = 'include'

TRUE           = 'true'
FALSE          = 'false'
NIL            = 'nil'
AND            = 'and'
OR             = 'or'
NOT            = 'not'

KW_RECORD      = 'record'
KW_ARRAY       = 'array'

KW_EXTERNAL    = 'external'

KW_PARAMS      = 'params'
KW_ANY         = "any"
KW_VARIABLE    = "variable"

Keywords = [KW_IF, KW_ELSE, KW_ELIF, KW_SELECT, KW_DISTINCT, KW_AS, KW_FROM, KW_WHERE, KW_MERGE, KW_ANY, KW_VARIABLE,
                KW_INTO, KW_FOREACH, KW_BREAK, KW_HALT, KW_CONTINUE,
                KW_RETURN, KW_RECORD, KW_ARRAY, KW_INCLUDE, KW_EXTERNAL, KW_PARAMS]
