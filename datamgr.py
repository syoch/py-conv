from typing import Any
import collections

# Value
values={}
def set_val(name:str,value:Any)->None:
    if name in values:
        raise Exception(f"{name} is already defined")
    values[name]=value

def get_val(name:str)->Any:
    if name not in values:
        raise Exception(f"{name} isn't defined")
    return values[name]

#Dict
dict_table={}
class dictmgr: # namespace
    table={}
    @staticmethod
    def create(name:str)->None:
        if name in dictmgr.table:
            raise Exception(f"{name} is already defined")
        dictmgr.table[name]={}

    @staticmethod
    def delete(name:str)->None:
        if name in dictmgr.table:
            raise Exception(f"{name} is already defined")
        del dictmgr.table[name]

    @staticmethod
    def put(name:str,val:Any)->None:
        if name not in dictmgr.table:
            raise Exception(f"{name} is not already defined")
        dictmgr.table[name].append(val)

    @staticmethod
    def getobj(name:str)->Any:
        if name not in dictmgr.table:
            raise Exception(f"{name} is not already defined")
        return dictmgr.table[name]

    @staticmethod
    def get(name:str,key:str)->Any:
        if name not in dictmgr.table:
            raise Exception(f"{name} is not already defined")
        return dictmgr.table[name][key]
    
    @staticmethod
    def set(name:str,key:str,value:Any)->Any:
        if name not in dictmgr.table:
            raise Exception(f"{name} is not already defined")
        dictmgr.table[name][key]=value

# queue
from collections import deque
class queuemgr: # namespace
    table={}
    @staticmethod
    def create(name:str)->None:
        if name in queuemgr.table:
            raise Exception(f"{name} is already defined")
        queuemgr.table[name]=deque()

    @staticmethod
    def put(name:str,val:Any)->None:
        if name not in queuemgr.table:
            raise Exception(f"{name} is not already defined")
        queuemgr.table[name].append(val)

    @staticmethod
    def get(name:str)->Any:
        if name not in queuemgr.table:
            raise Exception(f"{name} is not already defined")
        return queuemgr.table[name].popleft()
    
    @staticmethod
    def empty(name:str) -> Any:
        if name not in queuemgr.table:
            raise Exception(f"{name} is not already defined")
        return len(queuemgr.table[name])==0