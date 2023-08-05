from typing import Any, Dict

from ..mappers import Mapper
from ..transforms import Transform, OneToOneTransform


class Column:
    def __init__(self, mapper: Mapper):
        self.mapper = mapper


class Table:
    _transform: Transform = OneToOneTransform()

    @classmethod
    def mappers(cls) -> Dict[str, Mapper]:
        return {
            column_name: mapper
            for column_name, mapper in cls.__dict__.items()
            if issubclass(type(mapper), Mapper)
        }

    @classmethod
    def transform(cls, data: Any):
        return cls._transform(cls.mappers(), data)
