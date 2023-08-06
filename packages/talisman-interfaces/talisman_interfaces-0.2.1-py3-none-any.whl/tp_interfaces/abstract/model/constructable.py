from abc import abstractmethod
from typing import Type, TypeVar

from .model import AbstractModel

_Model = TypeVar('_Model', bound='AbstractConfigConstructableModel')


class AbstractConfigConstructableModel(AbstractModel):
    @classmethod
    @abstractmethod
    def from_config(cls: Type[_Model], config: dict) -> _Model:
        pass
