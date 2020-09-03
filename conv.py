import os
import ast
import util
import datamgr

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

    datamgr.push("srcs",src_file)

    fp=open(dest_file,"w")
    for sentence in src.body:
        fp.write(util.conv(sentence,mode=util.modes.SENT))
    fp.close()
    os.system("cat dest/conv.cpp")

# +-----------------------+
# |          Test         |
# +-----------------------+
if __name__ == "__main__":
    check()
    conv("conv.py")


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
