# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Lexer implementation"""

from string import whitespace

from .macal_keywords import Keywords, TRUE, FALSE, NIL, AND, OR, NOT
from .macal_lextoken import LexToken
from .macal_lextokentypes import SINGLE_TOKENS, DOUBLE_TOKENS
from .macal_exceptions import LexError
from .macal_lextokentype import LexTokenTypes
from .macal_sourcelocation import SourceLocation
from typing import Tuple

from .__about__ import __version__



class MacalTokenizer:
    def __init__(self):
        self.source: str = ""
        self.length: int = 0
        self.version: str = __version__
        self.filename: str = ''
        self.count = 0



    def lex(self, source: str, filename: str) -> list:
        self.source = source
        self.length = len(source)
        self.count = 0
        tokens = []
        location = SourceLocation(1, 1)
        position = 0
        (token, next_position, next_location) = self.lex_token(position, location)
        while token is not None and token != LexTokenTypes.Eof:
            tokens.append(token)
            (token, next_position, next_location) = self.lex_token(next_position, next_location)
        return tokens



    def lex_current(self, position: int, location: SourceLocation) -> Tuple[str, int, SourceLocation]:
        if position >= self.length:
            return (None, position, location)
        return (self.source[position], position, location)



    def lex_next(self, position: int, location: SourceLocation) -> Tuple[str, int, SourceLocation]:
        (current, next_position, next_location) = self.lex_current(position + 1, location.NextColumn())    
        return (current, next_position, next_location)



    def lex_peek(self, position: int, location: SourceLocation) -> Tuple[str, int, SourceLocation]:
        (current, _, _) = self.lex_current(position + 1, location)
        return (current, position, location)



    def skip_whitespace(self, position: int, location: SourceLocation) -> Tuple[str, int, SourceLocation]:
        (current, next_position, next_location) = self.lex_current(position, location)
        while current is not None and current in whitespace:
            if current == '\n':
                next_location = next_location.NewLine()
            (current, next_position, next_location) = self.lex_next(next_position, next_location)
        return (current, next_position, next_location)


    
    def lex_token(self, position: int, location: SourceLocation) -> Tuple[LexToken, int, SourceLocation]:
        (current, next_position, next_location) = self.skip_whitespace(position, location)
        if current is None:
            return  (LexTokenTypes.Eof, next_position, next_location)
        if current.isalpha():
            return self.lex_identifier(next_position, next_location)
        if current.isdigit():
            return self.lex_number(next_position, next_location)
        if current == '"' or current == "'":
            return  self.lex_string(next_position, next_location)
        return self.lex_shorts(next_position, next_location)




    def lex_identifier(self, position: int, location: SourceLocation) -> Tuple[LexToken, int, SourceLocation]:
        start = location.Clone()
        (current, next_position, next_location) = self.lex_current(position, location)
        while current is not None and (current.isalpha() or current == '_' or current.isdigit()):
            (current, next_position, next_location) = self.lex_next(next_position, next_location)
        ident = self.source[position:next_position]
        tt = LexTokenTypes.Identifier
        if ident in (TRUE, FALSE):
            tt = LexTokenTypes.BoolType
        elif ident == NIL:
            tt = LexTokenTypes.NilType
        elif ident in Keywords:
            tt = LexTokenTypes.Keyword
        elif ident == AND:
            tt = LexTokenTypes.OpAnd
        elif ident == OR:
            tt = LexTokenTypes.OpOr
        elif ident == NOT:
            tt = LexTokenTypes.OpNot
        return (LexToken(tt, ident, position, start), next_position, next_location)



    def lex_number(self, position: int, location: SourceLocation) -> Tuple[LexToken, int, SourceLocation]:
        start = location.Clone()
        (current, next_position, next_location) = self.lex_current(position, location)
        points = 0
        while current is not None and (current.isdigit() or current == '.'):
            if current == '.':
                points += 1
            if points > 1:
                raise LexError("Multiple decimal points found in float", next_location.line, next_location.column, self.filename)
            (current, next_position, next_location) = self.lex_next(next_position, next_location)
        return (LexToken(LexTokenTypes.IntType if points == 0 else LexTokenTypes.FloatType,
            int(self.source[position:next_position]) if points == 0 else float(self.source[position:next_position]), 
            position, start), next_position, next_location)



    @staticmethod
    def apply_escapes(source: str) -> str:
        index = 0
        length = len(source)
        destination = "";
        while index < length:
            if source[index] == '\\' and index+1 < length:
                if (source[index+1] in ['a','b','n','r','t','0']):
                    if source[index+1] == 'a':
                        destination=f"{destination}\a"
                    elif source[index+1] == 'b':
                        destination=f"{destination}\b"
                    elif source[index+1] == 'n':
                        destination=f"{destination}\n"
                    elif source[index+1] == 'r':
                        destination=f"{destination}\r"
                    elif source[index+1] == 't':
                        destination=f"{destination}\t"
                    else:
                        destination=f"{destination}\0"
                else:
                    destination = f"{destination}{source[index+1]}"
                index += 1
            else:
                destination=f"{destination}{source[index]}"
            index += 1
        return destination



    def lex_string(self, position: int, location: SourceLocation) -> Tuple[LexToken, int, SourceLocation]:
        start = location.Clone()
        (current, next_position, next_location) = self.lex_current(position, location)
        terminator = current
        (current, next_position, next_location) = self.lex_next(next_position, next_location)
        escaped = False
        while current is not None and True if current != terminator else escaped:
            escaped = current == '\\'
            (current, next_position, next_location) = self.lex_next(next_position, next_location)
        if current is None:
            raise LexError("Unexpected end of file in string", next_location.line, next_location.column, self.filename)
        (_, next_position, next_location) = self.lex_next(next_position, next_location)
        return (LexToken(LexTokenTypes.StringType, self.apply_escapes(self.source[(position+1):(next_position-1)]), position, start),
            next_position, next_location)



    def lex_shorts(self, position: int, location: SourceLocation) -> Tuple[LexToken, int, SourceLocation]:
        start = location.Clone()
        (current, next_position, next_location) = self.lex_current(position, location)
        if current in SINGLE_TOKENS:
            (_, next_position, next_location) = self.lex_next(next_position, next_location)
            return (LexToken(SINGLE_TOKENS[current], current, position, start), next_position, next_location)
        elif next_position < self.length:
            return self.lex_doubles(position, location)
        return (LexToken(None, current, position, start), next_position, next_location)    



    def lex_doubles(self, position: int, location: SourceLocation) -> Tuple[LexToken, int, SourceLocation]:
        start = location.Clone()
        (current, next_position, next_location) = self.lex_current(position, location)
        (next_char, _, _) = self.lex_peek(next_position, next_location)
        double = f"{current}{next_char}"
        if double in DOUBLE_TOKENS:
            (_, next_position, next_location) = self.lex_next(next_position, next_location) # skip #1
            if DOUBLE_TOKENS[double] == LexTokenTypes.Comment:
                return self.lex_comment_short(next_position, next_location)
            elif DOUBLE_TOKENS[double] == LexTokenTypes.CommentLeft:
                return self.lex_comment_long(next_position, next_location)
            else:
                (_, next_position, next_location) = self.lex_next(next_position, next_location) # skip #2
                return (LexToken(DOUBLE_TOKENS[double], double, position, start), next_position, next_location)
        elif current in DOUBLE_TOKENS:
            (_, next_position, next_location) = self.lex_next(next_position, next_location) # skip #1
            return (LexToken(DOUBLE_TOKENS[current], current, position, start), next_position, next_location)
        else:
            raise LexError(f"Invalid character sequence ({double}).", start.line, start.column, self.filename)
        return (LexToken(None, current, position, start), next_position, next_location)



    def lex_comment_short(self, position: int, location: SourceLocation) -> Tuple[LexToken, int, SourceLocation]:
        start = SourceLocation(line = location.line, column = location.column - 1)
        (_, next_position, next_location) = self.lex_next(position, location) # skip #2
        (current, next_position, next_location) = self.lex_current(next_position, next_location)
        while current is not None and current != '\n':
            (current, next_position, next_location) = self.lex_next(next_position, next_location)
        # -1 because we want to include the first /, -1 because we don't need the LF at the end.
        value = (LexToken(LexTokenTypes.Comment, self.source[position-1:next_position], position-1, start), next_position, next_location)
        return value



    def lex_comment_long(self, position: int, location: SourceLocation) -> Tuple[LexToken, int, SourceLocation]:
        start = SourceLocation(line = location.line, column = location.column - 1)
        (current, next_position, next_location) = self.lex_next(position, location)
        (peek, next_position_peek, next_peek_location) = self.lex_peek(next_position, next_location)
        dbl = f"{current}{peek}"
        if current == '\n':
            next_location = next_location.NewLine()
        while current is not None and (dbl not in DOUBLE_TOKENS or DOUBLE_TOKENS[dbl] != LexTokenTypes.CommentRight):
            (current, next_position, next_location) = self.lex_next(next_position, next_location)
            if current == '\n':
                next_location = next_location.NewLine()
                continue;
            (peek, next_position_peek, next_peek_location) = self.lex_next(next_position, next_location)
            dbl = f"{current}{peek}"
        # -1 because we want to include the first /
        value = (LexToken(LexTokenTypes.Comment, self.source[position-1:next_position_peek+1], position-1, start), next_position+2, next_location)
        return value

