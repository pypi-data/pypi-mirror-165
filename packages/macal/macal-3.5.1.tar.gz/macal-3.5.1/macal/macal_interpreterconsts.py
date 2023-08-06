# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

from collections import namedtuple

"""Interpreter class constant values"""

EXIT_VAR_NAME = 'exit_code'

"""Used specifically for the select command"""
SelectFieldFilter = namedtuple("SelectFilter", ["field_name", "as_name"])
FuncArg = namedtuple("FuncArg", ["arg_name", "arg_type"])