import bisect
from dataclasses import dataclass
from numbers import Number
from typing import TypeVar, Generic, Iterable, Iterator, List, Union, Tuple, Mapping

T = TypeVar('T', bound=Number)
V = TypeVar('V')


@dataclass(frozen=True)
class Segment(Generic[T], Tuple[T, T]):
    begin: T
    end: T

    def __new__(cls, begin: T, end: T):
        return  super().__new__(cls, (begin, end))

    def __post_init__(self):
        if not isinstance(self.begin, Number):
            raise TypeError(self.begin)

    def intersect(self, other: "Segment"):
        """Intersection of two segments. Inclusive of begin points, exclusive of end points."""
        if not isinstance(other, Segment):
            raise TypeError(other)
        return self.end > other.begin and other.end > self.begin or self.begin == other.begin


class Timeline(Generic[T], Iterable[Segment[T]]):
    def __init__(self, initial_values: Iterable[Segment[T]] = None):
        self._segments: List[Segment[T]] = []
        if isinstance(initial_values, Iterable):
            for segment in initial_values:
                self.insert(segment)

    def __iter__(self):
        return iter(self._segments)

    def __len__(self):
        return len(self._segments)

    def get(self, at_time: T, default=None):
        entries = self.get_all(at_time)[0]
        if not len(entries):
            return default
        return entries[0]

    def index(self, at_time: T, none_for_not_found=False):
        insert_index, intersect_index = self._insert_and_intersection(at_time)
        if len(intersect_index) == 1:
            return intersect_index[0]
        elif len(intersect_index) > 1:
            raise KeyError(f"Spans multiple segments: {at_time}")
        elif none_for_not_found:
            return None
        else:
            raise ValueError(f"{at_time} not in timeline")

    def get_all(self, at_time: Union[Segment, T]) -> Tuple[Segment, ...]:
        insert_index, intersect_index = self._insert_and_intersection(at_time)
        return tuple((self._segments[i] for i in intersect_index))

    def _insert_and_intersection(self, at_time: Union[Segment, T]) -> Tuple[int, Tuple[int, ...]]:
        if not isinstance(at_time, Segment) and isinstance(at_time, Iterable) and len(list(at_time)) == 2:
            at_time = Segment(*at_time)
        if isinstance(at_time, Number):
            at_time = Segment(at_time, at_time)
        if not isinstance(at_time, Segment):
            raise KeyError(at_time)
        insert_idx = bisect.bisect_right(self._segments, at_time)

        intersection = tuple()
        if insert_idx < len(self._segments) and self._segments[insert_idx].intersect(at_time):
            intersection = (insert_idx, )

        cursor = insert_idx - 1
        while cursor >= 0 and self._segments[cursor].intersect(at_time):
            intersection = (cursor, *intersection)
            cursor -= 1
        return insert_idx, intersection

    def insert(self, element: Segment[T]) -> int:
        element = Segment(*element)
        insert_index, intersect_index = self._insert_and_intersection(element)
        if len(intersect_index):
            overlapping = [self._segments[i] for i in intersect_index]
            raise TimelineOverlapError(element, overlapping_index=intersect_index, overlapping=overlapping)
        self._segments.insert(insert_index, element)
        return insert_index

    def pop(self, idx):
        return self._segments.pop(idx)

    # def remove(self, at: Union[Segment, T]):
    #     idx = self.index(at)
    #     self._segments.pop(idx)

    # def clear(self):
    #     self._segments.clear()


class TimelineDict(Mapping[T, V], Generic[T, V]):
    def __init__(self, init_values=None, *, conflict_resolver=None):
        self._timeline = Timeline[T]()
        self._values = []
        self._conflict_resolver = conflict_resolver
        for key, value in dict(init_values or []).items():
            self.insert(key, value)

    def __getitem__(self, k: T) -> V:
        idx = self._timeline.index(k)
        return self._values[idx]

    def get(self, k: T, default=None) -> V:
        idx = self._timeline.index(k, none_for_not_found=True)
        if idx is None:
            return default
        return self._values[idx]

    def insert(self, k: T, v: V):
        try:
            insert_index = self._timeline.insert(k)
            self._values.insert(insert_index, v)
            assert len(self._timeline) == len(self._values)
        except TimelineOverlapError as e:
            reraise_error = TimelineOverlapError(
                v,
                overlapping_index=list(e.overlapping_index),
                overlapping=[self[o] for o in e.overlapping],
            )
            if self._conflict_resolver is None:
                raise reraise_error from e
            conflicts = [
                (key, self._values[idx])
                for key, idx in zip(e.overlapping, e.overlapping_index)
            ]
            resolved = self._conflict_resolver.resolve((k, v), conflicts)

            for idx in reversed(sorted(e.overlapping_index)):
                self.pop(idx)

            try:
                for resolved_key, resolved_value in resolved:
                    insert_index = self._timeline.insert(resolved_key)
                    self._values.insert(insert_index, resolved_value)
                    assert len(self._timeline) == len(self._values)
            except TimelineOverlapError:
                raise reraise_error from e

    def update(self, other):
        for key, value in other.items():
            self.insert(key, value)

    def pop(self, idx):
        self._timeline.pop(idx)
        value = self._values.pop(idx)
        return value

    # def remove(self, k: T):
    #     idx = self._timeline.index(k)
    #     self._timeline.pop(idx)
    #     self._values.pop(idx)

    # def clear(self, k: T):
    #     self._timeline.clear()
    #     self._values.clear()

    def __len__(self) -> int:
        return len(self._timeline)

    def __iter__(self) -> Iterator[T]:
        return iter(self._timeline)

    def __repr__(self) -> str:
        as_dict = {segment: value for segment, value in zip(self._timeline, self._values)}
        return f"{self.__class__.__name__}({as_dict})"

    __str__ = __repr__


class TimelineOverlapError(ValueError):
    def __init__(self, element, *, overlapping_index: Iterable[int], overlapping: Iterable[Segment], **kwargs):
        super().__init__(f"{element} overlaps with {overlapping}")
        self.element = element
        self.overlapping_index = overlapping_index
        self.overlapping = overlapping
