#
# Filename:       | macal_library_time.py
# Author:         | Marco Caspers
# Description:    |
#
# Macal 2.0 Time Library
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.5.0 16-05-2022: detached from class MacalLibrary and now implemented through include time.mcl with "external" hooks to this module.
#

"""Time library implementation"""
from datetime import datetime
import time
from macal.macal_library_external import *

NUM_SECONDS_FIVE_MINUTES = 300
NUM_SECONDS_ONE_HOUR = 3600
TIME_FORMAT = '%Y%m%d%H%M%S'
ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
ISO_TIME_tzFORMAT = "%Y-%m-%dT%H:%M:%S.0Z"
__stopwatch__ = 0



def DateToUnix(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Convert a date_string of format YYYYMMDDhhmmss to unix time integer.
       Assumes the date string object is UTC time."""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    dt = datetime.strptime(GetParamValue(params, "date_str"), TIME_FORMAT)
    epoch = datetime(1970, 1, 1)
    result = int((dt - epoch).total_seconds())
    scope.SetReturnValue(result, VariableTypes.INT)



def IsoToUnix(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Convert a date_string of format %Y-%m-%dT%H:%M:%S.%f to unix time integer.
       Assumes the date string object is in iso format."""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    dt = datetime.strptime(GetParamValue(params, "date_str"), ISO_TIME_FORMAT)
    epoch = datetime(1970, 1, 1)
    result = int((dt - epoch).total_seconds())
    scope.SetReturnValue(result, VariableTypes.INT)



def DateFromUnix(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Converts time in seconds since UNIX EPOCH to UTC Time format"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    result = time.strftime(TIME_FORMAT, time.gmtime(GetParamValue(params, "seconds")))
    scope.SetReturnValue(result, VariableTypes.STRING)



def IsoFromUnix(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Converts time in seconds since UNIX EPOCH to UTC Time format"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    result = time.strftime(ISO_TIME_tzFORMAT, time.gmtime(GetParamValue(params, "seconds")))
    scope.SetReturnValue(result, VariableTypes.STRING)



def UtcNow(func: MacalFunction, name: str, params: list, scope: MacalScope):
    ValidateFunction(name, func, scope)
    result = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    scope.SetReturnValue(result, VariableTypes.STRING)



def UtcIsoNow(func: MacalFunction, name: str, params: list, scope: MacalScope):
    ValidateFunction(name, func, scope)
    result = "{}Z".format(datetime.utcnow().isoformat())
    scope.SetReturnValue(result, VariableTypes.STRING)



def IsoNow(func: MacalFunction, name: str, params: list, scope: MacalScope):
    ValidateFunction(name, func, scope)
    result = datetime.now().isoformat()
    scope.SetReturnValue(result, VariableTypes.STRING)



def Now(func: MacalFunction, name: str, params: list, scope: MacalScope):
    ValidateFunction(name, func, scope)
    result = datetime.now().strftime("%Y%m%d%H%M%S")
    scope.SetReturnValue(result, VariableTypes.STRING)

    

def PerfCounter(func: MacalFunction, name: str, params: list, scope: MacalScope):
    ValidateFunction(name, func, scope)
    result = time.perf_counter()
    scope.SetReturnValue(result, VariableTypes.FLOAT)
