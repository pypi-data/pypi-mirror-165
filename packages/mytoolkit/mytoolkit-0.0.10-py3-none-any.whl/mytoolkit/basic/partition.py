from typing import Generator, Iterable, List, TypeVar

T = TypeVar("T")


def partition(iterable: Iterable[T], chunk_size: int) -> Generator[List[T], None, None]:
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk
