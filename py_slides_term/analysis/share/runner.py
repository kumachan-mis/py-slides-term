from typing import Callable, TypeVar

from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term

AnalysisResult = TypeVar("AnalysisResult")


class AnalysisRunner:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._ignore_augmented = ignore_augmented

    def run_through_candidates(
        self,
        domain_candidates: DomainCandidateTermList,
        initial_result: AnalysisResult,
        update_result: Callable[[AnalysisResult, int, int, Term], None],
    ) -> AnalysisResult:
        result = initial_result

        for pdf_id, pdf_candidates in enumerate(domain_candidates.pdfs):
            for page_candidates in pdf_candidates.pages:
                page_num = page_candidates.page_num
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue
                    update_result(result, pdf_id, page_num, candidate)

        return result

    def run_through_subcandidates(
        self,
        domain_candidates: DomainCandidateTermList,
        initial_result: AnalysisResult,
        update_result: Callable[[AnalysisResult, int, int, Term], None],
    ) -> AnalysisResult:
        result = initial_result

        for pdf_id, pdf_candidates in enumerate(domain_candidates.pdfs):
            for page_candidates in pdf_candidates.pages:
                page_num = page_candidates.page_num
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue

                    num_morphemes = len(candidate.morphemes)
                    for i in range(num_morphemes):
                        for j in range(i + 1, num_morphemes + 1):
                            subcandidate = Term(
                                candidate.morphemes[i:j],
                                candidate.fontsize,
                                candidate.augmented,
                            )
                            update_result(result, pdf_id, page_num, subcandidate)

        return result
