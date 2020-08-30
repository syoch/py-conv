#Defines analyze of ast sentence functions

import ast
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
    return f+"Any "+sentence.name+"("+util.conv(sentence.args)+")"+"\n"+util.walk_shallow(sentence.body,f+"  ")

table={
    "Import":sent_import,
    "FunctionDef":sent_funcdef
}