# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

""""Named tuples used for function return values"""

from collections import namedtuple
from .macal_lextokentype import LexTokenType
from .macal_sourcelocation import SourceLocation


# Used by the parser to split each parameter in the select statement by it's token, astoken and
# asvalue. token being the name of a field as value or * for any.
# Astoken being the "as" keyword, asvalue being the token that has the destination name of the
# field.
SelectParam = namedtuple('SelectParam', ['token', 'astoken', 'asvalue'])

Some = namedtuple('Some', ['value', 'location'])


# this is the new 3.0 stuff.
# The token position is an interresting value to store because of useage in syntax highlighting.
# For making things human readable it has no real function though.
# The line and offset are for the first character in the token.

class LexToken:
	def __init__(self, token_type: LexTokenType, token_value, pos: int, location: SourceLocation):
		self.token_type: str = token_type
		self.token_value = token_value
		self.token_position: int = pos
		self.location: SourceLocation = location.Clone()

		

	def debugPrint(self):
		print("Token:")
		print("Type:     ", self.type)
		print("Value:    ", self.value)
		print('Pos:      ', self.token_position)
		print('Location: ', self.location)
		


	def __repr__(self):
		return (f"""LexerToken(token_type = "{self.token_type}", token_value = "{self.token_value}", """ +
			f"token_position = {self.token_position}, token_location = {self.location})")



	def __str__(self):
		return f"{self.token_type} : {self.token_value} {self.location}"

