from dataclasses import dataclass
from typing import List

@dataclass
class BenefitsNotes:
    benefitsStringIds: List[str]
    notesStringIds: List[str]
    helpLink: str


@dataclass
class ProgramInfo:
    name: str
    programStringIds: List[str]
    displayPriority: int
    benefitsNotes: BenefitsNotes


@dataclass
class ProgramListResponse:
    succeed: bool
    programInfoList: List[ProgramInfo]
