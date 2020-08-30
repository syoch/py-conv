#Defines analyze of ast expr functions

import ast
import util



def expr_alias(val:ast.alias):
    alias=util.conv(val.name)
    if val.asname!=None:
        alias+="->"+val.asname
    return alias

def expr_arg(val:ast.arg):
    ret=util.conv(val.arg)
    if val.annotation:
        return ret+":"+util.conv(val.annotation)
    else:
        return ret

def expr_args(val:ast.arguments):
    defaults=[None]*(len(val.args)-len(val.defaults))+val.defaults
    return ", ".join(
        [
            util.conv(a[0])+"="+util.conv(a[1])
            for a in zip(val.args,defaults)
        ]+[
            "*"+util.conv(val.vararg)
        ]+[
            util.conv(a[0])+"="+util.conv(a[1])
            for a in zip(val.kwonlyargs,val.kw_defaults)
        ]+[
            "**"+util.conv(val.kwarg)
        ]
    )

table={
    "alias":expr_alias,
    "arguments":expr_args,
    "arg":expr_arg,
    "Constant":lambda a:util.conv(a.value),
}