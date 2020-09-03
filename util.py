from datamgr import get
import sentences,exprs,basetype,operators
import enum

class modes(enum.Enum):
    EXPR=0
    SENT=1
    BOTH=2
    OPER=3

def conv(raw,f="",mode:modes=modes.BOTH):
    typename=raw.__class__.__name__
    if mode==modes.EXPR:
        if typename in exprs.table:
            return exprs.table[typename](raw)
        else:
            print("Unknown Expr Type "+typename)
            print(get("srcs"))
            exit(0)
    elif mode==modes.SENT:
        if typename in sentences.table:
            return sentences.table[typename](raw,f=f)
        else:
            print("Unknown Sentence Type "+typename)
            print(get("srcs"))
            exit(0)
    elif mode==modes.OPER:
        if typename in operators.table:
            return operators.table[typename]
        else:
            print("Unknown Operator Type "+typename)
            print(get("srcs"))
            exit(0)
    elif mode==modes.BOTH:
        if typename in sentences.table:
            return sentences.table[typename](raw,f=f)
        elif typename in exprs.table:
            return exprs.table[typename](raw)
        elif typename in basetype.table:
            return basetype.table[typename](raw)
        elif typename in operators.table:
            return operators.table[typename]
        else:
            print("Unknown Type "+typename)
            print(get("srcs"))
            exit(0)

def walk_shallow(obj,f=""):
    tmp=""
    for sentence in obj:
        tmp+=str(conv(sentence,f))
    return tmp