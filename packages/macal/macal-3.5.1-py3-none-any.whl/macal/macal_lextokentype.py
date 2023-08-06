#
# History
#
# Date: 30-08-2022
#
# Version: 3.5.1
#
# Description:
#
# Initial implementation.
#
# This class is used as an enum for the Lexer token type.
#

class LexTokenType(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError(name)

LexTokenTypes = LexTokenType(["LParen", "RParen", "LIndex", "RIndex", 
    "LBracket", "RBracket", "Semicolon", 'Colon', 'Comma', 'Dot', 'OpFormat',
    'OpRef', 'OpEqual', 'OpAdd', 'OpSub', 'OpMul', 'OpDiv', 'OpPwr', 'OpAssign',
    'OpLt', 'OpGt', 'OpNot', 'OpNe', 'OpLte', 'OpGte', 'OpDefine', 'OpAnd', 
    'OpOr', 'Identifier', 'Keyword', 'NewArrayIndex', 'NewRecordIndex', 
    'Comment', 'CommentLeft', 'CommentRight', 'Eof', 'Error', 'BoolType',
    'IntType', 'NilType', 'FloatType', 'StringType', 'ArrayType', 'RecordType'])

