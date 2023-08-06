from abc import ABCMeta
from collections import defaultdict
from enum import Enum
from itertools import chain
from typing import Any, DefaultDict, Dict, Iterable, Iterator, List, Optional, Tuple, TypeVar, Union

from pydantic import BaseModel, Extra
from tdm.abstract.datamodel import FactType
from typing_extensions import Literal

from tp_interfaces.abstract import ImmutableBaseModel

_Label = TypeVar("_Label", bound=Any)


class BaseValueType(str, Enum):
    STRING = "String"
    DATE = "Date"
    INT = "Int"
    DOUBLE = "Double"
    GEO = "Geo"
    STRING_LOCALE = "StringLocale"
    LINK = 'Link'

    def __str__(self):
        return self.value


class AbstractSchemaType(ImmutableBaseModel, metaclass=ABCMeta):
    id: str
    name: str
    fact_type: FactType

    class Config:
        extra = Extra.ignore


class NERCRegexp(ImmutableBaseModel):
    regexp: str
    context_regexp: Optional[str] = None


class SchemaConceptType(AbstractSchemaType):
    fact_type: Literal[FactType.CONCEPT] = FactType.CONCEPT
    regexp: Tuple[NERCRegexp, ...] = tuple()
    pretrained_nercmodels: Tuple[str, ...] = tuple()
    dictionary: Tuple[str, ...] = tuple()
    black_list: Tuple[str, ...] = tuple()


class SchemaValueType(SchemaConceptType):
    fact_type: Literal[FactType.VALUE] = FactType.VALUE
    value_type: BaseValueType
    value_restriction: Optional[Tuple[str, ...]]


class RelExtModel(ImmutableBaseModel):
    source_annotation: Optional[str]
    target_annotation: Optional[str]
    relation_type: Optional[str]
    invert_direction: Optional[bool]


class SchemaRelationType(AbstractSchemaType):
    from_id: str
    to_id: str
    pretrained_relext_models: Tuple[RelExtModel, ...] = tuple()
    is_directed: bool = True


AnySchemaType = Union[SchemaConceptType, SchemaValueType, SchemaRelationType]
FACT_TYPE_SCHEMAS = {
    FactType.CONCEPT: SchemaConceptType,
    FactType.VALUE: SchemaValueType,
    FactType.PROPERTY: SchemaRelationType,
    FactType.RELATION: SchemaRelationType
}


class KBSchema:
    def __init__(self, types: Iterable[AnySchemaType]):
        self._id2type: Dict[str, AnySchemaType] = {}
        self._fact_type2type: DefaultDict[FactType, List[AnySchemaType]] = defaultdict(list)

        for type_ in types:
            self._id2type[type_.id] = type_
            self._fact_type2type[type_.fact_type].append(type_)

    def get_type(self, id_: str) -> Optional[AnySchemaType]:
        return self._id2type.get(id_, None)

    def get_types(self, fact_types: Iterable[FactType]) -> Iterator[AnySchemaType]:
        return chain.from_iterable(self._fact_type2type[t] for t in fact_types)

    @classmethod
    def from_config(cls, config: dict) -> 'KBSchema':
        """Config example:
        {
            "types": [
                ... List of serialized `AnySchemaType` objects ...
            ]
        }
        """
        class SoftSchemaType(BaseModel):
            fact_type: FactType

        def convert_to_schema_type(schema_attributes: dict) -> AnySchemaType:
            soft_type = SoftSchemaType.parse_obj(schema_attributes)
            hard_type = FACT_TYPE_SCHEMAS[soft_type.fact_type]
            return hard_type.parse_obj(schema_attributes)

        return cls(map(convert_to_schema_type, config['types']))
