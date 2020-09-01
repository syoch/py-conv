#Defines analyze of ast sentence functions

import ast
from exprs import expr_args, expr_call
import os
import util
import datamgr

def sent_import(sentence:ast.Import,f=""):
    tmp=""
    for a in sentence.names:
        name=util.conv(a)[1:-1]
        if os.path.exists(name+".py"):
            tmp+=f+"#include \""+name+".cpp"+"\"\n"
            datamgr.push("srcs",name+".py")
        else:
            tmp+=f+"#include <"+name+">\n"
    return tmp

def sent_funcdef(sentence:ast.FunctionDef,f=""):
    return \
        f+"Any "+sentence.name+"("+expr_args(sentence.args)+")"+"{\n"+\
            util.walk_shallow(sentence.body,f+"  ")+\
        "}\n"

def sent_ret(sentence:ast.Return,f=""):
    return f+"Return "+util.conv(sentence.value,util.modes.EXPR)+";\n"

def sent_assign(sentence:ast.Assign,f=""):
    ret=""
    tmp=sentence.targets
    tmp=[util.conv(target,util.modes.EXPR) for target in tmp]
    tmp=", ".join(tmp)
    ret+=tmp
    ret+=" = "
    ret+=util.conv(sentence.value,util.modes.EXPR)
    return f+ret+";\n"

def sent_for(sentence:ast.For,f=""):
    return \
        f+"for ("+util.conv(sentence.target,util.modes.EXPR)+" in "+util.conv(sentence.iter,util.modes.EXPR)+"){\n"+\
            util.walk_shallow(sentence.body,f+"  ")+\
        f+"}\n"
def sent_if(sentence:ast.If,f=""):
    elif_list=[]

    #Make Elif Block list
    tmp=sentence.orelse
    while len(tmp)!=0 and type(tmp[0])==ast.If and len(tmp[0].orelse)!=0:
        elif_list.append(tmp)
        tmp=tmp[0].orelse
    blocks=[a[0] for a in elif_list]

    elseblock=tmp


    tmp=""
    #If Block
    tmp+=f+f"if({util.conv(sentence.test)}){{\n"
    tmp+=f+"  "+util.walk_shallow(sentence.body,f+"  ")+f+"  }"

    #Elif Blocks
    for block in blocks:
        tmp+=f+f"else if({util.conv(block.test)}){{\n"
        tmp+=f+"  "+util.walk_shallow(block.body,f+"  ")+f+"  }"

    #Else Block
    if len(elseblock)!=0:
        tmp+=f+f"else{{\n"
        tmp+=f+"  "+util.walk_shallow(elseblock,f+"  ")+f+"  }"
    
    return tmp+"\n"

table={
    "Import":sent_import,
    "FunctionDef":sent_funcdef,
    "Return":sent_ret,
    "Assign":sent_assign,
    "Call":lambda val,f="":f+expr_call(val)+";\n",
    "For":sent_for,
    "If":sent_if
}