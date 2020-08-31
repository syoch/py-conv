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

def expr_attr(val:ast.Attribute):
    return util.conv(val.value)+"."+val.attr

def expr_name(val:ast.Name):
    return val.id

def expr_call(val:ast.Call):
    def conv(val):
        a=val.__class__.__name__
        if a=="Call":
            return expr_call(val)
        else:
            return util.conv(val)
    tmp=conv(val.func)
    tmp+="("
    tmp+=", ".join([conv(arg) for arg in val.args])
    if len(val.keywords)!=0:
        tmp+=", "
        tmp+=", ".join([keyword.arg+"="+conv(keyword.value) for keyword in val.keywords])
    tmp+=")"
    return tmp

def expr_comp(val:ast.Compare):
    return util.conv(val.left)+" ".join([util.conv(op)+" "+util.conv(val)+" " for (op,val) in zip(val.ops,val.comparators)])

table={
    "alias":expr_alias,
    "arguments":expr_args,
    "arg":expr_arg,
    "Attribute":expr_attr,
    "Name":expr_name,
    "Constant":lambda a:util.conv(a.value),
    "Expr":lambda a:util.conv(a.value),
    "Call":expr_call,
    "Compare":expr_comp,
}