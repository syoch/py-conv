import sentences,exprs
def conv(raw):
    typename=raw.__class__.__name__
    if typename in sentences.table:
        return sentences.table[typename](raw)
    elif typename in exprs.table:
        return exprs.table[typename](raw)
    else:
        print("Unknown Type "+typename)
        exit(1)