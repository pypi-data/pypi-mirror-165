# History:
#
# 3.5.1 25-05-2022: Moved __version__ numbering to __about__
#                   Changed header to only include history for this file, removed all old history.

"""Expression item class used as value for left and right brances of the expression"""

from .macal_sourcelocation import SourceLocation
from .macal_exprtypes import ExpressionType

class ExpressionItem:
    """Expression item class, used by expressions and interpreter"""
    def __init__(self, value, item_type, location: SourceLocation = None):
        """Initializes expression item"""
        self.value     = value
        self.item_type: ExpressionType = item_type
        self.ref:       bool = False
        self.format:    bool = False
        self.Location:  SourceLocation = location

    def __str__(self):
        return f"ExpressionItem: value {self.value} type {self.item_type} ref {self.ref} format {self.format} {self.Location}."
