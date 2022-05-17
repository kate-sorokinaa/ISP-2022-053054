from abc import ABC, abstractmethod


class BaseSerializer(ABC):
    @abstractmethod
    def dump(self, obj, filepath):
        """abmet"""
    @abstractmethod
    def dumps(self, obj) -> str:
        """abmet"""
    @abstractmethod
    def load(self, filepath):
        """abmet"""
    @abstractmethod
    def loads(self, source) -> any:
        """abmet"""
