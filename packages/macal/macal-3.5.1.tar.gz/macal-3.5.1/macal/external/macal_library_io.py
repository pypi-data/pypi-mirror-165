#
# Filename:       | macal_library_io.py
# Author:         | Marco Caspers
# Version:        | 3.5.0
# Description:    |
#
#
# Macal 2.0 IO Library
#
# 3.0.6 26-01-2022: removed list type decorators to remove python version dependancy (>=3.8.4)    
#
# 3.5.0 16-05-2022: detached from class MacalLibrary and now implemented through include io.mcl with "external" hooks to this module.
#

"""IO library implementation"""

import os
import json
from macal.macal_library_external import *



def Load(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Load function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    filename = GetParamValue(params, "filename")
    try:
        with open (filename, "r") as tf:
            content=tf.read()
        scope.SetReturnValue(content, VariableTypes.STRING)
    except Exception as ex:
        raise RuntimeError(f"Load Exception: {ex}")



def ReadJSON(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Read JSON file function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    filename = GetParamValue(params, "filename")
    try:
        with open(filename, 'r') as fp:
            content = json.load(fp)
        scope.SetReturnValue(content, scope.get_value_type(content))
    except Exception as ex:
        raise RuntimeError(f"ReadJSON Exception: {ex}")
    


def Exists(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Exists function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    filename = GetParamValue(params, "filename")
    result = os.path.exists(filename)
    scope.SetReturnValue(result, VariableTypes.BOOL)



def Save(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Save function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    content  = GetParamValue(params, "content")
    filename = GetParamValue(params, "filename")
    try:
        with open(filename, "w") as tf:
            tf.write(content)
        scope.SetReturnValue(True, VariableTypes.BOOL)
    except Exception as ex:
        raise RuntimeError(f"Save exception: {ex}")



def WriteJSON(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of Save function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    content  = GetParamValue(params, "content")
    filename = GetParamValue(params, "filename")
    try:
        with open(filename, 'w') as fp:
            json.dump(content, fp, indent=4)
        scope.SetReturnValue(True, VariableTypes.BOOL)
    except Exception as ex:
        raise RuntimeError(f"WriteJSON exception: {ex}")



def GetLastRun(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of GetLastRun function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    org_name = GetParamValue(params, "org_name")
    iso_now  = GetParamValue(params, "iso_now")
    fileName = "/tmp/last_run_{}.ctl".format(org_name);
    if os.name == "nt":
        fileName = "c:/temp/last_run_{}.ctl".format(org_name);
    if os.path.exists(fileName):
        with open (fileName, "r") as tf:
            result=tf.read()
        if result is None or result == '':
            result = iso_now
    else:
        result = iso_now
    scope.SetReturnValue(result, VariableTypes.STRING)



def SetLastRun(func: MacalFunction, name: str, params: list, scope: MacalScope):
    """Implementation of SetLastRun function"""
    ValidateFunction(name, func, scope)
    ValidateParams(name, params, scope, func, True)
    org_name = GetParamValue(params, "org_name")
    iso_now  = GetParamValue(params, "iso_now")
    fileName = "/tmp/last_run_{}.ctl".format(org_name);
    if os.name == "nt":
        fileName = "c:/temp/last_run_{}.ctl".format(org_name);
    try:
        with open(fileName, "w") as tf:
            tf.write(iso_now)
    except Exception as ex:
        raise RuntimeError(f"Set last run exception: {ex}")
