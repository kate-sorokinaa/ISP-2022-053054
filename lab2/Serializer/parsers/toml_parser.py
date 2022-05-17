import imp
from types import CodeType, FunctionType, ModuleType

import toml

from ..dto.DTO import DTO
from ..dto.DTO import DTO_TYPES

class TomlParser():

    def _parse(self, source: dict):
        if len(source) == 1:
            for a in source.items():
                res = self._choosing_type(a[1])
        else:
            res = self._choosing_type(source)
        return res

    def _choosing_type(self, obj):
        if type(obj) in (int, float, bool, str, bytes, type(None), None):
            return self._prs_prim(obj)
        else:
            return self._prs_dto(obj)

    def _prs_prim(self, obj):
        if type(obj) == str:
            if obj == 'null':
                obj = None
        return obj

    def _prs_dto(self, obj: dict):
        if obj[DTO.dto_type] == DTO_TYPES.LIST:
            obj = self._prs_list(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.DICT:
            obj = self._prs_dict(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.FUNC:
            obj = self._prs_func(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.CLASS:
            obj = self._parse(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.OBJ:
            obj = self._prs_obj(obj)
        elif obj[DTO.dto_type] == DTO_TYPES.MODULE:
            obj = self._prs_module(obj)
        return obj

    def _prs_list(self, obj: dict) -> list:
        res = []
        obj.pop(DTO.dto_type)
        for a in obj.items():
            res.append(self._choosing_type(a[1]))
        return res

    def _prs_dict(self, obj: dict) -> dict:
        res = {}
        obj.pop(DTO.dto_type)
        for a in obj.items():
            res[self._choosing_type(a[0])] = self._choosing_type(a[1])
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
            bytes.fromhex(code["co_code"]), tuple(code["co_consts"]),
            tuple(code["co_names"]), tuple(code["co_varnames"]),
            code["co_filename"], code["co_name"],
            code["co_firstlineno"], bytes.fromhex(code["co_lnotab"]),
            tuple(code["co_freevars"]), tuple(code["co_cellvars"]),
        )

        res = FunctionType(res_code, globals, name, closure)
        res.__globals__["__builtins__"] = __import__("builtins")
        return res

    def _prs_obj(self, obj: dict):
        obj.pop(DTO.dto_type)
        base_class = self._choosing_type(obj[DTO.base_class])
        fields = self._choosing_type(obj[DTO.fields])

        init = base_class.__init__
        if callable(init):
            if init.__class__.__name__ == 'function':
                delattr(base_class, "__init__")
        obj = base_class()
        obj.__init__ = init
        obj.__dict__ = fields
        return obj

    def _prs_module(self, obj: dict) -> ModuleType:
        name = self._choosing_type(obj[DTO.name])
        fields = self._choosing_type(obj[DTO.fields])

        if fields == None:
            res = __import__(name)
        else:
            res = imp.new_module(name)
            for a in fields.items():
                setattr(res, a[0], a[1])
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