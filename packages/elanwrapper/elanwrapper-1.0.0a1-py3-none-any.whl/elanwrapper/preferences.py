import dataclasses
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import NamedTuple, Union, Tuple, List, Dict
from xml.etree.ElementTree import ElementTree

import pympi


class ElanPreferencesRGB(NamedTuple):
    red: int
    green: int
    blue: int

    def __str__(self):
        return f"{self.red},{self.green},{self.blue}"


class ElanPreferencesDimension(NamedTuple):
    width: int
    height: int

    def __str__(self):
        return f"{self.width},{self.height}"


class ElanPreferencesPoint(NamedTuple):
    x: int
    y: int

    def __str__(self):
        return f"{self.x},{self.y}"


@dataclass
class ElanPreferences:
    frame_size: Union[ElanPreferencesDimension, Tuple[int, int]] = field(default=None, metadata={"key": "FrameSize"})

    layout_manager__current_mode: "ElanMode" = field(default=None, metadata={"key": "LayoutManager.CurrentMode"})
    layout_manager__selected_tab_index: "ElanAnnotationModeSelectedTab" = field(default=None, metadata={"key": "LayoutManager.SelectedTabIndex"})

    frame_location: Union[ElanPreferencesPoint, Tuple[int, int]] = field(default=None, metadata={"key": "FrameLocation"})

    transcription_table__column_types: List[str] = field(default=None, metadata={"key": "TranscriptionTable.ColumnTypes"})
    transcription_table__tier_map: Dict[str, List[str]] = field(default=None, metadata={"key": "TranscriptionTable.TierMap"})
    transcription_table__column_width: Dict[int, int] = field(default=None, metadata={"key": "TranscriptionTable.ColumnWidth"})
    transcription_table__hidden_tiers: List[str] = field(default=None, metadata={"key": "TranscriptionTable.HiddenTiers"})

    time_scale__begin_time: int = field(default=None, metadata={"key": "TimeScaleBeginTime"})
    media_time: int = field(default=None, metadata={"key": "MediaTime"})

    time_line_viewer__zoom_level: float = field(default=None, metadata={"key": "TimeLineViewer.ZoomLevel"})
    signal_viewer__zoom_level: float = field(default=None, metadata={"key": "SignalViewer.ZoomLevel"})

    tier_colors: Dict[str, ElanPreferencesRGB] = field(default=None, metadata={"key": "TierColors"})

    multi_tier_viewer__tier_order: List[str] = field(default=None, metadata={"key": "MultiTierViewer.TierOrder"})
    multi_tier_viewer__hidden_tiers: List[str] = field(default=None, metadata={"key": "MultiTierViewer.HiddenTiers"})
    multi_tier_viewer__active_tier_name: str = field(default=None, metadata={"key": "MultiTierViewer.ActiveTierName"})
    multi_tier_viewer__tier_sorting_mode: "ElanTierSortingMode" = field(default=None, metadata={"key": "MultiTierViewer.TierSortingMode"})
    multi_tier_viewer__sort_alphabetically: bool = field(default=None, metadata={"key": "MultiTierViewer.SortAlphabetically"})

    grid_viewer__tier_name: str = field(default=None, metadata={"key": "GridViewer.TierName"})
    grid_viewer__multi_tier_mode: bool = field(default=None, metadata={"key": "GridViewer.MultiTierMode"})
    text_viewer__tier_name: str = field(default=None, metadata={"key": "TextViewer.TierName"})

    def __post_init__(self):
        self.frame_size = ElanPreferencesDimension(*self.frame_size) if self.frame_size is not None else None
        self.frame_location = ElanPreferencesPoint(*self.frame_location) if self.frame_location is not None else None

    def get_pref_dict(self, *args, **kwargs):
        return {
            field.metadata["key"]: getattr(self, field.name)
            for field in dataclasses.fields(self)
            if "key" in field.metadata
        }

    def to_file(self, filename):
        pref_dict = dataclasses.asdict(self, dict_factory=self.get_pref_dict)

        from xml.etree.ElementTree import Element

        p = Element('preferences', {
            'version': '1.1',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
            'xsi:noNamespaceSchemaLocation': 'http://www.mpi.nl/tools/elan/Prefs_v1.1.xsd'
        })
        pref_elements = [
            self.get_pref(key, value)
            for key, value in pref_dict.items()
            if value is not None
        ]
        p.extend(pref_elements)
        pympi.Elan.indent(p)
        t = ElementTree(p)
        t.write(filename)

    @classmethod
    def get_pref(cls, key: str, value: any, parent_key: str = None):
        from xml.etree.ElementTree import Element
        if isinstance(value, dict):
            e = Element("prefGroup", {"key": str(key)})
            e.extend(cls.get_pref(k, v, parent_key=key) for k, v in value.items())
        elif isinstance(value, list):
            e = Element("prefList", {"key": str(key)})
            e.extend(cls.get_pref_value((parent_key or key), v) for v in value)
        else:
            e = Element("pref", {"key": str(key)})
            e.append(cls.get_pref_value((parent_key or key), value))
        return e

    @classmethod
    def get_pref_value(cls, key, value):
        from xml.etree.ElementTree import Element
        t = cls.get_pref_value_type(key, value)
        a = cls.get_pref_value_attributes(key, value)
        e = Element(t, a)
        if isinstance(value, bool):
            e.text = str(value).lower()
        else:
            e.text = str(value)
        return e

    @staticmethod
    def get_pref_value_type(key, value):
        mapping = {
            int: "Long",
            str: "String",
            float: "Float",
            Decimal: "Float",
            bool: "Boolean",
            "LayoutManager.CurrentMode": "Int",
            "LayoutManager.SelectedTabIndex": "Int",
            "TranscriptionTable.ColumnWidth": "Int",
            "MultiTierViewer.TierSortingMode": "Int",
            ElanPreferencesRGB: "Object",
            ElanPreferencesDimension: "Object",
            ElanPreferencesPoint: "Object",
        }
        if key in mapping:
            return mapping[key]
        if type(value) in mapping:
            return mapping[type(value)]
        raise KeyError(key)

    @staticmethod
    def get_pref_value_attributes(key, value):
        mapping = {
            ElanPreferencesRGB: {"class": "java.awt.Color"},
            ElanPreferencesDimension: {"class": "java.awt.Dimension"},
            ElanPreferencesPoint: {"class": "java.awt.Point"},
        }
        if key not in mapping:
            key = type(value)
        return mapping.get(key, {})


class ElanMode(Enum):
    MEDIA_SYNCHRONIZATION = 0
    ANNOTATION = 1
    TRANSCRIPTION = 2
    SEGMENTATION = 3
    INTERLINEARIZATION = 4

    def __str__(self):
        return str(self.value)


class ElanAnnotationModeSelectedTab(Enum):
    GRID = 0
    TEXT = 1
    SUBTITLES = 2
    LEXICON = 3
    COMMENTS = 4
    RECOGNIZERS = 5
    METADATA = 6
    CONTROLS = 7

    def __str__(self):
        return str(self.value)


class ElanTierSortingMode(Enum):
    UNSORTED = 0
    HIERARCHY = 1
    NAME = 2
    TIER_TYPE = 3
    PARTICIPANT = 3
    ANNOTATOR = 4
    CONTENT_LANGUAGE = 5

    def __str__(self):
        return str(self.value)
