from datamgr import get
import sentences,exprs,basetype

def conv(raw):
    typename=raw.__class__.__name__
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