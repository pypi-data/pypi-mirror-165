__all__ = [
    'LessonPageData', 'LessonPageSchema',
    'CreateLessonPageOptionData', 'CreateLessonPageOptionSchema',
    'PatchLessonPageOptionSchema', 'PatchLessonPageOptionData',
]

from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow_dataclass

from .lesson_page_elements import LessonPageElementData, CreateLessonPageElementOptionData


@dataclass
class LessonPageData:
    id: int = field()
    order: int = field()
    note: str = field()
    elements: List[LessonPageElementData] = field(default_factory=list)


@dataclass
class CreateLessonPageOptionData:
    note: Optional[str] = field()
    previous_page: Optional[int] = field()
    elements: List[CreateLessonPageElementOptionData] = field(default_factory=list)


@dataclass
class PatchLessonPageOptionData:
    note: Optional[str] = field()


LessonPageSchema = marshmallow_dataclass.class_schema(LessonPageData)()
CreateLessonPageOptionSchema = marshmallow_dataclass.class_schema(CreateLessonPageOptionData)()
PatchLessonPageOptionSchema = marshmallow_dataclass.class_schema(PatchLessonPageOptionData)()
