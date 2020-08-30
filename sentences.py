#Defines analyze of ast sentence functions

import ast
from exprs import expr_call
import os
import util
import datamgr

def sent_import(sentence:ast.Import,f=""):
    tmp=""
    for a in sentence.names:
        name=util.conv(a)
        if os.path.exists(name+".py"):
            tmp+=f+"#include \""+name+".cpp"+"\"\n"
            datamgr.push("srcs",name+".py")
        else:
            tmp+=f+"#include <"+name+">\n"
    return tmp

def sent_funcdef(sentence:ast.FunctionDef,f=""):
    return \
        f+"Any "+sentence.name+"("+util.conv(sentence.args)+")"+"{\n"+\
            util.walk_shallow(sentence.body,f+"  ")+\
        "}\n"

def sent_ret(sentence:ast.Return,f=""):
    return f+"Return "+util.conv(sentence.value)+";\n"

def sent_assign(sentence:ast.Assign):
    ret=""
    tmp=sentence.targets
    tmp=[util.conv(target) for target in tmp]
    tmp=", ".join(tmp)
    ret+=tmp
    ret+=" = "
    ret+=util.conv(sentence.value)
    return ret+";\n"

table={
    "Import":sent_import,
    "FunctionDef":sent_funcdef,
    "Return":sent_ret,
    "Assign":sent_assign,
    "Call":lambda val:expr_call(val)+";\n"
}