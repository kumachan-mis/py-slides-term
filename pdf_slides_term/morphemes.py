from abc import ABCMeta
from dataclasses import dataclass, asdict
from typing import Dict, ClassVar


@dataclass
class BaseMorpheme(metaclass=ABCMeta):
    NUM_ATTR: ClassVar[int] = 1

    surface_form: str

    def to_json(self) -> Dict:
        return asdict(self)


@dataclass
class MorphemeIPADic(BaseMorpheme):
    NUM_ATTR: ClassVar[int] = 10

    surface_form: str
    pos: str
    category: str
    subcategory: str
    subsubcategory: str
    conjugation_type: str
    conjugation_form: str
    original_form: str
    reading: str
    pronunciation: str

    def to_json(self) -> Dict:
        return asdict(self)
