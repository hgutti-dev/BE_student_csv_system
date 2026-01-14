# src/utils/iterables.py
from __future__ import annotations

from typing import  Iterator, List, Sequence, Tuple, TypeVar

T = TypeVar("T")


def chunked(seq: Sequence[T], size: int) -> Iterator[Tuple[int, List[T]]]:
    """
    Yields (start_index, chunk_list)
    start_index es 0-based.
    """
    if size <= 0:
        raise ValueError("size debe ser > 0")

    for i in range(0, len(seq), size):
        yield i, list(seq[i : i + size])
