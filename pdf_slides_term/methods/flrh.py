from pdf_slides_term.methods.base import BaseSingleDomainRankingMethod
from pdf_slides_term.methods.rankingdata.flrh import FLRHRakingData
from pdf_slides_term.methods.collectors.flrh import FLRHRankingDataCollector
from pdf_slides_term.methods.rankers.flrh import FLRHRanker


class FLRHMethod(BaseSingleDomainRankingMethod[FLRHRakingData]):
    # public
    def __init__(self, consider_charfont: bool = True):
        collector = FLRHRankingDataCollector(collect_charfont=consider_charfont)
        ranker = FLRHRanker()
        super().__init__(collector, ranker)
