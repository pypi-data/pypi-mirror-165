from typing import Dict, Iterable, Any, Callable, Mapping

from .base import Transform
from ..mappers import Mapper


class OneToOneTransform(Transform):
    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        if not isinstance(data, Iterable):
            raise TypeError(
                "Cannot transform a non-iterable set of data. If only one row is required to transform, wrap it with a list"
            )

        for item_i, item in enumerate(data):
            if not isinstance(item, Mapping):
                raise TypeError(
                    f"Cannot transform row '{item}' at index {item_i} as it is not a Mapping"
                )

            yield self.transform(mappers, item)


class OneToManyTransform(Transform):
    def __init__(
        self,
        split_mappers: Dict[str, Mapper],
        default_val=None,
        keep_splits=True,
    ):
        self.split_mappers = split_mappers
        self.default_val = default_val
        self.keep_splits = keep_splits

    def __call__(
        self,
        mappers: Dict[str, Mapper],
        data: Iterable[Dict[Any, Any]],
    ) -> Iterable[Dict[Any, Any]]:
        splits = [self.transform(self.split_mappers, item) for item in data]

        if any(split is None for split in splits):
            # TODO: Lol
            raise ValueError("One split is None so didnt work lol")

        for split, row in zip(splits, data):
            # TODO: I dont think this preserves order here in some cases
            # We are assuming split === dict(zip(split.keys(), split.values())), which I dont think is correct
            for x in zip(*split.values()):
                transformed = self.transform(mappers, row)

                if self.keep_splits:
                    split_dict = dict(zip(split.keys(), x))
                    yield {**split_dict, **transformed}
                else:
                    yield transformed


class ManyToOneTransform(Transform):
    # Say we have some fields that we know are the SAME over multiple rows
    # Can we define a way to merge these rows into a single row in a nice way?
    # We could maybe do a recursive meta merge?
    pass


class FilterTransform(Transform):
    def __init__(self, filter_fn: Callable[[Any], bool]):
        self.filter_fn = filter_fn

    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        for item in data:
            if self.filter_fn(item):
                yield self.transform(mappers, item)


def one_to_many(split_mappers):
    def _one_to_many(cls):
        cls._transform = OneToManyTransform(split_mappers)
        return cls

    return _one_to_many
