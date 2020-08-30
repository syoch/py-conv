#Defines analyze of ast expr functions

import ast
import util

def expr_alias(val:ast.alias):
    alias=util.conv(val.name)
    if val.asname!=None:
        alias+="->"+val.asname
    return alias

table={
    "alias":expr_alias,
    "str":lambda a:a
}