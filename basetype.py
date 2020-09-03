table={
    "NoneType":lambda a:"nullptr",
    "str":lambda a:"\""+a.replace("\n","\\n")+"\"",
    "int":lambda a:str(a),
}