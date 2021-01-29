from dataclasses import dataclass, field
from typing import List

from .base import BaseLayerConfig


@dataclass(frozen=True)
class CandidateLayerConfig(BaseLayerConfig):
    morpheme_filters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.filters.JapaneseMorphemeFilter",
            "py_slides_term.filters.EnglishMorphemeFilter",
        ]
    )
    term_filters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.filters.JapaneseConcatenationFilter",
            "py_slides_term.filters.EnglishConcatenationFilter",
            "py_slides_term.filters.JapaneseSymbolLikeFilter",
            "py_slides_term.filters.EnglishSymbolLikeFilter",
            "py_slides_term.filters.JapaneseProperNounFilter",
            "py_slides_term.filters.EnglishProperNounFilter",
        ]
    )
    splitters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.splitters.RepeatSplitter",
        ]
    )
    augmenters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.augmenters.ModifyingParticleAugmenter",
        ]
    )
    use_cache: bool = True
    remove_lower_layer_cache: bool = True
