__all__ = [
    'LessonPageElementTypeValues',
    'LessonPageElementStyleData', 'LessonPageElementStyleSchema',
    'LessonPageElementData', 'LessonPageElementSchema',
    'CreateLessonPageElementOptionData', 'CreateLessonPageElementOptionSchema',
    'UpdateLessonPageElementOptionData', 'UpdateLessonPageElementOptionSchema',
    'SocketLessonPageElementData', 'SocketLessonPageElementSchema',
]

import enum
from dataclasses import dataclass, field, MISSING
from typing import Optional

import marshmallow_dataclass


class LessonPageElementTypeValues(enum.Enum):
    TextElement = 'TextElement'
    MarkdownElement = 'MarkdownElement'
    ImageElement = 'ImageElement'
    YoutubeElement = 'YoutubeElement'


@dataclass
class LessonPageElementStyleData:
    width: Optional[float] = field(default=None)
    height: Optional[float] = field(default=None)
    top: Optional[float] = field(default=None)
    left: Optional[float] = field(default=None)

    font_size: Optional[str] = field(default=None)
    text_align: Optional[str] = field(default=None)


@dataclass
class LessonPageElementData:
    id: int = field()

    type: LessonPageElementTypeValues = field()
    content: str = field()
    style: LessonPageElementStyleData = field()


@dataclass
class CreateLessonPageElementOptionData:
    type: LessonPageElementTypeValues = field()
    content: Optional[str] = field()
    style: Optional[LessonPageElementStyleData] = field(default_factory=LessonPageElementStyleData)


@dataclass
class UpdateLessonPageElementOptionData:
    content: str = field()
    style: LessonPageElementStyleData = field()


@dataclass
class SocketLessonPageElementData:
    event: str = field()
    lesson_id: int = field()
    page_id: int = field()
    element_id: int = field()
    element: Optional[LessonPageElementData] = field(default=None)


LessonPageElementStyleSchema = marshmallow_dataclass.class_schema(LessonPageElementStyleData)()
LessonPageElementSchema = marshmallow_dataclass.class_schema(LessonPageElementData)()
CreateLessonPageElementOptionSchema = marshmallow_dataclass.class_schema(CreateLessonPageElementOptionData)()
UpdateLessonPageElementOptionSchema = marshmallow_dataclass.class_schema(UpdateLessonPageElementOptionData)()

SocketLessonPageElementSchema = marshmallow_dataclass.class_schema(SocketLessonPageElementData)()
