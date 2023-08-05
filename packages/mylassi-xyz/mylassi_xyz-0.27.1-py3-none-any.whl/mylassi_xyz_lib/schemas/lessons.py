__all__ = [
    'LessonLessonPageData', 'LessonLessonPageSchema',
    'LessonInfoData', 'LessonInfoSchema',
    'LessonData', 'LessonSchema',
    'LessonListData', 'LessonListSchema',
    'CreateLessonOptionData', 'CreateLessonOptionSchema',
    'PatchLessonOptionData', 'PatchLessonOptionSchema',
]

from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow_dataclass

from .lesson_page_elements import LessonPageElementData

from .users import UserData


@dataclass
class LessonInfoData:
    id: int = field()
    public_id: str = field()
    name: str = field()

    owner: Optional[UserData] = field()
    tags: List[str] = field(default_factory=list)


@dataclass
class LessonLessonPageData:
    id: int = field()
    order: int = field()
    lesson_id: int = field()
    note: Optional[str] = field()
    elements: List[LessonPageElementData] = field(default_factory=list)


@dataclass
class LessonData(LessonInfoData):
    pages: List[LessonLessonPageData] = field(default_factory=list)


@dataclass
class LessonListData:
    length: int = field()
    page: int = field()
    pages: int = field()

    items: List[LessonInfoData] = field(default_factory=list)


@dataclass
class CreateLessonOptionData:
    name: str = field()
    tags: Optional[List[str]] = field(default_factory=list)


@dataclass
class PatchLessonOptionData:
    name: str = field()
    tags: Optional[List[str]] = field(default_factory=list)


LessonInfoSchema = marshmallow_dataclass.class_schema(LessonInfoData)()
LessonSchema = marshmallow_dataclass.class_schema(LessonData)()
LessonListSchema = marshmallow_dataclass.class_schema(LessonListData)()

CreateLessonOptionSchema = marshmallow_dataclass.class_schema(CreateLessonOptionData)()
PatchLessonOptionSchema = marshmallow_dataclass.class_schema(PatchLessonOptionData)()
LessonLessonPageSchema = marshmallow_dataclass.class_schema(LessonLessonPageData)()
