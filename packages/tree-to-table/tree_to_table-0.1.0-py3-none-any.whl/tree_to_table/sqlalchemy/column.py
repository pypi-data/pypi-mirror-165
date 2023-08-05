from typing import Optional, Callable, Any

from sqlalchemy import Table, Column, MetaData, Integer


class MappedCol(Column):
    def __init__(self, *args, mapper=None, **kwargs):
        self._mapper = mapper
        super().__init__(*args, **kwargs)

    @property
    def mapper(self) -> Callable[[Any], Any]:
        from tree_to_table.mappers import Get

        if self._mapper is None:
            return Get(self.name)
        return self._mapper

    @mapper.setter
    def mapper(self, val: Optional[str]):
        self._mapper = val


from tree_to_table.mappers import Get

table = Table("students", MetaData(), MappedCol("id", Integer, mapper=Get("id")))
