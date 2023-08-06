from collections import Counter, defaultdict
from typing import Counter as TypingCounter, DefaultDict, Dict, Iterable, Tuple, Type

from tdm.abstract.datamodel import AbstractTalismanDocument, AbstractTalismanSpan, AbstractTreeDocumentContent
from tdm.datamodel import CreateConceptDirective
from tdm.datamodel.fact import ConceptFact

from tp_interfaces.abstract import ImmutableBaseModel
from tp_interfaces.knowledge_base.interfaces import DBConcept, KB, MentionCandidates, MentionConceptFeatures
from tp_interfaces.knowledge_base.kb_schema import KBSchema


EMPTY_SCHEMA = KBSchema(tuple())


class DMBCommonnessStub(KB[ImmutableBaseModel]):
    def __init__(self, kb_schema: KBSchema = EMPTY_SCHEMA):
        self._id2concept: Dict[str, DBConcept] = {}
        self._mention2ids_counter: DefaultDict[str, TypingCounter[DBConcept]] = defaultdict(Counter)
        self._kb_schema = kb_schema

    def __exit__(self, *exc):
        pass

    def bind_facts_and_load_docs(self, docs: Iterable[AbstractTalismanDocument]):
        for doc in docs:
            for directive in doc.filter_directives(CreateConceptDirective):
                self._load_directive(directive)

        for doc in docs:
            for fact in doc.filter_facts(ConceptFact, lambda f: isinstance(f.value, str) and f.mention is not None):
                concept = fact.value
                if concept not in self._id2concept:
                    raise ValueError(f"Provided document {doc.doc_id} contains concept not in KB: concept id = {concept}")

                self._mention2ids_counter[self._build_mention(doc.content, fact.mention)][concept] += 1

    def _load_directive(self, directive: CreateConceptDirective):
        self._id2concept[directive.id] = DBConcept(directive.id, directive.name, directive.concept_type)
        self._mention2ids_counter[directive.name][directive.id] += 1

    @staticmethod
    def _build_mention(content: AbstractTreeDocumentContent, mention: Tuple[AbstractTalismanSpan, ...]) -> str:
        return " ".join(content.text_for(span) for span in mention)

    def _compute_mention_candidates(self, mention: str) -> MentionCandidates:
        candidates_counter = self._mention2ids_counter[mention]  # Counter[candidate_id, candidate_occ_num]
        mention_occs = sum(candidates_counter.values())
        candidate2feats = dict()
        for candidate_id, candidate_occs in candidates_counter.items():
            candidate = self._id2concept[candidate_id]
            candidate2feats[candidate] = MentionConceptFeatures(candidate_occs / mention_occs)

        return MentionCandidates(candidate2feats)

    def get_candidates(self, doc: AbstractTalismanDocument, config: ImmutableBaseModel) -> Dict[ConceptFact, MentionCandidates]:
        ret = {}
        for fact in doc.filter_facts(ConceptFact, lambda f: not f.value and f.mention is not None):  # facts without values only
            mention_str = self._build_mention(doc.content, fact.mention)
            if mention_str not in self._mention2ids_counter:
                continue
            ret[fact] = self._compute_mention_candidates(mention_str)

        return ret

    @property
    def config_type(self) -> Type[ImmutableBaseModel]:
        return ImmutableBaseModel

    @property
    def schema(self) -> KBSchema:
        return self._kb_schema

    @classmethod
    def from_config(cls, config: dict) -> 'DMBCommonnessStub':
        """Config example:
        {
            "schema": {
                ...`KBSchema` config...
            }
        }
        """
        return cls(kb_schema=KBSchema.from_config(config['schema']))
