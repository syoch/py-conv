#Defines analyze of ast sentence functions

import ast
from exprs import expr_args, expr_call, expr_name
import os
import util
import datamgr

def sent_import(sentence:ast.Import,f=""):
    tmp=""
    for a in sentence.names:
        name=a.name
        if os.path.exists(name+".py"):
            tmp+=f+"#include \""+name+".cpp"+"\"\n"
            if not os.path.abspath(name+".py") in datamgr.dictmgr.get("internal","converted"):
                datamgr.queuemgr.put("srcs",os.path.abspath(name+".py"))
        else:
            tmp+=f+"#include <"+name+">\n"
        if a.asname:
            tmp+=f+f"#define {a.asname} {name}\n"
    return tmp

def sent_importfrom(sentence:ast.ImportFrom,f=""):
    tmp=""
    name=sentence.module
    if os.path.exists(name+".py"):
        tmp+=f+"#include \""+name+".cpp"+"\"\n"
        datamgr.queuemgr.put("srcs",os.path.abspath(name+".py"))
    else:
        tmp+=f+"#include <"+name+">\n"
    for a in sentence.names:
        if a.asname:
            tmp+=f+f"#define {a.asname} {a.name}\n"
    return tmp
def sent_funcdef(sentence:ast.FunctionDef,f=""):
    if type(sentence.body[0]) == ast.Expr and type(sentence.body[0].value) == ast.Constant:
        body=sentence.body[1:]
    else:
        body=sentence.body
    return \
        f+"Any "+sentence.name+"("+expr_args(sentence.args)+")"+"{\n"+\
            util.walk_shallow(body,f+"  ")+\
        f+"}\n"

def sent_ret(sentence:ast.Return,f=""):
    return f+"return "+util.conv(sentence.value,mode=util.modes.EXPR)+";\n"

def sent_assign(sentence:ast.Assign,f=""):
    ret=""
    value=util.conv(sentence.value,mode=util.modes.EXPR)
    for i,target in enumerate(sentence.targets):
        ret+=f
        #if util.conv(target,mode=util.modes.EXPR) not in datamgr.dictmgr.get("session","definedVariables"):
        ret+="Any "
        ret+=util.conv(target,mode=util.modes.EXPR)
        ret+=" = "+value
        if len(sentence.targets)!=1:
            ret+="["+str(i)+"]"
        ret+=";\n"
    return ret

def sent_for(sentence:ast.For,f=""):
    return \
        f+"for ("+util.conv(sentence.target,mode=util.modes.EXPR)+" : "+util.conv(sentence.iter,mode=util.modes.EXPR)+"){\n"+\
            util.walk_shallow(sentence.body,f+"  ")+\
        f+"}\n"

def sent_while(sentence:ast.While,f=""):
    return \
        f+"while ("+util.conv(sentence.test,mode=util.modes.EXPR)+"){\n"+\
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
    tmp+=f+f"if({util.conv(sentence.test,mode=util.modes.EXPR)}){{\n"
    tmp+=util.walk_shallow(sentence.body,f=f+"  ")
    tmp+=f+"}"

    #Elif Blocks
    for block in blocks:
        tmp+=f"else if({util.conv(block.test,mode=util.modes.EXPR)}){{\n"
        tmp+=util.walk_shallow(block.body,f+"  ")
        tmp+=f+"}"

    #Else Block
    if len(elseblock)!=0:
        tmp+=f"else{{\n"
        tmp+=util.walk_shallow(elseblock,f+"  ")
        tmp+=f+"}"
    return tmp+"\n"

