from types import ModuleType, FunctionType

import pytoml as toml

from ..dto.DTO import DTO_TYPES
from ..dto.DTO import DTO
from Serializer.serializers.base_serializer import BaseSerializer
from ..parsers.toml_parser import TomlParser
from .. import attributes

class TomlSerializer(BaseSerializer):
    __parser = None

    def __init__(self):
        self.__parser = TomlParser()

    def dump(self, obj, filepath):
        with open(filepath, "w") as file:
            file.write(self.dumps(obj))

    def dumps(self, obj):
        return self._serialize(obj)

    def load(self, filepath):
        with open(filepath, "r") as file:
            return self.loads(file.read())

    def loads(self, source):
        return self.__parser._parse(toml.loads(source))

    def _serialize(self, obj):
        if type(obj) in (int, float, bytes, str, bool, None, type(None)):
            res = self._ser_buf_simp(obj)
        else:
            res = self._choosing_type(obj)
        return toml.dumps(res)

    def _ser_buf_simp(self, obj: any) -> dict:
        res = {}
        if type(obj) in (int, float):
            res[f'{DTO_TYPES.NUMBER}'] = obj
        elif type(obj) == str:
            res[f'{DTO_TYPES.STRING}'] = obj
        elif type(obj) == bytes:
            res[f'{DTO_TYPES.BYTES}'] = obj.hex()
        elif type(obj) == bool:
            res[f'{DTO_TYPES.BOOL}'] = obj
        elif type(obj) == type(None):
            res[f'{DTO_TYPES.NONE}'] = "null"
        return res


    def _choosing_type(self, obj):
        if type(obj) in (int, float, bool, str, bytes, type(None), None):
            if type(obj) == bytes:
                res = obj.hex()
            elif type(obj) == type(None):
                res = "null"
            else:
                res = obj
        elif type(obj) in (list, tuple):
            res = self._ser_list(obj)
        elif type(obj) == dict:
            res = self._ser_dict(obj)
        elif type(obj) == FunctionType:
            res = self._ser_func(obj)
        elif type(obj) == type:
            res = self._ser_class(obj)
        elif type(obj) == ModuleType:
            res = self._ser_module(obj)
        elif isinstance(obj, object):
            res = self._ser_obj(obj)
        return res

    def _ser_list(self, obj) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.LIST}'
        if obj == []:
            return res
        else:
            for i, member in enumerate(obj):
                res[f'item_{i}'] = self._choosing_type(member)
            return res

    def _ser_dict(self, obj) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.DICT}'
        if obj == {}:
            return res
        else:
            for a in obj.items():
                res[a[0]] = self._choosing_type(a[1])
            return res

    def _ser_func(self, obj: FunctionType) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.FUNC}'
        res[f'{DTO.name}'] = self._choosing_type(obj.__name__)
        res[f'{DTO.global_names}'] = self._choosing_type(attributes.get_globals(obj))
        res[f'{DTO.code}'] = self._choosing_type(attributes.get_code_fields(obj.__code__))
        res[f'{DTO.closure}'] = self._choosing_type(obj.__closure__)
        return res

    def _ser_obj(self, obj):
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.OBJ}'
        res[f'{DTO.base_class}'] = self._choosing_type(obj.__class__)
        res[f'{DTO.fields}'] = self._choosing_type(obj.__dict__)
        return res

    def _ser_module(self, obj):
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.MODULE}'
        res[f'{DTO.name}'] = self._choosing_type(obj.__name__)
        if attributes.is_std_lib_module(obj):
            res[f'{DTO.fields}'] = self._choosing_type(None)
        else:
            res[f'{DTO.fields}'] = self._choosing_type(attributes.get_module_fields(obj))
        return res

    def _ser_class(self, obj) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.CLASS}'
        res[f'{DTO.name}'] = self._choosing_type(obj.__name__)
        res[f'{DTO.fields}'] = self._choosing_type(attributes.get_class_fields(obj))
        return res