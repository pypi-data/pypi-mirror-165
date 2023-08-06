# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Token type names for the Lexer output"""

from .macal_lextokentype import LexTokenTypes


NEW_ARRAY_INDEX  = '?_NEW_ARRAY_INDEX_?'
NEW_RECORD_INDEX = '?_NEW_RECORD_INDEX_?'


SINGLE_TOKENS = {
    '(': LexTokenTypes.LParen,
    ')': LexTokenTypes.RParen,
    '[': LexTokenTypes.LIndex,
    ']': LexTokenTypes.RIndex,
    '{': LexTokenTypes.LBracket,
    '}': LexTokenTypes.RBracket,
    ';': LexTokenTypes.Semicolon,
    ',': LexTokenTypes.Comma,
    '+': LexTokenTypes.OpAdd,
    '-': LexTokenTypes.OpSub,
    '*': LexTokenTypes.OpMul,
    '^': LexTokenTypes.OpPwr, 
    '$': LexTokenTypes.OpFormat,
    '&': LexTokenTypes.OpRef,
    ':': LexTokenTypes.Colon,
    '.': LexTokenTypes.Dot}

DOUBLE_TOKENS = {
    '==': LexTokenTypes.OpEqual,
    '=':  LexTokenTypes.OpAssign,
    '>=': LexTokenTypes.OpGte,
    '>':  LexTokenTypes.OpGt,
    '<=': LexTokenTypes.OpLte,
    '<':  LexTokenTypes.OpLt,
    '!=': LexTokenTypes.OpNe,
    '!' : LexTokenTypes.OpNot,
    '//': LexTokenTypes.Comment,
    '/*': LexTokenTypes.CommentLeft,
    '*/': LexTokenTypes.CommentRight,
    '/' : LexTokenTypes.OpDiv,
    '=>': LexTokenTypes.OpDefine}