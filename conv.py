import ast
import util
import datamgr

def a(c,d=1,*,e,f=1,**b):
    return None

def eval_sentence(sentence:ast.stmt):
    print(util.conv(sentence),end="")

def conv(filename:str,dest:str):
    """
    Convert python to c++ source code

    Parameter

       Name  | Description|Type
    ---------+------------+-----
    filename |   source   | str
    dest     |   dest     | str

    Returns:None
    """
    fp=open(filename,"r")
    data=fp.read()
    fp.close()

    src=ast.parse(data,filename)
    datamgr.push("srcs",filename)

    for sentence in src.body:
        print(util.conv(sentence,util.modes.SENT),end="")

# +-----------------------+
# |          Test         |
# +-----------------------+
if __name__ == "__main__":
    conv("conv.py","dest.cpp")