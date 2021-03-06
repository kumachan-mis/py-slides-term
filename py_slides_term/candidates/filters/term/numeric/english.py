from ..base import BaseEnglishCandidateTermFilter
from py_slides_term.morphemes import BaseMorpheme, EnglishMorphemeClassifier
from py_slides_term.share.data import Term


class EnglishNumericFilter(BaseEnglishCandidateTermFilter):
    # public
    def __init__(self):
        self._classifier = EnglishMorphemeClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._is_numeric_phrase(scoped_term)

    def _is_numeric_phrase(self, scoped_term: Term) -> bool:
        def is_number_or_meaningless(morpheme: BaseMorpheme) -> bool:
            return morpheme.pos == "NUM" or self._classifier.is_meaningless(morpheme)

        return all(map(is_number_or_meaningless, scoped_term.morphemes))
