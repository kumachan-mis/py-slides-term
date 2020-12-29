from dataclasses import dataclass, field
from typing import Dict, List, Callable, Iterable, Optional

from pdf_slides_term.methods.data import DomainTermRanking, ScoredTerm
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm
from pdf_slides_term.share.utils import extended_log10


@dataclass(frozen=True)
class MDPDomainRankingData:
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences
    # count even if the term occurs as a part of a phrase
    num_terms: int = field(init=False)
    # brute force counting of all terms occurrences
    # count even if the term occurs as a part of a phrase
    term_maxsize: Optional[Dict[str, float]] = None
    # max fontsize of the term
    # default of this is zero

    def __post_init__(self):
        object.__setattr__(self, "num_terms", sum(self.term_freq.values()))


class MDPRanker:
    # public
    def __init__(self, compile_scores: Callable[[Iterable[float]], float] = min):
        self._compile_scores = compile_scores

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: MDPDomainRankingData,
        other_ranking_data_list: List[MDPDomainRankingData],
    ) -> DomainTermRanking:
        scored_term_dict: Dict[str, ScoredTerm] = dict()

        for xml_candidates in domain_candidates.xmls:
            for page_candidates in xml_candidates.pages:
                for candidate in page_candidates.candidates:
                    if str(candidate) in scored_term_dict:
                        continue
                    scored_candidate = self._calculate_score(
                        candidate, ranking_data, other_ranking_data_list
                    )
                    scored_term_dict[scored_candidate.term] = scored_candidate

        ranking = sorted(list(scored_term_dict.values()), key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    # private
    def _calculate_score(
        self,
        candidate: TechnicalTerm,
        ranking_data: MDPDomainRankingData,
        other_ranking_data_list: List[MDPDomainRankingData],
    ) -> ScoredTerm:
        score = self._compile_scores(
            map(
                lambda other_ranking_data: self._calculate_zvalue(
                    candidate, ranking_data, other_ranking_data
                ),
                other_ranking_data_list,
            )
        )

        return ScoredTerm(str(candidate), score)

    def _calculate_zvalue(
        self,
        candidate: TechnicalTerm,
        our_ranking_data: MDPDomainRankingData,
        their_ranking_data: MDPDomainRankingData,
    ) -> float:
        candidate_str = str(candidate)

        our_term_maxsize = (
            our_ranking_data.term_maxsize[candidate_str]
            if our_ranking_data.term_maxsize is not None
            else 1.0
        )
        their_term_maxsize = (
            their_ranking_data.term_maxsize.get(candidate_str, 0.0)
            if their_ranking_data.term_maxsize is not None
            else 1.0
        )

        our_term_freq = our_ranking_data.term_freq[candidate_str]
        their_term_freq = their_ranking_data.term_freq.get(candidate_str, 0)

        our_inum_terms = 1 / our_ranking_data.num_terms
        their_inum_terms = 1 / their_ranking_data.num_terms

        our_term_prob = our_term_freq / our_ranking_data.num_terms
        their_term_prob = their_term_freq / their_ranking_data.num_terms
        term_prob = (our_term_freq + their_term_freq) / (
            our_ranking_data.num_terms + their_ranking_data.num_terms
        )

        return extended_log10(
            (our_term_maxsize * our_term_prob - their_term_maxsize * their_term_prob)
            / (term_prob * (1.0 - term_prob) * (our_inum_terms + their_inum_terms))
        )
