"""Utility functions for converting between SDK args and proto objects."""

from copy import deepcopy
from typing import Dict, List, Optional

from google.protobuf.json_format import ParseDict

from rime_sdk.protos.firewall.firewall_pb2 import (
    BinSize,
    DataLocation,
    DataLocationType,
)
from rime_sdk.protos.result_synthesizer.result_message_pb2 import (
    ThresholdDirection,
    ThresholdInfo,
)


def get_bin_size_proto(bin_size_str: str) -> BinSize:
    """Get bin size proto from string."""
    years = 0
    months = 0
    seconds = 0
    if bin_size_str == "year":
        years += 1
    elif bin_size_str == "month":
        months += 1
    elif bin_size_str == "week":
        seconds += 7 * 24 * 60 * 60
    elif bin_size_str == "day":
        seconds += 24 * 60 * 60
    elif bin_size_str == "hour":
        seconds += 60 * 60
    else:
        raise ValueError(
            f"Got unknown bin size ({bin_size_str}), "
            f"should be one of: `year`, `month`, `week`, `day`, `hour`"
        )
    return BinSize(years=years, months=months, seconds=seconds)


LOCATION_TYPE_TO_ENUM_MAP: Dict[str, "DataLocationType.V"] = {
    "data_collector": DataLocationType.LOCATION_TYPE_DATA_COLLECTOR
}


def location_args_to_data_location(location_type: str) -> DataLocation:
    """Create Data Location object for Firewall Requests."""
    location_keys = set(LOCATION_TYPE_TO_ENUM_MAP.keys())
    if location_type not in location_keys:
        raise ValueError(
            f"Location type {location_type} must be one of {location_keys}"
        )
    return DataLocation(location_type=LOCATION_TYPE_TO_ENUM_MAP[location_type])


THRESHOLD_INFO_TO_ENUM_MAP = {
    "above": ThresholdDirection.THRESHOLD_DIRECTION_ABOVE,
    "below": ThresholdDirection.THRESHOLD_DIRECTION_BELOW,
    None: ThresholdDirection.THRESHOLD_DIRECTION_UNSPECIFIED,
}


def get_threshold_direction_proto(direction: Optional[str]) -> "ThresholdDirection.V":
    """Get the threshold direction protobuf."""
    _direction = THRESHOLD_INFO_TO_ENUM_MAP.get(direction)
    if _direction is None:
        # TODO: Handle "both" cases
        raise ValueError(
            f"Invalid threshold direction {direction}. Expected 'above' or 'below'."
        )
    return _direction


def get_threshold_info_proto(metric_threshold_info: dict) -> ThresholdInfo:
    """Return the threshold info map."""
    info_copy = deepcopy(metric_threshold_info)
    info_copy["direction"] = get_threshold_direction_proto(
        metric_threshold_info.get("direction")
    )
    return ParseDict(info_copy, ThresholdInfo())


def threshold_infos_to_map(
    threshold_infos: List[ThresholdInfo],
) -> Dict[str, ThresholdInfo]:
    """Return map of metric name to ThresholdInfo."""
    threshold_info_map = {}
    for threshold_info in threshold_infos:
        info_without_metric = ThresholdInfo(
            direction=threshold_info.direction,
            low=threshold_info.low,
            medium=threshold_info.medium,
            high=threshold_info.high,
            disabled=threshold_info.disabled,
        )
        threshold_info_map[threshold_info.metric_name] = info_without_metric
    return threshold_info_map


DEFAULT_THRESHOLD_INFO_KEY_ORDER = [
    field.name for field in ThresholdInfo.DESCRIPTOR.fields
]
# Put metric_name at the beginning
DEFAULT_THRESHOLD_INFO_KEY_ORDER.remove("metric_name")
DEFAULT_THRESHOLD_INFO_KEY_ORDER = ["metric_name"] + DEFAULT_THRESHOLD_INFO_KEY_ORDER
