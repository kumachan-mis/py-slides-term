import re

from .base import BaseCandidateTermFilter
from pdf_slides_term.mecab import BaseMeCabMorpheme
from pdf_slides_term.share.data import Term
from pdf_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


class ProperNounFilter(BaseCandidateTermFilter):
    def __init__(self):
        pass

    def inscope(self, term: Term) -> bool:
        regex = re.compile(rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})+")
        return regex.fullmatch(str(term)) is not None

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_region_or_person(scoped_term)

    def _is_region_or_person(self, scoped_term: Term) -> bool:
        def is_region_or_person_morpheme(morpheme: BaseMeCabMorpheme) -> bool:
            return (
                morpheme.pos == "名詞"
                and morpheme.category == "固有名詞"
                and morpheme.subcategory in {"人名", "地域"}
            ) or (morpheme.pos == "助詞" and morpheme.category == "名詞接続")

        return all(map(is_region_or_person_morpheme, scoped_term.morphemes))
