from types import FunctionType, ModuleType

from Serializer.serializers.base_serializer import BaseSerializer
from ..parsers.json_parser import JsonParser
from ..dto.DTO import DTO_TYPES
from ..dto.DTO import DTO
from .. import attributes


class JsonSerializer(BaseSerializer):
    __result = ""
    __parser = None

    def __init__(self):
        self.__parser = JsonParser()

    def dump(self, obj, filepath):
        with open(filepath, "w") as file:
            file.write(self.dumps(obj))

    def dumps(self, obj) -> str:
        self._choosing_type(obj)
        return self.__result

    def load(self, filepath):
        with open(filepath, "r") as file:
            return self.loads(file.read())

    def loads(self, source) -> any:
        return self.__parser.parse(source)

    def _sym(self, symbol):
        self.__result += symbol

    def _choosing_type(self, obj):
        if type(obj) in (int, float, bool, bytes, str):
            self._ser_prim(obj)
        elif type(obj) in (list, tuple):
            self._ser_lt(obj)
        elif obj == None:
            self._sym("null")
        else:
            self._sym("{")
            if type(obj) == dict:
                self._ser_dict(obj)
            elif type(obj) == FunctionType:
                self._ser_func(obj)
            elif type(obj) == type:
                self._ser_class(obj)
            elif type(obj) == ModuleType:
                self._ser_module(obj)
            elif isinstance(obj, object):
                self._ser_obj(obj)
            self._sym("}")

    def _ser_prim(self, obj):
        obj_type = type(obj)
        if obj_type in (int, float):
            self._sym(f'{obj}')
        elif obj_type == bool:
            if obj:
                self._sym("true")
            else:
                self._sym("false")
        elif obj_type == str:
            self._sym(f'"{obj}"')
        elif obj_type == bytes:
            self._sym(f'"{obj.hex()}"')

    def _ser_lt(self, obj):
        if (len(obj)) == 0:
            self._sym('[]')
        else:
            self._sym('[')
            for i, a in enumerate(obj):
                if i != 0:
                    self._sym(',')
                self._choosing_type(a)
            self._sym(']')

    def _ser_dict(self, obj: dict):
        self._sym(f'"{DTO.dto_type}": "{DTO_TYPES.DICT}"')
        if len(obj) >= 1:
            self._sym(",")
            is_first = True
            i = 0

        for key, value in obj.items():
            if is_first != True:
                self._sym(',')
            self._choosing_type(key)
            self._sym(': ')
            self._choosing_type(value)
            is_first = False

    def _ser_func(self, obj):
        self._sym(f'"{DTO.dto_type}": "{DTO_TYPES.FUNC}",')
        self._sym(f'"{DTO.name}": "{obj.__name__}",')
        self._sym(f'"{DTO.global_names}": ')
        self._choosing_type(attributes.get_globals(obj))
        self._sym(',')
        self._ser_code(obj)
        self._sym(',')
        self._sym(f'"{DTO.closure}": "{obj.__closure__}"')

    def _ser_code(self, obj):
        self._sym(f'"{DTO.code}": ')
        self._sym('{')
        self._sym(f'"{DTO.dto_type}": "{DTO_TYPES.CODE}",')
        self._sym(f'"{DTO.fields}": ')
        self._choosing_type(attributes.get_code_fields(obj.__code__))
        self._sym('}')

    def _ser_obj(self, obj):
        self._sym(f'"{DTO.dto_type}": "{DTO_TYPES.OBJ}",')
        self._sym(f'"{DTO.base_class}": ')
        self._choosing_type(obj.__class__)
        self._sym(",")
        self._sym(f'"{DTO.fields}": ')
        self._choosing_type(obj.__dict__)

    def _ser_class(self, obj):
        self._sym(f'"{DTO.dto_type}": "{DTO_TYPES.CLASS}",')
        self._sym(f'"{DTO.name}": "{obj.__name__}",')
        self._sym(f'"{DTO.fields}": ')
        self._choosing_type(attributes.get_class_fields(obj))

    def _ser_module(self, obj):
        self._sym(f'"{DTO.dto_type}": "{DTO_TYPES.MODULE}",')
        self._sym(f'"{DTO.name}": "{obj.__name__}",')
        self._sym(f'"{DTO.fields}": ')
        if attributes.is_std_lib_module(obj):
            self._choosing_type(None)
        else:
            self._choosing_type(attributes.get_module_fields(obj))

