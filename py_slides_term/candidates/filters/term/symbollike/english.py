import re

from ..base import BaseEnglishCandidateTermFilter
from py_slides_term.share.data import Term


PHONETIC_REGEX = r"[A-Za-z]"


class EnglishSymbolLikeFilter(BaseEnglishCandidateTermFilter):
    # public
    def __init__(self):
        pass

    def is_candidate(self, scoped_term: Term) -> bool:
        return not self._has_phonetic_symbol(scoped_term)

    # private
    def _has_phonetic_symbol(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)
        phonetic_regex = re.compile(PHONETIC_REGEX)

        if num_morphemes == 1:
            morpheme_str = str(scoped_term.morphemes[0])
            return phonetic_regex.fullmatch(morpheme_str) is not None

        def phonetic_char_appears_continuously_at(i: int) -> bool:
            if i == num_morphemes - 1:
                return False

            morpheme_str = str(scoped_term.morphemes[i])
            next_morpheme_str = str(scoped_term.morphemes[i + 1])
            return (
                phonetic_regex.fullmatch(morpheme_str) is not None
                and phonetic_regex.fullmatch(next_morpheme_str) is not None
            )

        return any(map(phonetic_char_appears_continuously_at, range(num_morphemes)))
