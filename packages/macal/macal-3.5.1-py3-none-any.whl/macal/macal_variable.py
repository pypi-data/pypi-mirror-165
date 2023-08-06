# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Variable class implementation, this class is used by the scope and by the interpreter."""

class MacalVariable:
	"""Variable had to be a class because a named tuple is not mutable after it was set."""
	def __init__(self, name):
		self.name  = name
		self.x_value = None
		self.x_var_type = None
		self.initialized = False
		self.ref = False
		self.format = False
		self.constant = False
		self.index = None

	def get_value(self):
		#print(f"get var ({self.name}) value: {self.x_value}")
		if not self.initialized:
			raise Exception(f"Runtime Error: Attempt to retrieve value from uninitialized variable ({self.name}).")
		return self.x_value

	def set_value(self, value):
		#print(f"set var ({self.name}) value: {value} type: {self.x_var_type}.")
		if self.constant == True:
			raise Exception(f"Runtime Error: Attempt to assing a value to a constant ({self.name}).")
		self.x_value = value
		self.initialized = True

	def get_type(self):
		return self.x_var_type

	def set_type(self, var_type):
		self.x_var_type = var_type

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return f"""VARIABLE: {"REF " if self.ref else ""}{"FMT " if self.format else ""}{"INITIALIZED " if self.initialized else ""}{self.name} ({self.x_var_type}) : {self.x_value}"""
