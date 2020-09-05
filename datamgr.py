from typing import Any
import collections

#Queue

queue={}

def create(name:str) -> None:
    if name in queue:
        raise f"queue `{name}` is already defined"
    queue[name]=collections.deque()

def remove(name:str) -> None:
    if name not in queue:
        raise f"queue `{name}` isn't defined"
    del queue[name]

def get(name:str) ->None:
    if name not in queue:
        raise f"queue `{name}` isn't defined"
    return queue[name]

def push(name:str,data:Any) -> None:
    if not name in queue:
        create(name)
    queue[name].append(data)

def pop(name:str) -> None:
    if not name in queue:
        raise f"queue `{name}` isn't defined"
    return queue[name].pop()

def pushleft(name:str,data:Any) -> None:
    if not name in queue:
        create(name)
    queue[name].appendleft(data)

def popleft(name:str) -> None:
    if not name in queue:
        raise f"queue `{name}` isn't defined"
    return queue[name].popleft()

def have_data(name:str) -> bool:
    if not name in queue:
        return False
    if len(queue[name])==0:
        return False
    else:
        return True

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
    dict_table[name][key]=Any