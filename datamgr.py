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
def create_dict(name:str) -> None:
    if name in dict_table:
        raise f"dict `{name}` is already defined"
    dict_table[name]={}

def remove_dict(name:str) -> None:
    if name not in dict_table:
        raise f"dict `{name}` isn't defined"
    del dict_table[name]

def getobj_dict(name:str) ->None:
    if name not in dict_table:
        raise f"dict `{name}` isn't defined"
    return dict_table[name]

def get_dict(name:str,key:str) ->None:
    if name not in dict_table:
        raise f"dict `{name}` isn't defined"
    return dict_table[name][key]

def set_dict(name:str,key:str,value:Any) ->None:
    if name not in dict_table:
        raise f"dict `{name}` isn't defined"
    dict_table[name][key]=value

# queue
from collections import deque
class queue: # namespace
    table={}
    @staticmethod
    def create(name:str)->None:
        if name in queue.table:
            raise Exception(f"{name} is already defined")
        queue.table[name]=deque()

    @staticmethod
    def put(name:str,val:Any)->None:
        if name not in queue.table:
            raise Exception(f"{name} is not already defined")
        queue.table[name].append(val)

    @staticmethod
    def get(name:str)->Any:
        if name not in queue.table:
            raise Exception(f"{name} is not already defined")
        return queue.table[name].popleft()
    
    @staticmethod
    def empty(name:str) -> Any:
        if name not in queue.table:
            raise Exception(f"{name} is not already defined")
        return len(queue.table[name])==0