from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, Iterable, Optional, TypeVar

from tdm.abstract.datamodel import AbstractTreeDocumentContent
from tdm.datamodel import TalismanDocument

from .processor import AbstractDocumentProcessor

_DocumentContent = TypeVar('_DocumentContent', bound=AbstractTreeDocumentContent)
_Processor = TypeVar('_Processor', bound=AbstractDocumentProcessor)


class AbstractTrainer(Generic[_Processor, _DocumentContent], metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, config: dict):
        pass

    @abstractmethod
    def train(
            self,
            train_docs: Iterable[TalismanDocument[_DocumentContent]],
            dev_docs: Iterable[TalismanDocument[_DocumentContent]] = None
    ) -> _Processor:
        pass

    @property
    @abstractmethod
    def score(self) -> Optional[Dict[str, float]]:
        """Development set score of the last trained model.
        Is None if no development set was provided or model has not been trained yet

        Score is a mapping: `score_name` -> `score_value`
        """
        pass
