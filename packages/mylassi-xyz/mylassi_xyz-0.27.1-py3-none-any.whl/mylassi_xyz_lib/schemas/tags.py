__all__ = [
    'TagListData', 'TagListSchema',
    'TagInfoData', 'TagInfoSchema',
    'TagInfoListData', 'TagInfoListSchema',
]

from dataclasses import dataclass, field
from typing import List

import marshmallow_dataclass


@dataclass
class TagListData:
    tags: List[str] = field(default_factory=list)


@dataclass
class TagInfoData:
    id: int = field()
    label: str = field()


@dataclass
class TagInfoListData:
    tags: List[TagInfoData] = field(default_factory=list)


TagListSchema = marshmallow_dataclass.class_schema(TagListData)()

TagInfoSchema = marshmallow_dataclass.class_schema(TagInfoData)()
TagInfoListSchema = marshmallow_dataclass.class_schema(TagInfoListData)()
