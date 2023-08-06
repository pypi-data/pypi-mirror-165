from abc import abstractmethod
from typing import Tuple, TypeVar, Optional, List, Protocol, Iterator

T = TypeVar('T')
Path = Tuple[int, ...]
Tree = Tuple[T, Optional[List['Tree[T]']]]


class ParseTree(Protocol):
    @abstractmethod
    def __iter__(self) -> Iterator[str | List['ParseTree'] | None]:
        raise NotImplementedError()

    @abstractmethod
    def __getitem__(self, item: int) -> str | List['ParseTree'] | None:
        raise NotImplementedError()