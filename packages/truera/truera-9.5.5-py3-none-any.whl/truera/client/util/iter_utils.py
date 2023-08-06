"""
Utilities for use with iterators or iteration. Batching-related iteration is
included.

TODO: similar utilities are likely found in other parts of the codebase. Please
move them here once found.
"""

from pathlib import Path
from typing import Iterable, Iterator, List, TypeVar

import pandas as pd

T = TypeVar("T")


def iter_csv(path: Path,
             chunksize: int = 1024,
             *args,
             **kwargs) -> Iterable[pd.DataFrame]:
    """
    Read a CSV in chunksize pieces, iterating over chunksized dataframes. Extra
    args passed to Pandas.read_csv .
    """

    assert chunksize > 0, f"chunksize:int={chunksize} must be greater than 0"

    df: Iterable[pd.DataFrame
                ] = pd.read_csv(path, chunksize=chunksize, *args, **kwargs)

    return df


def it_take(it: Iterator[T], n: int) -> List[T]:
    """
    EFFECT: take and return the first n items in the iteration. May return fewer
    at end of iterator.
    """

    ret = []

    try:
        for _ in range(n):
            ret.append(next(it))
    except StopIteration:
        pass

    return ret


def batch(items: Iterable[T], batch_size: int) -> Iterable[List[T]]:
    """
    Batch the given iterable items into batches of `batch_size` (except the last
    batch potentially).
    """

    it: Iterator[T] = iter(items)

    while True:
        batch = it_take(it, n=batch_size)
        if len(batch) == 0:
            return
        else:
            yield batch


def flatten(batches: Iterable[Iterable[T]]) -> Iterable[T]:
    """
    Flatten iterables of iterables into an interable.
    """

    for batch in batches:
        for item in batch:
            yield item


def rebatch(batches: Iterable[Iterable[T]],
            batch_size: int) -> Iterable[List[T]]:
    """
    Takes batches from the given iterable and rebatches it into the given
    batch_size.
    """

    assert batch_size > 0, f"batch_size:int={batch_size} must be greater than 0"

    flat: Iterable[T] = flatten(batches)

    return batch(flat, batch_size=batch_size)
