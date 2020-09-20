def bytes2str(b):
    s=""
    for a in b:
        s+=chr(a)
    return s
table={
    "NoneType":lambda a:"nullptr",
    "str":lambda a:"\""+a.replace("\\","\\\\").replace("\n","\\n").replace("\"","\\\"")+"\"",
    "int":lambda a:str(a),
    "bool":lambda a:"bool",
    "bytes":bytes2str,
    "float":lambda a:str(a),
    "ellipsis":lambda a:""
}