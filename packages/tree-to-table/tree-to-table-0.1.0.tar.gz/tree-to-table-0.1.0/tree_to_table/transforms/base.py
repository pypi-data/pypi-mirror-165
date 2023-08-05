from typing import Dict, Any, Iterable

from ..mappers import Mapper


class Transform:
    def __call__(
        self, mappers: Dict[str, Mapper], data: Iterable[Dict[Any, Any]]
    ) -> Iterable[Dict[Any, Any]]:
        raise NotImplementedError

    def transform(
        self, mappers: Dict[str, Mapper], data: Dict[Any, Any]
    ) -> Dict[str, Any]:
        return {name: mapper(data) for name, mapper in mappers.items()}
