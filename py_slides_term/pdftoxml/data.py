from dataclasses import dataclass, asdict
from xml.etree.ElementTree import tostring, fromstring, Element
from typing import Dict, Any


@dataclass(frozen=True)
class PDFnXMLPath:
    pdf_path: str
    xml_path: str

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)


@dataclass(frozen=True)
class PDFnXMLElement:
    pdf_path: str
    xml_root: Element

    def to_json(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "xml_root": tostring(self.xml_root, encoding="utf-8").decode("utf-8"),
        }

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(obj["pdf_path"], fromstring(obj["xml_root"]))
