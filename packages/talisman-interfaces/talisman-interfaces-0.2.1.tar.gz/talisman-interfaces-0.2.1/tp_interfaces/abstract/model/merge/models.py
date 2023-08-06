from abc import ABCMeta, abstractmethod
from typing import TypeVar

from tp_interfaces.abstract.model import AbstractModel

_MergeModel = TypeVar('_MergeModel', bound='MergeModel')


class MergeModel(AbstractModel, metaclass=ABCMeta):

    @abstractmethod
    def can_be_merged(self, model: AbstractModel) -> bool:
        pass

    @abstractmethod
    def merge(self: _MergeModel, model: AbstractModel) -> _MergeModel:
        pass


class IDBasedMergeModel(MergeModel, metaclass=ABCMeta):

    def can_be_merged(self, model: AbstractModel) -> bool:
        if isinstance(model, IDBasedMergeModel):
            return self.id == model.id
        return False

    @property
    @abstractmethod
    def id(self) -> str:
        pass
