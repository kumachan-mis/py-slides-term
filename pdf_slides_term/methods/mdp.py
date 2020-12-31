from typing import Callable, Iterable

from pdf_slides_term.methods.base import BaseMultiDomainRankingMethod
from pdf_slides_term.methods.rankingdata.mdp import MDPRankingData
from pdf_slides_term.methods.collectors.mdp import MDPRankingDataCollector
from pdf_slides_term.methods.rankers.mdp import MDPRanker


class MDPMethod(BaseMultiDomainRankingMethod[MDPRankingData]):
    # public
    def __init__(
        self,
        compile_scores: Callable[[Iterable[float]], float] = min,
        consider_charfont: bool = True,
    ):
        collector = MDPRankingDataCollector(collect_charfont=consider_charfont)
        ranker = MDPRanker(compile_scores=compile_scores)
        super().__init__(collector, ranker)
