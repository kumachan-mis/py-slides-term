import os
import json
from argparse import ArgumentParser
from glob import iglob
from typing import Iterator

from pdf_slides_term.methods.tfidf import TFIDFMethod
from pdf_slides_term.methods.lfidf import LFIDFMethod
from pdf_slides_term.methods.flr import FLRMethod
from pdf_slides_term.methods.hits import HITSMethod
from pdf_slides_term.methods.flrh import FLRHMethod
from pdf_slides_term.methods.mdp import MDPMethod
from pdf_slides_term.methods.base import (
    BaseSingleDomainRankingMethod,
    BaseMultiDomainRankingMethod,
)
from pdf_slides_term.candidates.data import (
    DomainCandidateTermList,
    XMLCandidateTermList,
)
from scripts.settings import DATASET_DIR


CANDIDATE_DIR = os.path.join(DATASET_DIR, "candidate")
METHODS_DIR = os.path.join(DATASET_DIR, "methods")


def generate_domain_candidates_list() -> Iterator[DomainCandidateTermList]:
    domains = list(
        filter(
            lambda dir_name: not dir_name.startswith(".")
            and os.path.isdir(os.path.join(CANDIDATE_DIR, dir_name)),
            os.listdir(CANDIDATE_DIR),
        )
    )

    for domain in domains:
        xmls = []
        json_path_pattern = os.path.join(CANDIDATE_DIR, domain, "**", "*.json")
        for json_path in iglob(json_path_pattern, recursive=True):
            with open(json_path, "r") as f:
                obj = json.load(f)
            xmls.append(XMLCandidateTermList.from_json(obj))

        yield DomainCandidateTermList(domain, xmls)


if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tfidf", help="use TF-IDF method", action="store_true")
    group.add_argument("--lfidf", help="use LF-IDF method", action="store_true")
    group.add_argument("--flr", help="use FLR method", action="store_true")
    group.add_argument("--hits", help="use HITS method", action="store_true")
    group.add_argument("--flrh", help="use FLRH method", action="store_true")
    group.add_argument("--mdp", help="use MDP method", action="store_true")
    args = parser.parse_args()

    if args.tfidf:
        method_name = "tfidf"
        method = TFIDFMethod()
    elif args.lfidf:
        method_name = "lfidf"
        method = LFIDFMethod()
    elif args.flr:
        method_name = "flr"
        method = FLRMethod()
    elif args.hits:
        method_name = "hits"
        method = HITSMethod()
    elif args.flrh:
        method_name = "flrh"
        method = FLRHMethod()
    elif args.mdp:
        method_name = "mdp"
        method = MDPMethod(compile_scores=max)
    else:
        exit(1)
        # never reach

    file_name = f"{method_name}.json"
    domain_candidates_generator = generate_domain_candidates_list()

    # pyright:reportUnnecessaryIsInstance=false
    if isinstance(method, BaseSingleDomainRankingMethod):
        for candidates in domain_candidates_generator:
            ranking_path = os.path.join(METHODS_DIR, candidates.domain, file_name)
            ranking_dir_name = os.path.dirname(ranking_path)
            os.makedirs(ranking_dir_name, exist_ok=True)
            term_ranking = method.rank_terms(candidates)

            with open(ranking_path, "w") as ranking_file:
                json_obj = term_ranking.to_json()
                json.dump(json_obj, ranking_file, ensure_ascii=False, indent=2)
    elif isinstance(method, BaseMultiDomainRankingMethod):
        domain_candidates_list = list(domain_candidates_generator)
        term_ranking_generator = method.rank_terms(domain_candidates_list)
        for term_ranking in term_ranking_generator:
            ranking_path = os.path.join(METHODS_DIR, term_ranking.domain, file_name)
            ranking_dir_name = os.path.dirname(ranking_path)
            os.makedirs(ranking_dir_name, exist_ok=True)

            with open(ranking_path, "w") as ranking_file:
                json_obj = term_ranking.to_json()
                json.dump(json_obj, ranking_file, ensure_ascii=False, indent=2)
