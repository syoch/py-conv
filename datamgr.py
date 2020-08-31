from typing import Any

#Queue

queue={}

def create(name:str) -> None:
    if name in queue:
        raise f"queue `{name}` is already defined"
    queue[name]=[]

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