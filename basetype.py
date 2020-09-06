table={
    "NoneType":lambda a:"nullptr",
    "str":lambda a:"\""+a.replace("\n","\\n").replace("\"","\\\"")+"\"",
    "int":lambda a:str(a),
    "bool":lambda a:"bool"
}