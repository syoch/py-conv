import ast
import util

def eval_sentence(sentence:ast.stmt):
    print(util.conv(sentence))

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

    for sentence in src.body:
        eval_sentence(sentence)

# +-----------------------+
# |          Test         |
# +-----------------------+
if __name__ == "__main__":
    conv("conv.py","dest.cpp")