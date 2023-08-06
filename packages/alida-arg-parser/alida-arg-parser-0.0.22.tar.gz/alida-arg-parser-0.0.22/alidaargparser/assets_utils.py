from alidaargparser import ArgumentParser
import sys

def get_asset_property(asset_name, property=None):
    
    to_find = "--" + asset_name
    if property is not None:
        to_find = to_find + "." + property
    
    for arg in sys.argv:
        if arg.split("=")[0] == to_find:
            return "=".join(arg.split("=")[1:])

