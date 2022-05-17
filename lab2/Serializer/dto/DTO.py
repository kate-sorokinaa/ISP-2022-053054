from dataclasses import dataclass


@dataclass
class DTO:
    dto_type = "DTO_TYPE"
    name = "name"
    fields = "fields"
    path = "path"
    code = "code"
    global_names = "globals"
    base_class = "class"
    closure = "closure"


@dataclass
class DTO_TYPES:
    FUNC = "func"
    CODE = "code"
    MODULE = "module"
    CLASS = "class"
    OBJ = "obj"
    DICT = "dict"
    LIST = "list"
    NUMBER = "number"
    STRING = "str"
    BYTES = "bytes"
    BOOL = "bool"
    NONE = "none"
