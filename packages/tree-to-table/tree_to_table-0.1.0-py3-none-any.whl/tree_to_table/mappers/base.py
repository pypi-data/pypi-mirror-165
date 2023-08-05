from __future__ import annotations
from typing import TypeVar, Protocol, Union, Type, Callable, Optional

T = TypeVar("T")
ProtoSource = TypeVar("ProtoSource", contravariant=True)
ProtoResult = TypeVar("ProtoResult", covariant=True)
ProtoFinalResult = TypeVar("ProtoFinalResult", covariant=True)


class MapperProtocol(Protocol[ProtoSource, ProtoResult, ProtoFinalResult]):
    """
    The MapperProtocol defines the class structure required for a Mapper

    This protocol is generic over its input and output, in the sense that
    Mappers transform one instance of a defined schema to another
    """

    def apply(self, obj: ProtoSource) -> Optional[ProtoResult]:
        ...

    def __call__(self, obj: ProtoSource) -> Optional[ProtoFinalResult]:
        ...


def identity(obj: T) -> T:
    return obj


Source = TypeVar("Source")
Result = TypeVar("Result")
FinalResult = TypeVar("FinalResult")


class Mapper(MapperProtocol[Source, Result, FinalResult]):
    def __init__(self, next: "Callable[[Result], FinalResult]"):
        self.next = next

    def apply(self, obj: Source) -> Optional[Result]:
        ...

    def __call__(self, obj: Source) -> Optional[FinalResult]:
        value = self.apply(obj)
        if value is None:
            return None
        return self.next(value)
