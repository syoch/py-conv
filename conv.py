import os
import ast
import util
import datamgr

a=lambda x:print("a",x)
b=lambda x:print("b",x)
c=lambda x:print("c",x)
@a
@b
@c
class test(ast.expr):
    pass

print(test)

def check():
    #Check dest Folder
    if not os.path.exists("dest/"):
        os.mkdir("dest")

def conv(filename:str):
    """
    Convert python to c++ source code

    Parameter

       Name  | Description|Type
    ---------+------------+-----
    filename |   source   | str

    Returns:None
    """
    src_path=os.path.split(os.path.abspath(filename))[0]
    src_name=os.path.splitext(filename)[0]

    src_file=os.path.abspath(filename)
    dest_file=os.path.join(src_path,"dest",src_name+".cpp")

    os.chdir(os.path.dirname(src_file))

    with open(src_file,"r") as fp:
        src=ast.parse(fp.read(),src_file)

    datamgr.pushleft("srcs",src_file)

    fp=open(dest_file,"w")
    fp.write("#include <base>\n")
    for sentence in src.body:
        fp.write(util.conv(sentence,mode=util.modes.SENT))
    fp.close()
    datamgr.popleft("srcs")

# +-----------------------+
# |          Test         |
# +-----------------------+
if __name__ == "__main__":
    check()
    conv("conv.py")
    while datamgr.have_data("srcs"):
        conv(os.path.relpath(datamgr.popleft("srcs")))

def a(a): # Test
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
        if a/2==2:
            print("a/2==2")
    return None
