from math import log10
from typing import List, Literal

from .base import BaseMultiDomainRanker
from ..rankingdata import TFIDFRankingData
from ..data import DomainTermRanking
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term, ScoredTerm
from py_slides_term.share.utils import extended_log10


class TFIDFRanker(BaseMultiDomainRanker[TFIDFRankingData]):
    # public
    def __init__(
        self,
        tfmode: Literal["natural", "log", "augmented", "logave", "binary"] = "log",
        idfmode: Literal["natural", "smooth", "prob", "unary"] = "natural",
    ):
        self._tfmode = tfmode
        self._idfmode = idfmode

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: List[TFIDFRankingData],
    ) -> DomainTermRanking:
        domain_candidates_dict = domain_candidates.to_domain_candidate_term_dict()
        ranking_data = next(
            filter(
                lambda item: item.domain == domain_candidates.domain,
                ranking_data_list,
            )
        )
        ranking = list(
            map(
                lambda candidate: self._calculate_score(
                    candidate, ranking_data, ranking_data_list
                ),
                domain_candidates_dict.candidates.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    # private
    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: TFIDFRankingData,
        ranking_data_list: List[TFIDFRankingData],
    ) -> ScoredTerm:
        candidate_str = str(candidate)

        tf = self._calculate_tf(candidate_str, ranking_data, ranking_data_list)
        idf = self._calculate_idf(candidate_str, ranking_data, ranking_data_list)
        term_maxsize = (
            ranking_data.term_maxsize[candidate_str]
            if ranking_data.term_maxsize is not None
            else 1.0
        )
        score = extended_log10(term_maxsize * tf * idf)
        return ScoredTerm(candidate_str, score)

    def _calculate_tf(
        self,
        candidate: str,
        ranking_data: TFIDFRankingData,
        ranking_data_list: List[TFIDFRankingData],
    ) -> float:
        tf = ranking_data.term_freq[candidate]
        max_tf = max(
            map(lambda data: data.term_freq.get(candidate, 0), ranking_data_list)
        )
        tf_sum = sum(
            map(lambda data: data.term_freq.get(candidate, 0), ranking_data_list)
        )
        ave_tf = tf_sum / len(ranking_data_list)

        if self._idfmode == "natural":
            return tf
        elif self._tfmode == "log":
            return 1.0 * log10(tf) if tf > 0.0 else 0.0
        elif self._tfmode == "augmented":
            return 0.5 + 0.5 * tf / max_tf
        elif self._tfmode == "logave":
            return (1.0 + log10(tf)) / (1.0 + log10(ave_tf)) if tf > 0.0 else 0.0
        else:
            return 1.0 if tf > 0.0 else 0.0

    def _calculate_idf(
        self,
        candidate: str,
        ranking_data: TFIDFRankingData,
        ranking_data_list: List[TFIDFRankingData],
    ) -> float:
        num_docs = sum(map(lambda data: data.num_docs, ranking_data_list))
        df = sum(map(lambda data: data.doc_freq.get(candidate, 0), ranking_data_list))

        if self._idfmode == "natural":
            return log10(num_docs / df)
        if self._idfmode == "smooth":
            return log10(num_docs / (df + 1)) + 1.0
        elif self._idfmode == "prob":
            return max(log10((num_docs - df) / df), 0.0)
        else:
            return 1.0
