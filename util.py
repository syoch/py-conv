from datamgr import get
import sentences,exprs,basetype
import enum

class modes(enum.Enum):
    EXPR=0
    SENT=1
    BOTH=2

def conv(raw,mode:modes=modes.BOTH):
    typename=raw.__class__.__name__
    if mode==modes.EXPR:
        if typename in exprs.table:
            return exprs.table[typename](raw)
        else:
            print("Unknown Expr Type "+typename)
            print(get("srcs"))
            exit()
    elif mode==modes.SENT:
        if typename in sentences.table:
            return sentences.table[typename](raw)
        else:
            print("Unknown Sentence Type "+typename)
            print(get("srcs"))
            exit()
    elif mode==modes.BOTH:
        if typename in sentences.table:
            return sentences.table[typename](raw)
        elif typename in exprs.table:
            return exprs.table[typename](raw)
        elif typename in basetype.table:
            return basetype.table[typename](raw)
        else:
            print("Unknown Type "+typename)
            print(get("srcs"))
            exit()

def walk_shallow(obj,f=""):
    tmp=""
    for sentence in obj:
        tmp+=f+conv(sentence)
    return tmp