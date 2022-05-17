import imp
import inspect
import sys
from types import CodeType, ModuleType, WrapperDescriptorType, MethodDescriptorType, BuiltinFunctionType, \
    MappingProxyType, GetSetDescriptorType


def get_globals(obj) -> dict:
    res = {}
    for glob in obj.__globals__.items():
        if glob[0] in obj.__code__.co_names:
            res.update({glob[0]: glob[1]})
    return res


def get_module_fields(module: ModuleType) -> dict:
    module_fields = {}
    module_members = inspect.getmembers(module)
    for mem in module_members:
        if not mem[0].startswith("__"):
            module_fields.update({mem[0]: mem[1]})
    return module_fields

def get_code_fields(_code: CodeType) -> dict:
    res = dict()
    for a in inspect.getmembers(_code):
        if str(a[0]).startswith("co_"):
            res.update({a[0]: a[1]})
    return res


def get_actual_module_fields(module: ModuleType) -> dict:
    fields = {}
    for a in inspect.getmembers(module):
        if not a[0].startswith("__"):
            fields.update({a[0]: a[1]})
    return fields


def is_std_lib_module(module: ModuleType):
    python_libs_path = sys.path[2]
    module_path = imp.find_module(module.__name__)[1]
    if module.__name__ in sys.builtin_module_names:
        return True
    elif python_libs_path in module_path:
        return True
    elif 'site-packages' in module_path:
        return True
    return False

def get_class_fields(obj) -> dict:
    fields = dict()
    if obj == type:
        fields["__bases__"] = []
    else:

        for a in inspect.getmembers(obj):
            if type(a[1]) not in (
                WrapperDescriptorType,
                MethodDescriptorType,
                BuiltinFunctionType,
                MappingProxyType,
                GetSetDescriptorType
            ) and a[0] not in (
                "__mro__", "__base__", "__basicsize__",
                "__class__", "__dictoffset__", "__name__",
                "__qualname__", "__text_signature__", "__itemsize__",
                "__flags__", "__weakrefoffset__"
            ):
                fields[a[0]] = a[1]
    return fields
