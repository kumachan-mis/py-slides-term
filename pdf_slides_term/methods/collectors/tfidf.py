from .base import BaseRankingDataCollector
from ..rankingdata import TFIDFRankingData
from pdf_slides_term.candidates import DomainCandidateTermList
from pdf_slides_term.analysis import TermOccurrenceAnalyzer, TermCharFontAnalyzer


class TFIDFRankingDataCollector(BaseRankingDataCollector[TFIDFRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> TFIDFRankingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        doc_freq = self._occurrence_analyzer.analyze_doc_term_freq(domain_candidates)
        num_docs = len(domain_candidates.xmls)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return TFIDFRankingData(
            domain_candidates.domain, term_freq, doc_freq, num_docs, term_maxsize
        )