def sent_with(sentence:ast.With,f=""):
    tmp=""
    tmp+=f+"\n"
    for item in sentence.items:
        tmp+=f+util.conv(item.optional_vars,mode=util.modes.EXPR)+" = "+util.conv(item.context_expr,mode=util.modes.EXPR)+".__enter__();\n"
    
    tmp+=util.walk_shallow(sentence.body,f)

    for item in sentence.items:
        tmp+=f+util.conv(item.optional_vars,mode=util.modes.EXPR)+" = "+util.conv(item.context_expr,mode=util.modes.EXPR)+".__exit__(nullptr,nullptr,nullptr);\n"
    tmp+=f+"\n"
    return tmp

def sent_classdef(sentence:ast.ClassDef,f=""):
    tmp=""
    tmp+=f+"class _"+sentence.name
    if len(sentence.bases) != 0:
        tmp+=": "
    tmp+=", ".join(["public "+util.conv(base,mode=util.modes.EXPR) for base in sentence.bases])
    tmp+="\n"
    tmp+="{\n"

    tmp+=util.walk_shallow(sentence.body,f=f+"  ")
    tmp+="}\n"
    
    decor_proc="_"+sentence.name
    decors=[util.conv(a,mode=util.modes.EXPR) for a in sentence.decorator_list]
    decors.reverse()
    for decor in decors:
        decor_proc=f"{decor}({decor_proc})"
    tmp+=f"#define {sentence.name} {decor_proc}\n"
    
    return tmp

def sent_augAssign(sentence:ast.AugAssign,f=""):
    return f+util.conv(sentence.target,mode=util.modes.EXPR)+util.conv(sentence.op,mode=util.modes.EXPR)+"="+util.conv(sentence.value,mode=util.modes.EXPR)+";\n"

def sent_raise(sentence:ast.Raise,f=""):
    return f+"throw "+util.conv(sentence.exc,mode=util.modes.EXPR)+";\n"
    
def sent_delete(sentence:ast.Delete,f=""):
    return f+"delete" + ", ".join([util.conv(a,mode=util.modes.EXPR) for a in sentence.targets])+";\n"
def sent_try(sentence:ast.Try,f=""):
    s=""
    s+=f+"try{"
    s+=  util.walk_shallow(sentence.body,f+"  ")
    s+=  util.walk_shallow(sentence.finalbody,f+"  ")
    s+=f+"}"
    for handler in sentence.handlers:
        name=handler.name
        if not name:
            name="ex"
        s+=f+"catch("+util.conv(handler.type,mode=util.modes.EXPR)+" "+name+"){"
        s+=  util.walk_shallow(handler.body,f+"  ")
        s+=  util.walk_shallow(sentence.finalbody,f+"  ")
        s+=f+"}"
    if len(sentence.orelse)!=0:
        s+=  util.walk_shallow(sentence.orelse,f)
    return s

def sent_assert(sentence:ast.Assert,f=""):
    return f+"Core::assert("+util.conv(sentence.test,mode=util.modes.EXPR)+","+util.conv(sentence.msg,mode=util.modes.EXPR)+")"

def sent_YieldFrom(sentence:ast.YieldFrom,f=""):
    s=""
    s+=f+"for(Any value:"+util.conv(sentence.value,mode=util.modes.EXPR)+"){"
    s+=f+"  yield value"
    s+=f+"}"
    return s

table={
    "Import":sent_import,
    "ImportFrom":sent_importfrom,
    "FunctionDef":sent_funcdef,
    "Return":sent_ret,
    "Assign":sent_assign,
    "For":sent_for,
    "While":sent_while,
    "If":sent_if,
    "With":sent_with,
    "Expr":lambda a,f="":util.conv(a.value,f=f),
    "Call":lambda val,f="":f+expr_call(val)+";\n",
    "Pass":lambda a,f="": f+"pass\n",
    "ClassDef":sent_classdef,
    "AugAssign":sent_augAssign,
    "Raise":sent_raise,
    "Delete":sent_delete,
    "Break":lambda a,f="":f+"break\n",
    "Try":sent_try,
    "Assert":sent_assert,
    "Continue":lambda a,f="":f+"Continue\n",
    "YieldFrom":sent_YieldFrom
}