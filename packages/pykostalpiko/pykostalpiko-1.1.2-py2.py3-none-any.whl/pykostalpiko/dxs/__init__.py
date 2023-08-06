"""DxsEntries general constants and methods."""
from typing import Any

from pykostalpiko.dxs.current_values import LIST_ALL as current_values_LIST
from pykostalpiko.dxs.entry import Descriptor
from pykostalpiko.dxs.inverter import LIST_ALL as inverter_LIST
from pykostalpiko.dxs.statistics import LIST_ALL as statistics_LIST

LIST_ALL: list[Descriptor] = current_values_LIST + statistics_LIST + inverter_LIST


def find_descriptor_by_id(dxs_id: int) -> Descriptor:
    """Find a descriptor by its id."""
    for descriptor in LIST_ALL:
        if descriptor.key == dxs_id:
            return descriptor

    raise ValueError(f"No descriptor found for id {dxs_id}")


def get_value_by_descriptor(descriptor: Descriptor, data: dict) -> Any:
    """Get the value of a descriptor from a data dictionary."""
    return data[descriptor.name]
