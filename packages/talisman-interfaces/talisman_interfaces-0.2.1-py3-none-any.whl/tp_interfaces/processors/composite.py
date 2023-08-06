import operator
from operator import attrgetter
from typing import Iterable, Optional, Sequence, Tuple, Type, TypeVar

from pydantic import BaseModel, create_model
from tdm.abstract.datamodel import AbstractTreeDocumentContent
from tdm.datamodel import TalismanDocument

from tp_interfaces.abstract import AbstractCompositeModel, AbstractDocumentProcessor, ImmutableBaseModel
from tp_interfaces.abstract.model.merge import MergeModel

_DocumentContent = TypeVar('_DocumentContent', bound=AbstractTreeDocumentContent)
_Config = TypeVar('_Config', bound=BaseModel)


class SequentialConfig(ImmutableBaseModel):
    pass


class SequentialDocumentProcessor(
    AbstractCompositeModel[AbstractDocumentProcessor],
    AbstractDocumentProcessor[SequentialConfig, _DocumentContent]
):

    def __init__(self, processors: Iterable[Tuple[str, AbstractDocumentProcessor]]):
        processors = tuple(processors)
        AbstractCompositeModel[AbstractDocumentProcessor].__init__(self, map(operator.itemgetter(1), processors))
        AbstractDocumentProcessor.__init__(self)

        config_extractors = []
        config_types = {}
        nonempty_idx = None
        for idx, (model_name, model) in enumerate(processors):
            if not model.config_type.__fields__:
                config = model.config_type()
                config_extractors.append(lambda _: config)
                continue
            if model_name in config_types:
                raise ValueError(f"duplicate model name {model_name}")
            config_types[model_name] = (model.config_type, model.config_type())
            config_extractors.append(attrgetter(model_name))
            nonempty_idx = idx

        if len(config_types) == 1:
            config_extractors[nonempty_idx] = lambda config: config
            self._config_type = next(iter(config_types.values()))[0]
        else:
            if any(not name for name in config_types):
                raise ValueError(f"empty model name couldn't be processed")
            self._config_type = create_model('RuntimeSequentialConfig', **config_types, __base__=SequentialConfig)

        self._config_extractors = tuple(config_extractors)

    def process_doc(self, document: TalismanDocument[_DocumentContent], config: _Config) -> TalismanDocument[_DocumentContent]:
        return self.process_docs([document], config)[0]

    def process_docs(
            self,
            documents: Sequence[TalismanDocument[_DocumentContent]],
            config: SequentialConfig
    ) -> Tuple[TalismanDocument[_DocumentContent], ...]:
        for processor, config_extractor in zip(self._models, self._config_extractors):
            documents = processor.process_docs(documents, config_extractor(config))
        return documents

    @property
    def config_type(self) -> Type[SequentialConfig]:
        return self._config_type

    @classmethod
    def build(cls, processors: Iterable[Tuple[str, AbstractDocumentProcessor]], *, merge: bool = True) -> AbstractDocumentProcessor:
        processors = tuple(_merge_models(processors)) if merge else tuple(processors)
        if len(processors) == 1:
            return processors[0][1]
        return SequentialDocumentProcessor(processors)


def _merge_models(models: Iterable[Tuple[str, AbstractDocumentProcessor]]) -> Iterable[Tuple[str, AbstractDocumentProcessor]]:
    current_merger: Optional[MergeModel] = None
    merger_name: Optional[str] = None
    for name, model in models:
        if current_merger is not None:
            if current_merger.can_be_merged(model):
                current_merger = current_merger.merge(model)
            else:
                yield merger_name, current_merger
                merger_name, current_merger = None, None
        if current_merger is None:
            if isinstance(model, MergeModel):
                merger_name, current_merger = name, model
            else:
                yield name, model
    if current_merger is not None:
        yield merger_name, current_merger
