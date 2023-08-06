# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""PFunction class implementation, this class is used by the scope and by the interpreter."""

from .macal_parsernodes import ast_Block, ast_function_Param_list
from .macal_variable_types import VariableTypes

class MacalFunction:
	"""PFunction initialization."""
	def __init__(self, name: str, args: list, block):
		self.name:        str = name
		self.args:        ast_function_Param_list = args
		self.block:       ast_Block = block
		self.scope  = None
		self.is_extern:   bool = False
		self.call_extern = None



	def get_type(this):
		return VariableTypes.FUNCTION



	def __str__(self):
		return f"{self.name}({self.args}) {self.is_extern} {self.call_extern} \n{self.block}"