from types import ModuleType, FunctionType

import yaml
from .. import attributes
from Serializer.parsers import yaml_parser
from Serializer.serializers.base_serializer import BaseSerializer

from ..dto.DTO import DTO_TYPES, DTO


class YamlSerializer(BaseSerializer):
    __parser = None

    def __init__(self):
        self.__parser = yaml_parser.YamlParser()

    def dump(self, obj, filepath):
        with open(filepath, "w") as file:
            file.write(self.dumps(obj))

    def dumps(self, obj):
        return self._serialize(obj)

    def loads(self, source: str) -> any:
        return self.__parser._parse(source)

    def load(self, filepath: str) -> any:
        with open(filepath, 'r') as file:
            return self.loads(file.read())

    def _serialize(self, obj) -> str:
        return yaml.dump(self._choosing_type(obj), sort_keys=False)

    def _choosing_type(self, obj):
        if type(obj) in (int, float, bool, str, bytes, type(None)):
            res = obj
        elif type(obj) in (tuple, list):
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

    def _ser_list(self, obj) -> list:
        res = []
        for a in obj:
            res.append(self._choosing_type(a))
        return res

    def _ser_dict(self, obj) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.DICT}'
        for a in obj.items():
            res[self._choosing_type(a[0])] = self._choosing_type(a[1])
        return res

    def _ser_obj(self, obj) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.OBJ}'
        res[f'{DTO.base_class}'] = self._choosing_type(obj.__class__)
        res[f'{DTO.fields}'] = self._choosing_type(obj.__dict__)
        return res

    def _ser_func(self, obj: FunctionType) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.FUNC}'
        res[f'{DTO.name}'] = self._choosing_type(obj.__name__)
        res[f'{DTO.global_names}'] = self._choosing_type(attributes.get_globals(obj))
        res[f'{DTO.code}'] = self._choosing_type(attributes.get_code_fields(obj.__code__))
        res[f'{DTO.closure}'] = self._choosing_type(obj.__closure__)
        return res

    def _ser_module(self, obj: ModuleType) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.MODULE}'
        res[f'{DTO.name}'] = self._choosing_type(obj.__name__)
        if attributes.is_std_lib_module(obj):
            res[f'{DTO.fields}'] = self._choosing_type(None)
        else:
            res[f'{DTO.fields}'] = self._choosing_type(attributes.get_actual_module_fields(obj))
        return res

    def _ser_class(self, obj: type) -> dict:
        res = {}
        res[f'{DTO.dto_type}'] = f'{DTO_TYPES.CLASS}'
        res[f'{DTO.name}'] = self._choosing_type(obj.__name__)
        class_fields = attributes.get_class_fields(obj)
        res[f'{DTO.fields}'] = self._choosing_type(class_fields)
        return res
