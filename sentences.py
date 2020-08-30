#Defines analyze of ast sentence functions

import ast
import os
import util
import datamgr

def sent_import(sentence:ast.Import):
    tmp=""
    for a in sentence.names:
        name=util.conv(a)
        if os.path.exists(name+".py"):
            tmp+="#include \""+name+".cpp"+"\"\n"
            datamgr.push("srcs",name+".py")
        else:
            tmp+="#include <"+name+">\n"
    return tmp

def sent_funcdef(sentence:ast.FunctionDef):
    return "Any "+sentence.name+"("+util.conv(sentence.args)+")"+"\n"
    #print(sentence.body)

table={
    "Import":sent_import,
    "FunctionDef":sent_funcdef
}