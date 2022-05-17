import imp
from types import CodeType, FunctionType, ModuleType

import yaml

from ..dto.DTO import DTO
from ..dto.DTO import DTO_TYPES


class YamlParser():

    def _parse(self, txt):
        return self._choosing_type(yaml.full_load(txt))

    def _choosing_type(self, obj: any) -> any:
        if type(obj) in (int, float, bool, str, bytes, type(None)):
            res = obj
        elif type(obj) == list:
            res = self._prs_list(obj)
        else:
            res = self._prs_dto(obj)
        return res

    def _prs_list(self, obj: list) -> list:
        res = []
        for a in obj:
            res.append(self._choosing_type(a))
        return res

    def _prs_dto(self, obj: any) -> any:
        if obj[DTO.dto_type] == DTO_TYPES.DICT:
            obj = self._prs_dict(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.FUNC:
            obj = self._prs_func(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.CLASS:
            obj = self._prs_class(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.OBJ:
            obj = self._prs_obj(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.MODULE:
            obj = self._prs_module(obj)
        return obj

    def _prs_dict(self, obj: dict) -> dict:
        res = {}
        obj.pop(DTO.dto_type)
        for a in obj.items():
            res[self._choosing_type(a[0])] = self._choosing_type(a[1])
        return res

    def _prs_class(self, obj) -> type:
        obj.pop(DTO.dto_type)
        name = self._choosing_type(obj[DTO.name])
        fields = self._choosing_type(obj[DTO.fields])
        bases = (object,)
        if "__bases__" in fields:
            bases = tuple(fields["__bases__"])
        res = type(name, bases, fields)
        return res

    def _prs_func(self, obj: dict) -> FunctionType:
        obj.pop(DTO.dto_type)
        name = self._choosing_type(obj[DTO.name])
        globals = self._choosing_type(obj[DTO.global_names])
        code = self._choosing_type(obj[DTO.code])
        closure = self._choosing_type(obj[DTO.closure])

        res_code = CodeType(
            code["co_argcount"], code["co_posonlyargcount"],
            code["co_kwonlyargcount"], code["co_nlocals"],
            code["co_stacksize"], code["co_flags"],
            code["co_code"], tuple(code["co_consts"]),
            tuple(code["co_names"]), tuple(code["co_varnames"]),
            code["co_filename"], code["co_name"],
            code["co_firstlineno"], code["co_lnotab"],
            tuple(code["co_freevars"]), tuple(code["co_cellvars"]),
        )

        res = FunctionType(res_code, globals, name, closure)
        res.__globals__["__builtins__"] = __import__("builtins")
        return res


    def _prs_obj(self, obj: dict) -> any:
        obj.pop(DTO.dto_type)
        base_class = self._choosing_type(obj[DTO.base_class])
        fields = self._choosing_type(obj[DTO.fields])

        class_init = base_class.__init__
        if callable(class_init):
            if class_init.__class__.__name__ == 'function':
                delattr(base_class, "__init__")
        obj = base_class()
        obj.__init__ = class_init
        obj.__dict__ = fields
        return obj

    def _prs_module(self, obj: dict) -> ModuleType:
        name = self._choosing_type(obj[DTO.name])
        fields = self._choosing_type(obj[DTO.fields])

        if fields == None:
            module = __import__(name)
        else:
            module = imp.new_module(name)
            for field in fields.items():
                setattr(module, field[0], field[1])
        return module
