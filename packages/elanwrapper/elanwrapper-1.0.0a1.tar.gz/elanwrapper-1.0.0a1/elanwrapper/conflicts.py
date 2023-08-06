import abc
import dataclasses
import itertools
import logging
from typing import Tuple, Iterable


class ConflictResolver(metaclass=abc.ABCMeta):
    """
    In the event of overlapping segments, sometimes we can reconcile the conflicting items. This gives us an opportunity
    for just that.
    """
    @abc.abstractmethod
    def resolve(
            self,
            inserting: Iterable[Tuple["Segment", any]],
            conflicting: Iterable[Tuple["Segment", any]]
    ) -> Iterable[Tuple["Segment", any]]:
        pass


class ElanConflictResolver(ConflictResolver):
    """
    A conflict resolver for two situations:

    - For adjacent segments `a` and `b`, trim `a.end` to `b.beginning - 1` if `a.beginning - a.end is below a threshold
        (default threshold is 0, which helps with segments bumping right up against each other)
    - When segments occur with exactly the same boundaries, try removing segments with labels matching

    (base class description:) In the event of overlapping segments, sometimes we can reconcile the conflicting items.
    This gives us an opportunity for just that.

    """

    def __init__(self, trim_end_threshold_ms=0, duplicate_removal_rules=None):
        self.trim_end_threshold_ms = trim_end_threshold_ms
        self.duplicate_removal_rules = duplicate_removal_rules or [lambda label: label.strip() == ""]

    def resolve(
            self,
            inserting: Tuple["Segment", "ElanSegment"],
            conflicting: Iterable[Tuple["Segment", "ElanSegment"]]
    ) -> Iterable[Tuple["Segment", "ElanSegment"]]:
        s = sorted((inserting, *conflicting), key=lambda x: x[0])
        steps = [self._resolve_duplicates, self._trim_end]
        for step in steps:
            s, still_problems = step(s)
            if not still_problems:
                return s
        raise

    def _resolve_duplicates(self, s):
        result = []
        for key, values in itertools.groupby(s, key=lambda x: x[0]):
            _, values = zip(*values)

            if len(values) > 1:
                symbols = set(v.symbol for v in values)
                for rule in self.duplicate_removal_rules:
                    for symbol in list(symbols):
                        if len(symbols) == 1:
                            break
                        if rule(symbol or ""):
                            symbols.remove(symbol)

                preferred = []
                for symbol in symbols:
                    preferred.append(next(v for v in values if v.symbol == symbol))

                if len(preferred):
                    values = preferred
                if len(values) > 1:
                    logging.warning(values)

            for value in values:
                result.append((key, value))
        problems = any(a.intersect(b) for (a, _), (b, _) in zip(result[:-1], result[1:]))
        return result, problems

    def _trim_end(self, s: Iterable[Tuple["Segment", "ElanSegment"]]):
        result = []
        problems = False
        s = (*s, (None, None))
        for (a, a_value), (b, b_value) in zip(s[:-1], s[1:]):
            if b is None:
                result.append((a, a_value))
                return result, problems
            if a.begin < b.begin <= a.end and a.end - b.begin <= self.trim_end_threshold_ms:
                a = dataclasses.replace(a, end=b.begin)
                a_value = dataclasses.replace(a_value, end_ms=b.begin)
            result.append((a, a_value))
            if a.intersect(b):
                problems = True
        raise RuntimeError("huh?")
