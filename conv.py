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
    print("Converting",src_file,"->",dest_file)

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

[a+b for a in range(1,10) if a%2==0 for b in range(1,10) if b%2==1]
