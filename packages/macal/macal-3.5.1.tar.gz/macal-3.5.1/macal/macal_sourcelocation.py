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
# This is used throughout the entire project for indicating where in the source code a specific token is.
#

from __future__ import annotations



class SourceLocation:
	def __init__(self, line: int, column: int):
		self.line: int   = line
		self.column: int = column
		


	def Clone(self) -> SourceLocation:
		return SourceLocation(self.line, self.column)



	def NextColumn(self) -> SourceLocation:
		self.column += 1
		return self



	def NewLine(self) -> SourceLocation:
		self.line += 1
		self.column = 0
		return self



	def __repr__(self) -> str:
		return f"SourceLocation(line={self.line}, column={self.column})"



	def __str__(self) -> str:
		return f"@({self.line}, {self.column})"
