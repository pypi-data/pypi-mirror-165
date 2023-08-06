from __future__ import annotations
from .SubModel import SubModel
import re
from typing import Iterator, Any, List, Tuple
from .Utilities import Utilities
class Hidden:
    def __new__(cls, input:str) -> Hidden:
        obj=super().__new__(cls)
        obj.input=input
        return obj
    ### Todo

class List_Span:
    def __new__(cls, input:str) ->List_Span:
        pass
    ### ToDo

class node_data:
    __slots__ = ["key","value","data","child"]
    def __new__(cls, key,value):
        obj=super().__new__(cls)
        obj.key=key
        obj.value=value
        obj.child=None
        return obj
    def get(self,key) -> Any:
        return getattr(self,key)
    def repr(self):

        data={}
        data[self.key]=self.data
        return data
    def __repr__(self):
        try:
            data={}
            for name in self:
                data[name]=self.get(name)
            return str(data)
        except:
            return f"{str(self.value), str(self.key)}"
    def __iter__(self) -> Iterator[str]:
        for name in node_data.__slots__:
            if not name.startswith('_'):
                yield name

class ParseModel(object):
    def __init__(self,obj:Any):
        self._obj=obj
        self.json_data=None
    ##get item
    def get(self,key) -> Any:
        return getattr(self._obj,key)
    ## keys function to attract list of items
    def keys(self) -> List[Any]:
        return list(self)
    ### return values of all keys
    def values(self) -> List[Any]:
        return [self[i] for i in self]
    ## return items Iterator
    def items(self) -> Iterator[Tuple[str,Any]]:
        for i in self:
            yield i, self.get(i)
    def __contains__(self, item:Any) -> bool:
        return item in self.keys()
    ## I have to write magic iter in order to get the dictionary of the self
    def __iter__(self) -> Iterator[str]:
        for name in dir(self._obj):
            if not name.startswith('_'):
                yield name
    def data(self,json_data):
        self.json_data=json_data



    @staticmethod
    def __sub_class(cls):
        classes=[cls.__name__ for cls in type(cls).__mro__][1:-1]
        return classes


    def __build_node(self):
        for _key, _value in self.items():
            if isinstance(_value,SubModel):
                child=_value
                child_value=str(child._value)
                value_obj=node_data(_key,child_value)
                value_obj.child=child
            else:
            # setattr(self,key)=node_data(key,value)
                value_obj=node_data(_key,_value)
            self.__setattr__(_key,value_obj)

    def __setattr__(self, key, value):
        self.__dict__[key]=value

    def __getattribute__(self, item):
        return object.__getattribute__(self,item)



    def __build_child_data(self,child_instance,null_value,error_if_null) -> object:
        data=child_instance.data
        sub_child=child_instance.child
        sub_child.data=data

        subclasses=ParseModel.__sub_class(child_instance.child)
        # if len(subclasses)>1:
        return SubModel.build_data(sub_child,null_value,error_if_null)





    def __build_data(self,null_value:Any=None,error_if_null:bool=False) -> Any:
        return_data = {}
        if not isinstance(self.json_data, List):
            self.json_data = [self.json_data]
        ### get each data from this list
        for json_data in self.json_data:
            for key in self:
                child_instance = self.__getattribute__(key)
                try:
                    value=child_instance.value
                    get_data = Utilities.attract_value(json_data, value)
                    child_instance.data=get_data
                    if child_instance.child != None:
                        obj=self.__build_child_data(child_instance, null_value, error_if_null)
                        child_instance.data=obj.data


                except (KeyError, TypeError) as e:
                    if error_if_null == False:
                        if null_value == None:
                            child_instance.data = "None"
                        else:
                            child_instance.data = null_value
                    elif error_if_null == True:
                        raise (e)
            for node in self.list_node():
                return_data[node.key]=node.data
            yield return_data


    def list_node(self):
        for key in self:
            child=self.__getattribute__(key)
            yield child
    def parse(self, null_value:Any=None,error_if_null:bool=False) -> Any:
        self.__build_node()
        for i in self.__build_data(null_value,error_if_null):
            yield i



