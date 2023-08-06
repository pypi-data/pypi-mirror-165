import contextlib
import dataclasses
import itertools
import json
import os
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from io import StringIO
from typing import Dict, Optional, Iterable, Union

import pympi

from elanwrapper import ElanConflictResolver
from elanwrapper.segments import TimelineDict, Segment, TimelineOverlapError


@dataclass
class ElanSegment:
    symbol: str
    begin_ms: int
    end_ms: int
    tier: str
    ref_tier: str = None
    linguistic_type: str = "default-lt"
    constraints: Optional[str] = None
    timealignable: bool = True

    def __post_init__(self):
        self.begin_ms = int(self.begin_ms)
        self.end_ms = int(self.end_ms)
        self.timealignable = _parse_bool(self.timealignable)
        if self.ref_tier is not None and self.constraints is None:
            self.constraints = "Symbolic_Association"
            self.timealignable = False

    @property
    def length_ms(self):
        return self.end_ms - self.begin_ms

    @property
    def length(self) -> Decimal:
        return Decimal(f"{self.length_ms / 1000}")

    @property
    def begin(self) -> Decimal:
        return Decimal(f"{self.begin_ms / 1000}")

    @property
    def end(self) -> Decimal:
        return Decimal(f"{self.end_ms / 1000}")


@dataclass
class Tier:
    tier_id: str
    linguistic_type_ref: str = 'default-lt'
    parent_ref: str = None
    default_locale: str = None
    participant: str = None
    annotator: str = None
    lang_ref: str = None

    def to_tier_dict(self):
        return {key.upper(): value for key, value in dataclasses.asdict(self).items()}

    @classmethod
    def from_tier_dict(cls, tier_dict):
        return cls(**{key.lower(): value for key, value in tier_dict.items()})

    @classmethod
    def from_elan_segment(cls, s: ElanSegment):
        return cls(tier_id=s.tier, linguistic_type_ref=s.linguistic_type, parent_ref=s.ref_tier)


@dataclass
class LinguisticType:
    linguistic_type_id: str = 'default-lt'
    constraints: Optional[str] = None
    time_alignable: bool = True
    graphic_references: bool = False
    ext_ref: Optional[str] = None

    def __post_init__(self):
        self.time_alignable = _parse_bool(self.time_alignable)
        self.graphic_references = _parse_bool(self.graphic_references)

    def to_param_dict(self):
        return {
            "LINGUISTIC_TYPE_ID": self.linguistic_type_id,
            "CONSTRAINTS": self.constraints,
            "TIME_ALIGNABLE": str(self.time_alignable).lower(),
            "GRAPHIC_REFERENCES": str(self.graphic_references).lower(),
            "EXT_REF": self.ext_ref,
        }

    @classmethod
    def from_param_dict(cls, param_dict):
        return cls(**{key.lower(): value for key, value in param_dict.items()})

    @classmethod
    def from_elan_segment(cls, s: ElanSegment):
        return cls(linguistic_type_id=s.linguistic_type, constraints=s.constraints, time_alignable=s.timealignable)


