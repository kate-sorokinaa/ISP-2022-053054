import imp
import inspect
import re
from types import CodeType, FunctionType, ModuleType

from ..dto.DTO import DTO_TYPES,DTO
from . import json_tokens

TOKEN_TYPES = json_tokens

class JsonParser():
    __tokens: list = []

    def _del_sym(self, token_types: tuple) -> tuple:
        if len(self.__tokens):
            if self.__tokens[0][0] in token_types:
                return self.__tokens.pop(0)
        return ("", "")

    def _head_token(self) -> tuple:
        if len(self.__tokens):
            return self.__tokens[0]

    def _get_arg(self, source: str) -> list:
        res = []
        while len(source) > 0:
            for token in TOKEN_TYPES.TOKEN_REGEXPS.items():
                if token[0] == TOKEN_TYPES.EOF:
                    continue
                try:
                    regexp_res = re.match(token[1], source)
                    if regexp_res.start() == 0:
                        source = str(
                            source[regexp_res.end() - regexp_res.start():]).strip()
                        if token[0] == TOKEN_TYPES.STR:
                            string = regexp_res.group(0)
                            res.append((token[0], string.replace('"', "")))
                        elif token[0] == TOKEN_TYPES.NULL:
                            res.append((token[0], None))
                        elif token[0] == TOKEN_TYPES.NUMBER:
                            num = regexp_res.group(0)
                            num = float(num) if "." in num else int(num)
                            res.append((token[0], num))
                        elif token[0] == TOKEN_TYPES.BOOL:
                            _bool = regexp_res.group(0)
                            res = True if _bool == "true" else False
                            res.append((token[0], res))
                        else:
                            res.append((token[0],))
                except:
                    None
        res.append((TOKEN_TYPES.EOF,))
        return res

    def _skip_field_name(self, comma: bool = False) -> str:
        if comma:
            self._del_sym(TOKEN_TYPES.COMMA)
        field_key = self._del_sym(TOKEN_TYPES.STR)
        self._del_sym(TOKEN_TYPES.COLON)
        return field_key[1]

    def _prs_code(self) -> CodeType:
        self._skip_field_name(comma=True)
        code = self._parse()
        func_code = CodeType(
            int(code["co_argcount"]),
            int(code["co_posonlyargcount"]),
            int(code["co_kwonlyargcount"]),
            int(code["co_nlocals"]),
            int(code["co_stacksize"]),
            int(code["co_flags"]),
            bytes.fromhex(code["co_code"]),
            tuple(code["co_consts"]),
            tuple(code["co_names"]),
            tuple(code["co_varnames"]),
            str(code["co_filename"]),
            str(code["co_name"]),
            int(code["co_firstlineno"]),
            bytes.fromhex(code["co_lnotab"]),
            tuple(code["co_freevars"]),
            tuple(code["co_cellvars"]),
        )
        return func_code

    def _prs_func(self) -> any:
        self._skip_field_name()
        name = self._parse()
        self._skip_field_name(comma=True)
        globals = self._parse()
        self._skip_field_name(comma=True)
        code = self._parse()

        func = FunctionType(code, globals, name)
        func.__globals__["__builtins__"] = __import__("builtins")
        return func

    def _prs_module(self) -> ModuleType:
        self._skip_field_name()
        name = self._parse()
        self._skip_field_name(comma=True)
        fields = self._parse()

        module = None
        if fields == None:
            module = __import__(name)
        else:
            module = imp.new_module(name)
            for field in fields.items():
                setattr(module, field[0], field[1])
        return module

    def _prs_class(self) -> type:
        self._skip_field_name()
        name = self._parse()
        self._skip_field_name(comma=True)
        members = self._parse()

        bases = (object,)
        if "__bases__" in members:
            bases = tuple(members["__bases__"])
        return type(name, bases, members)

    def _prs_obj(self) -> object:
        self._skip_field_name()
        _class = self._parse()
        self._skip_field_name(comma=True)
        fields = self._parse()

        class_init = _class.__init__
        if callable(class_init):
            if class_init.__class__.__name__ == "function":
                delattr(_class, "__init__")
        obj = _class()
        obj.__init__ = class_init
        obj.__dict__ = fields
        return obj

    def _prs_dict(self):
        res = {}
        is_first = True
        while self._head_token()[0] != TOKEN_TYPES.RBRACE:
            co_key = self._skip_field_name(not is_first)
            co_value = self._parse()
            res.update({co_key: co_value})
            is_first = False
        return res

    def _prs_list(self) -> list:
        self._skip_field_name()
        self._del_sym(TOKEN_TYPES.LBRACKET)
        res = []
        is_first = True
        while self._head_token()[0] != TOKEN_TYPES.RBRACKET:
            if not is_first:
                self._del_sym(TOKEN_TYPES.COMMA)
            res.append(self._parse())
            is_first = False
        self._del_sym(TOKEN_TYPES.RBRACKET)
        return res

    def _prs_prim(self) -> any:
        token_type = self._head_token()[0]
        res = None
        if token_type == TOKEN_TYPES.NUMBER:
            res = self._del_sym(TOKEN_TYPES.NUMBER)[1]
        elif token_type == TOKEN_TYPES.STR:
            res = self._del_sym(TOKEN_TYPES.STR)[1]
        elif token_type == TOKEN_TYPES.NULL:
            res = self._del_sym(TOKEN_TYPES.NULL)[1]
        elif token_type == TOKEN_TYPES.BOOL:
            res = self._del_sym(TOKEN_TYPES.BOOL)[1]
        elif token_type in TOKEN_TYPES.LBRACKET:
            res = self._prs_list()
        if self._head_token()[0] == TOKEN_TYPES.COMMA:
            self._del_sym(TOKEN_TYPES.COMMA)
        return res

    def _prs_dto(self):
        self._del_sym(TOKEN_TYPES.LBRACE)

        if self._head_token()[0] == TOKEN_TYPES.RBRACE:
            self._del_sym(TOKEN_TYPES.RBRACE)
            return None

        dto_type_key = self._del_sym(TOKEN_TYPES.STR)
        self._del_sym(TOKEN_TYPES.COLON)
        dto_type_value = self._del_sym(TOKEN_TYPES.STR)
        self._del_sym(TOKEN_TYPES.COMMA)

        res_dto = None

        if dto_type_key[1] == DTO.dto_type:
            if dto_type_value[1] == DTO_TYPES.DICT:
                res_dto = self._prs_dict()
            elif dto_type_value[1] == DTO_TYPES.FUNC:
                res_dto = self._prs_func()
            elif dto_type_value[1] == DTO_TYPES.CODE:
                res_dto = self._prs_code()
            elif dto_type_value[1] == DTO_TYPES.MODULE:
                res_dto = self._prs_module()
            elif dto_type_value[1] == DTO_TYPES.CLASS:
                res_dto = self._prs_class()
            elif dto_type_value[1] == DTO_TYPES.OBJ:
                res_dto = self._prs_obj()

        self._del_sym(TOKEN_TYPES.RBRACE)
        return res_dto

    def _parse(self) -> any:
        head_token_type = self._head_token()[0]
        if head_token_type == TOKEN_TYPES.LBRACE:
            return self._prs_dto()
        return self._prs_prim()

    def parse(self, s: str) -> any:
        self.__tokens = self._get_arg(s)
        return self._parse()
