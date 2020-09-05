#Defines analyze of ast expr functions

import ast
import util



def expr_arg(val:ast.arg):
    ret=val.arg
    if val.annotation:
        return util.conv(val.annotation)+" "+ret
    else:
        return "Any "+ret

def expr_args(val:ast.arguments):
    defaults=[None]*(len(val.args)-len(val.defaults))+val.defaults
    tmp=[]
    tmp+=[
            util.conv(a[0])+"="+util.conv(a[1])
            for a in zip(val.args,defaults)
        ]
    if val.vararg != None:tmp+=["*"+util.conv(val.vararg)]
    tmp+=[
            util.conv(a[0])+"="+util.conv(a[1])
            for a in zip(val.kwonlyargs,val.kw_defaults)
        ]
    if val.kwarg != None:tmp+=["**"+util.conv(val.kwarg)]
    return ", ".join(tmp)

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
    return \
        util.conv(val.left,mode=util.modes.EXPR)+\
        " ".join([util.conv(op)+util.conv(val)+" " for (op,val) in zip(val.ops,val.comparators)])[:-1]

def expr_UnaryOp(val:ast.UnaryOp):
    return util.conv(val.op)+" "+util.conv(val.operand,mode=util.modes.EXPR)

def expr_Slice(val:ast.slice):
    tmp=""
    if val.lower!=None:tmp+=util.conv(val.lower)
    tmp+=":"
    if val.upper!=None:tmp+=util.conv(val.upper)
    tmp+=":"
    if val.step!=None:tmp+=util.conv(val.step)
    return "["+tmp+"]"

def expr_Index(val:ast.Index):
    return "["+util.conv(val.value)+"]"

def expr_Subscript(val:ast.Subscript):
    return util.conv(val.value,mode=util.modes.EXPR)+util.conv(val.slice)

def expr_BinOp(val:ast.BinOp):
    return util.conv(val.left)+util.conv(val.op,mode=util.modes.OPER)+util.conv(val.right)

def expr_lambda(val:ast.Lambda):
    return "lambda "+expr_args(val.args)+": "+util.conv(val.body,mode=util.modes.EXPR)

def expr_dict(val:ast.Dict):
    tmp=""
    tmp+="{"
    for k,v in zip(val.keys,val.values):
        tmp+=util.conv(k,mode=util.modes.EXPR)+":"+util.conv(v,mode=util.modes.EXPR)+","
    tmp+="}"
    return tmp

def expr_joinedstr(val:ast.JoinedStr):
    return "".join([util.conv(a,util.modes.EXPR) for a in val.values])

def expr_formattedvalue(val:ast.FormattedValue):
    return (util.conv(val.value))

def expr_BoolOp(val:ast.BoolOp):
    vals=[util.conv(a,mode=util.modes.EXPR) for a in val.values]
    return vals[0]+" "+util.conv(val.op,mode=util.modes.OPER)+" "+vals[1]


def expr_ListComp(val:ast.ListComp):
    tmp="Core::Proc_ListComp("
    chars=", ".join([util.conv(gen.target,mode=util.modes.EXPR) for gen in val.generators])
    tmp+=f"[]({chars})"
    tmp+="{return "+util.conv(val.elt,mode=util.modes.EXPR)+";}, "
    tmp+="{ "
    for i,gen in enumerate(val.generators):
        tmp+="{"
        tmp+=str(i)+","
        tmp+=util.conv(gen.iter,mode=util.modes.EXPR)
        tmp+="},"
    tmp+="},{"
    for i,gen in enumerate(val.generators):
        tmp+="{"
        for cond in gen.ifs:
            tmp+="[]("+util.conv(gen.target,mode=util.modes.EXPR)+"){return "+util.conv(cond,mode=util.modes.EXPR)+";}"
        tmp+="}, "
    tmp=tmp[:-2]
    tmp+="});"
    return tmp

def expr_list(val:ast.List):
    tmp=""
    tmp+="{"
    for elt in val.elts:
        tmp+=util.conv(elt,mode=util.modes.EXPR)
        tmp+=", "
    tmp=tmp[:-2]
    tmp+="}"
    return tmp

table={
    "arguments":expr_args,
    "arg":expr_arg,
    "Attribute":expr_attr,
    "Name":expr_name,
    "Constant":lambda a:util.conv(a.value),
    "Call":expr_call,
    "Compare":expr_comp,
    "UnaryOp":expr_UnaryOp,
    "Slice":expr_Slice,
    "Subscript":expr_Subscript,
    "Index":expr_Index,
    "BinOp":expr_BinOp,
    "Lambda":expr_lambda,
    "Dict":expr_dict,
    "JoinedStr":expr_joinedstr,
    "FormattedValue":expr_formattedvalue,
    "BoolOp":expr_BoolOp,
    "ListComp":expr_ListComp,
    "List":expr_list,
    "Tuple":expr_list
}