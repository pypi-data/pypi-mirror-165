#
# Filename:       | macal_library_syslog.py
# Author:         | Marco Caspers
# Version;        | 3.5.0
# Description:    |
#
# Macal 2.0 Syslog Library
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.5.0 16-05-2022: detached from class MacalLibrary and now implemented through include syslog.mcl with "external" hooks to this module.
#

"""Syslog library implementation"""

from macal.macal_library_external import *
from macal.macal_SysLog_class import SysLog

SysLogLocal = SysLog()
        
def Syslog(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Syslog function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    level = GetParamValue(params, "level")
    message = GetParamValue(params, "message")
    if level == "debug":
        SysLogLocal.debug(message)
    elif level == "info" or level == "information":
        SysLogLocal.info(message)
    elif level == "warn" or level == "warning":
        SysLogLocal.warn(message)
    elif level == "error":
        SysLogLocal.error(message)
    elif level == "critical":
        SysLogLocal.critical(message)
    else:
        raise RuntimeError(f"Invalid syslog level given: {level}")



def SyslogInit(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of SysLog init function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    remote = GetParamValue(params, "remote")
    SysLogLocal.SysLogInit(remote)



def SyslogSetAddress(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of SysLog SetAddress function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    address = GetParamValue(params, "address")
    port = GetParamValue(params, "port")
    SysLogLocal.SysLogSetAddress(address, port)
