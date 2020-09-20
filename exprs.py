#Defines analyze of ast expr functions

import ast
import util



def expr_arg(val:ast.arg):
    ret=val.arg
    if val.annotation:
        return util.conv(val.annotation,mode=util.modes.EXPR)+" "+ret
    else:
        return "Any "+ret

def expr_args(val:ast.arguments):
    defaults=[None]*(len(val.args)-len(val.defaults))+val.defaults
    tmp=[]
    tmp+=[
            util.conv(a[0],mode=util.modes.EXPR)+"="+util.conv(a[1],mode=util.modes.EXPR)
            for a in zip(val.args,defaults)
        ]
    if val.vararg != None:tmp+=["*"+util.conv(val.vararg,mode=util.modes.EXPR)]
    tmp+=[
            util.conv(a[0],mode=util.modes.EXPR)+"="+util.conv(a[1],mode=util.modes.EXPR)
            for a in zip(val.kwonlyargs,val.kw_defaults)
        ]
    if val.kwarg != None:tmp+=["**"+util.conv(val.kwarg,mode=util.modes.EXPR)]
    return ", ".join(tmp)

def expr_attr(val:ast.Attribute):
    return util.conv(val.value,mode=util.modes.EXPR)+"."+val.attr

def expr_name(val:ast.Name):
    return val.id

def expr_call(val:ast.Call):
    def conv(val):
        a=val.__class__.__name__
        if a=="Call":
            return expr_call(val)
        else:
            return util.conv(val,mode=util.modes.EXPR)
    def cat(a,b):
        if a==None:
            return b
        else:
            return a+"="+b
    tmp=conv(val.func)
    tmp+="("
    tmp+=", ".join([conv(arg) for arg in val.args])
    if len(val.keywords)!=0:
        tmp+=", "
        tmp+=", ".join([cat(keyword.arg,conv(keyword.value)) for keyword in val.keywords])
    tmp+=")"
    return tmp

def expr_comp(val:ast.Compare):
    return \
        util.conv(val.left,mode=util.modes.EXPR)+" "+\
        " ".join([util.conv(op,mode=util.modes.EXPR)+" "+util.conv(val,mode=util.modes.EXPR)+" " for (op,val) in zip(val.ops,val.comparators)])[:-1]

def expr_UnaryOp(val:ast.UnaryOp):
    return util.conv(val.op,mode=util.modes.EXPR)+" "+util.conv(val.operand,mode=util.modes.EXPR)

def expr_Slice(val:ast.slice):
    tmp=""
    if val.lower!=None:tmp+=util.conv(val.lower,mode=util.modes.EXPR)
    tmp+=":"
    if val.upper!=None:tmp+=util.conv(val.upper,mode=util.modes.EXPR)
    tmp+=":"
    if val.step!=None:tmp+=util.conv(val.step,mode=util.modes.EXPR)
    return "["+tmp+"]"

def expr_Index(val:ast.Index):
    return "["+util.conv(val.value,mode=util.modes.EXPR)+"]"

def expr_Subscript(val:ast.Subscript):
    return util.conv(val.value,mode=util.modes.EXPR)+util.conv(val.slice,util.modes.EXPR)

def expr_BinOp(val:ast.BinOp):
    return util.conv(val.left,mode=util.modes.EXPR)+util.conv(val.op,mode=util.modes.EXPR)+util.conv(val.right,mode=util.modes.EXPR)

def expr_lambda(val:ast.Lambda):
    return "[]("+expr_args(val.args)+"){return "+util.conv(val.body,mode=util.modes.EXPR)+";}"

def expr_dict(val:ast.Dict):
    tmp=""
    tmp+="Core::make_dict("
    keys=[]
    values=[]
    for k,v in zip(val.keys,val.values):
        keys.append(util.conv(k,mode=util.modes.EXPR))
        values.append(util.conv(v,mode=util.modes.EXPR))
    tmp+="{"+",".join(keys)+"}"
    tmp+=", "
    tmp+="{"+",".join(values)+"}"
    tmp+=")"
    return tmp

def expr_joinedstr(val:ast.JoinedStr):
    return "+".join([util.conv(a,mode=util.modes.EXPR) for a in val.values])

def expr_formattedvalue(val:ast.FormattedValue):
    return util.conv(val.value,mode=util.modes.EXPR)

def expr_BoolOp(val:ast.BoolOp):
    vals=[util.conv(a,mode=util.modes.EXPR) for a in val.values]
    return vals[0]+" "+util.conv(val.op,mode=util.modes.EXPR)+" "+vals[1]


def expr_ListComp(val:ast.ListComp):
    tmp="Core::ListComp("
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
    tmp+=", ".join([util.conv(elt,mode=util.modes.EXPR) for elt in val.elts])
    tmp+="}"
    return tmp

def expr_ifexp(val:ast.IfExp):
    return util.conv(val.test,mode=util.modes.EXPR)+" ? "+util.conv(val.body,mode=util.modes.EXPR)+" : "+util.conv(val.orelse,mode=util.modes.EXPR)

def expr_starred(val:ast.Starred):
    return "*"+util.conv(val.value,mode=util.modes.EXPR)

def expr_NamedExpr(val:ast.NamedExpr):
    return util.conv(val.target,mode=util.modes.EXPR)+"="+util.conv(val.value,mode=util.modes.EXPR)

def expr_DictComp(val:ast.DictComp):
    s=""
    s+="Core::DictComp("
    s+="{"
    args=set()
    for gen in val.generators:
        s+="{"
        s+=util.conv(gen.iter,mode=util.modes.EXPR)+","
        s+="{"
        s+=",".join([util.conv(ifb,mode=util.modes.EXPR) for ifb in gen.ifs])
        s+="}"
        args.add(util.conv(gen.target,mode=util.modes.EXPR))
        s+="}"
    s+="},"
    args=",".join([f"Any {b}" for b in args])
    s+=f"[]({args}){{{util.conv(val.key,mode=util.modes.EXPR)}}},"
    s+=f"[]({args}){{{util.conv(val.value,mode=util.modes.EXPR)}}}"
    s+=")"
    return s

def expr_set(val:ast.Set):
    vals=[util.conv(a,mode=util.modes.EXPR) for a in val.elts]
    return "["+",".join(vals)+"]"

table={
    "arguments":expr_args,
    "arg":expr_arg,
    "Attribute":expr_attr,
    "Name":expr_name,
    "Constant":lambda x:"Any("+util.conv(x.value,mode=util.modes.EXPR)+")",
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
    "Tuple":expr_list,
    "IfExp":expr_ifexp,
    "Starred":expr_starred,
    "GeneratorExp":expr_ListComp,
    "NamedExpr":expr_NamedExpr,
    "DictComp":expr_DictComp,
    "Set":expr_set
}