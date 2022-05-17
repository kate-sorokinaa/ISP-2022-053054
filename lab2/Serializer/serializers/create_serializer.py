from Serializer.serializers.json_serializer import JsonSerializer
from Serializer.serializers.yaml_serializer import YamlSerializer
from Serializer.serializers.toml_serializer import TomlSerializer
from Serializer.serializers.base_serializer import BaseSerializer

SERIALIZERS_MAP = {
    "json": JsonSerializer,
    "toml": TomlSerializer,
    "yaml": YamlSerializer
}


def create_serializer(exten_name: str) -> BaseSerializer:
    if exten_name in SERIALIZERS_MAP:
        return SERIALIZERS_MAP[exten_name]()
    else:
        return None
