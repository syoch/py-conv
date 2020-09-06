import os
import ast
import util
import datamgr

def check():
    #Check dest Folder
    if not os.path.exists("dest/"):
        os.mkdir("dest")
    datamgr.queuemgr.create("srcs")
    datamgr.dictmgr.create("internal")
    datamgr.dictmgr.set("internal","converted",set())

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
    src_name=os.path.splitext(os.path.basename(filename))[0]
    src_file=os.path.abspath(filename)
    dest_file=os.path.join(src_path,"dest",src_name+".cpp")
    print(os.path.relpath(src_file).ljust(25)+"|","->",os.path.relpath(dest_file).ljust(25+5)+"| ",end="... ",flush=True)
    
    if src_file in datamgr.dictmgr.get("internal","converted"):
        print("Already converted |")
    else:
        #Read  src(python)
        os.chdir(os.path.dirname(src_file))
        with open(src_file,"r") as fp:
            src=ast.parse(fp.read(),src_file)
        #Write src(C++)
        fp=open(dest_file,"w")
        fp.write("#include <base>\n")
        for sentence in src.body:
            fp.write(util.conv(sentence,mode=util.modes.SENT))
        fp.close()

        print("done              |")
    
    datamgr.dictmgr.get("internal","converted").add(src_file)
    

# +-----------------------+
# |          Test         |
# +-----------------------+
if __name__ == "__main__":
    check()
    conv("conv.py")
    while not datamgr.queuemgr.empty("srcs"):
        conv(datamgr.queuemgr.get("srcs"))