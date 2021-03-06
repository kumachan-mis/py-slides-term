import re
from typing import List

from .base import BaseSplitter
from ..filters import FilterCombiner
from py_slides_term.share.data import Term
from py_slides_term.share.consts import ALPHABET_REGEX


class SymbolNameSplitter(BaseSplitter):
    # public
    def __init__(self, candidate_filter: FilterCombiner):
        self._filter = candidate_filter

    def split(self, term: Term) -> List[Term]:
        num_morphemes = len(term.morphemes)
        if num_morphemes < 2:
            return [term]

        regex = re.compile(rf"{ALPHABET_REGEX}|\-")
        last_str = str(term.morphemes[len(term.morphemes) - 1])
        second_last_str = str(term.morphemes[len(term.morphemes) - 2])

        if not regex.fullmatch(last_str) or regex.fullmatch(second_last_str):
            return [term]

        non_symbol_morphemes = term.morphemes[: num_morphemes - 1]
        symbol_morphemes = [term.morphemes[num_morphemes - 1]]

        non_symbol_term = Term(non_symbol_morphemes, term.fontsize, term.augmented)
        symbol_term = Term(symbol_morphemes, term.fontsize, term.augmented)

        if not self._filter.is_candidate(non_symbol_term):
            return [term]

        splitted_terms = [non_symbol_term]
        if self._filter.is_candidate(symbol_term):
            splitted_terms.append(symbol_term)

        return splitted_terms
