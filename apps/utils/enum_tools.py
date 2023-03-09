from enum import Enum as _Enum
from typing import List


# 枚举工具
class Enum(_Enum):

    __enumtag__ = {}

    @classmethod
    def tag(cls, value) -> str:
        """根据值获取设置的tag"""
        for _, val in enumerate(cls):
            if value == val.value:
                return cls.__enumtag__.get(val.name, val.name)
        return None

    @classmethod
    def tags(cls) -> list:
        """获取所有标签数据"""
        return [
            cls.__enumtag__.get(val.name, val.name)
            for _, val in enumerate(cls)
        ]

    @classmethod
    def values(cls) -> list:
        """获取所有枚举数据"""
        return [val.value for _, val in enumerate(cls)]

    @classmethod
    def enums(cls) -> List[dict]:
        """ 获取所有枚举属性"""

        return [
            {
                "name": val.name,
                "value": val.value,
                "tag": cls.__enumtag__.get(val.name, val.name)
            }for _, val in enumerate(cls)
        ]