class ElanFile:
    def __init__(self, media_descriptors=None, conflict_resolver=None):
        conflict_resolver = conflict_resolver or ElanConflictResolver()
        self.media_descriptors = media_descriptors or []
        self._tier_timelines : defaultdict = defaultdict(lambda: TimelineDict(conflict_resolver=conflict_resolver))
        self._tier_meta : Dict[str, Tier] = {}
        self._linguistic_types : Dict[str, LinguisticType] = {}

    def segments(self, tier=None) -> Iterable[Segment]:
        if tier:
            return list(self._tier_timelines[tier].values())
        else:
            all = itertools.chain(*(timeline_dict.values() for timeline_dict in self._tier_timelines.values()))
            return sorted(all, key=lambda segment: (segment.begin, segment.end, segment.tier))

    def add(self, a: ElanSegment):
        key = Segment(a.begin_ms, a.end_ms)
        self._tier_timelines[a.tier].insert(key, a)
        self._handle_tier(a)

    def _handle_tier(self, a: ElanSegment):
        tm = Tier.from_elan_segment(a)
        lt = LinguisticType.from_elan_segment(a)
        for dictionary, item in ((self._tier_meta, tm), (self._linguistic_types, lt)):
            if a.tier in dictionary:
                if dictionary[a.tier] != item:
                    raise ValueError(f"Incosistent tier meta: {item} does not mesh with {dictionary[a.tier]}")
            else:
                dictionary[a.tier] = item

    def extend(self, alignments: Iterable[ElanSegment]):
        for a in alignments:
            self.add(a)

    def tier(self, tier_name):
        return self._tier_timelines.get(tier_name)

    def tier_names(self):
        return set(self._tier_meta)

    @classmethod
    def from_elan(cls, filename, conflict_resolver=None) -> "Session":
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):  # pympi gives warnings on any ELAN file not marked version 2.8/2.9.
            try:
                eaf = pympi.Elan.Eaf(filename)
                media_descriptors = [ElanMediaDescriptor.from_elan(**m) for m in eaf.media_descriptors]
                session = cls(media_descriptors=media_descriptors, conflict_resolver=conflict_resolver)
                linguistic_types = {
                    tier_name: LinguisticType.from_param_dict(lt)
                    for tier_name, lt in eaf.linguistic_types.items()
                }
                tiers = {
                    tier_name: Tier.from_tier_dict(tier)
                    for tier_name, (*_, tier, tier_len) in eaf.tiers.items()
                }
                for tier_id, (aligned_annotations, reference_annotations, attributes, ordinal) in eaf.tiers.items():
                    if tier_id == "default" and tier_id not in tiers:
                        continue
                    tier_meta = tiers[tier_id]
                    ling_type = linguistic_types[tier_meta.linguistic_type_ref]
                    try:
                        session.extend(
                            cls._to_alignment(eaf, tier_id, a, tier_meta, ling_type)
                            for a in aligned_annotations.values()
                        )
                        session.extend(
                            cls._ref_to_alignment(eaf, tier_id, a, tier_meta, ling_type)
                            for a in reference_annotations.values()
                        )
                    except TimelineOverlapError as e:
                        raise ElanFileLoadError(f"{filename}", f"tier {tier_id}", e) from e

                return session
            except:
                print(temp_stdout.getvalue())
                raise

    @classmethod
    def _to_alignment(cls, eaf, tier_id, aligned_annotation, tier: Tier, linguistic_type: LinguisticType):
        begin_ts, end_ts, value, svg_ref = aligned_annotation

        return ElanSegment(
            begin_ms=eaf.timeslots[begin_ts],
            end_ms=eaf.timeslots[end_ts],
            symbol=value,
            tier=tier_id,
            linguistic_type=linguistic_type.linguistic_type_id,
            ref_tier=tier.parent_ref,
            constraints=linguistic_type.constraints,
            timealignable=linguistic_type.time_alignable
        )

    @classmethod
    def _ref_to_alignment(cls, eaf, tier_id, reference_annotation, tier: Tier, linguistic_type: LinguisticType):
        ref_key, value, x, y = reference_annotation
        ref_tier = eaf.annotations[ref_key]
        alignment = cls._to_alignment(eaf, tier_id, eaf.tiers[ref_tier][0][ref_key], tier, linguistic_type)
        alignment = dataclasses.replace(alignment, symbol=value, tier=tier_id, ref_tier=ref_tier)
        return alignment

    def to_elan(self, filename):
        eaf = pympi.Elan.Eaf()
        # eaf.maxts = 0
        eaf.media_descriptors.extend(m.to_elan() for m in self.media_descriptors)

        for tier_name, linguistic_type in self._linguistic_types.items():
            eaf.add_linguistic_type(linguistic_type.linguistic_type_id, param_dict=linguistic_type.to_param_dict())

        for tier_name, tier_meta in self._tier_meta.items():
            if self._linguistic_types[tier_name].time_alignable:
                eaf.add_tier(tier_name, tier_dict=tier_meta.to_tier_dict())
                for a in self._tier_timelines[tier_name].values():
                    eaf.add_annotation(a.tier, a.begin_ms, a.end_ms, value=a.symbol)

        for tier_name, tier_meta in self._tier_meta.items():
            if not self._linguistic_types[tier_name].time_alignable:
                eaf.add_tier(tier_name, tier_dict=tier_meta.to_tier_dict())
                for a in self._tier_timelines[tier_name].values():
                    eaf.add_ref_annotation(a.tier, a.ref_tier, time=a.begin_ms, value=a.symbol)

        if os.path.exists(filename):
            os.unlink(filename)

        eaf.to_file(filename)

    def earliest(self):
        return min(
            (next(iter(timeline.values())) for tier, timeline in self._tier_timelines.items()),
            key=lambda t: t.begin_ms
        )


@dataclass
class ElanMediaDescriptor:
    file_path: str = None
    rel_path: str = None
    mimetype: str = None
    time_origin: int = None
    ex_from: str = None

    def __post_init__(self):
        self.file_path = self.file_path or self.rel_path
        assert self.file_path
        if self.mimetype is None:
            import pympi
            *_, file_extension = self.file_path.split('.')
            if not file_extension:
                raise ValueError("")
            self.mimetype = pympi.Eaf.MIMES[self.file_path.split('.')[-1]]

    @classmethod
    def from_elan(cls, MEDIA_URL, RELATIVE_MEDIA_URL=None, MIME_TYPE=None, TIME_ORIGIN=None, EXTRACTED_FROM=None):
        return cls(
            file_path=MEDIA_URL,
            rel_path=RELATIVE_MEDIA_URL,
            mimetype=MIME_TYPE,
            time_origin=TIME_ORIGIN,
            ex_from=EXTRACTED_FROM,
        )

    def to_elan(self):
        return {
            'MEDIA_URL': self.file_path,
            'RELATIVE_MEDIA_URL': self.rel_path,
            'MIME_TYPE': self.mimetype,
            'TIME_ORIGIN': self.time_origin,
            'EXTRACTED_FROM': self.ex_from
        }


class ElanFileLoadError(Exception):
    pass


def _parse_bool(b: Union[str, bool]) -> bool:
    if isinstance(b, str) and b.lower() in ("true", "false"):
        return json.loads(b)
    return b
