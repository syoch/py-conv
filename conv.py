import ast
import util
import datamgr

def a(a,b=1,*,c,d=1,**e): # Test
    if a==0:
        print("a==0")
    elif a==1:
        print("a==1")
    elif a==2:
        print("a==2")
    elif a==3:
        print("a==3")
    else:
        print("else")
    if a==4:
        print("a==4")
    return None

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