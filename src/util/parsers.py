from typing import List, Optional
from itertools import chain

from fastapi import Query


def flat_map(f, x):
    lst = []
    for y in x:
        lst.extend(f(y))
    return lst


def parse_leis(leis: List[str] = Query(None)) -> Optional[List]:
    """
    Parses leis from list of one or multiple strings to a list of multiple distinct lei strings
    Returns empty list when nothing is passed in
    Ex1: ['lei1,lei2'] -> ['lei1', 'lei2']
    Ex2: ['lei1,lei2', 'lei3,lei4'] -> ['lei1','lei2','lei3','lei4']
    """

    if leis:
        return list(chain.from_iterable([x.split(',') for x in leis]))
    else:
        return None