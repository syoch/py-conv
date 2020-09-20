table={
    "NoneType":lambda a:"nullptr",
    "str":lambda a:"\""+a.replace("\\","\\\\").replace("\n","\\n").replace("\"","\\\"")+"\"",
    "int":lambda a:str(a),
    "bool":lambda a:"bool",
    "bytes":lambda a:a.decode(),
    "float":lambda a:str(a),
    "ellipsis":lambda a:""
}