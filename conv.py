import os
import ast
import util
import datamgr
import argparse

out="dest/"
basemode=False

def check():
    #Check dest Folder
    if not os.path.exists("dest/"):
        os.mkdir("dest")
    datamgr.queuemgr.create("srcs")
    datamgr.dictmgr.create("internal")
    datamgr.dictmgr.set("internal","converted",set())

def _conv(filename:str):
    """
    Convert python to c++ source code

    Parameter

       Name  | Description|Type
    ---------+------------+-----
    filename |   source   | str

    Returns:None
    """
    
    src_abs=os.path.abspath(filename)
    src_rel=os.path.relpath(filename)
    if basemode:
        tmp=os.path.basename(src_rel)
    else:
        tmp=os.path.splitext(src_rel)[0]
    out_file=out+os.path.sep+tmp+".cpp"
    src_file=src_abs
    print(src_rel.ljust(25)+"|",os.path.relpath(out_file).ljust(25+5)+"| ",end="",flush=True)
    

    if src_file in datamgr.dictmgr.get("internal","converted"):
        print("Already converted |")
    else:
        #Read  src(python)
        with open(src_file,"r") as fp:
            src=ast.parse(fp.read(),src_file)
        #Write src(C++)
        fp=open(out_file,"w")
        fp.write("#include <base>\n")
        for sentence in src.body:
            fp.write(util.conv(sentence,mode=util.modes.SENT))
        fp.close()
        
        print("done              |")
    
    datamgr.dictmgr.get("internal","converted").add(src_file)
    
def conv(filename:str):
    _conv(filename)
    while not datamgr.queuemgr.empty("srcs"):
        _conv(datamgr.queuemgr.get("srcs"))

def main():
    global out,basemode

    check()
    parser=argparse.ArgumentParser(
        description="Transcompile python source code into C++ source code"
    )

    group=parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-d","--directory",
        help="Convert directory",
        nargs="?",
        type=str,
        default=None,
        const="libs",
        metavar="dir"
    )
    
    group.add_argument(
        "-f","--file",
        help="Convert python script",
        type=str
    )

    parser.add_argument(
        "-o","--outputDir",
        help="folder for output",
        type=str,
        default="dest"
    )

    parser.add_argument(
        "-b","--basename",
        help="output filename contains basename only",
        action="store_true"
    )

    ns=parser.parse_args()

    out=ns.outputDir
    if ns.basename:
        basemode=True
    if ns.directory:
        import glob
        for filename in glob.glob(ns.directory+"/*"):
            conv(filename)

    if ns.file:
        conv(ns.file)


if __name__ == "__main__":
    main()