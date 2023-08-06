from typing import Any, List, Iterator
from .Utilities import Utilities

class SubModel:
    exclude=["build_data","data", "exclude"]
    def __new__(cls, value):
        obj = super().__new__(cls)
        obj._value = value
        return obj

    def __getattribute__(self, item):
        return object.__getattribute__(self,item)
    def __iter__(self) -> Iterator[str]:
        for name in dir(self):
            if not name.startswith('_'):
                if name not in SubModel.exclude:
                    yield name


    @staticmethod
    def build_data(obj: object, null_value:Any=None,error_if_null:bool=False) -> object:
        return_data=[]
        if not isinstance(obj.data, List):
            obj.data=[obj.data]
        ### get each data from this list
        for _data in obj.data:
            data_json={}

            for key in obj:
                try:
                    value=obj.__getattribute__(key)
                    get_data = Utilities.attract_value(_data, value)
                    data_json[key]=get_data
                except (KeyError, TypeError) as e:
                    if error_if_null == False:
                        if null_value == None:
                            data_json[key] = "None"
                        else:
                            data_json[key] = null_value
                    elif error_if_null == True:
                        raise (e)
            return_data.append(data_json)
        obj.data=return_data
        return obj




