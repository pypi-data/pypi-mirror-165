"""DxsEntries for all statistics."""
from dataclasses import dataclass

from pykostalpiko.dxs.entry import Descriptor, DescriptorOptions


@dataclass
class Day:
    """DxsEntries for the daily statistics."""

    YIELD = Descriptor(
        251658754, "Todays Yield", "Todays energy produced by the PV generator", "Wh"
    )
    HOME_CONSUMPTION = Descriptor(
        251659010,
        "Todays Home Consumption",
        "Todays energy consumed by the home.",
        "Wh",
    )
    SELF_CONSUMPTION = Descriptor(
        251659266,
        "Todays Self Consumption",
        "Todays energy consumed by the home, that was provided by the PV generator & battery."
        "Wh",
    )
    SELF_CONSUMPTION_RATE = Descriptor(
        251659278,
        "Todays Self Consumtion Rate",
        "Todays rate of self consumption.",
        "%",
    )
    DEGREE_OF_SELF_SUFFICIENCY = Descriptor(
        251659279,
        "Todays Degree of Self Sufficiency",
        "Todays degree of self sufficiency.",
        "%",
    )

    LIST = [
        YIELD,
        HOME_CONSUMPTION,
        SELF_CONSUMPTION,
        SELF_CONSUMPTION_RATE,
        DEGREE_OF_SELF_SUFFICIENCY,
    ]
    LIST_ALL = LIST


@dataclass
class Total:
    """DxsEntries for the total statistics."""

    YIELD = Descriptor(
        251658753,
        "Total Yield",
        "Total energy produced by the PV generator",
        "Wh",
        DescriptorOptions(multiplication_factor=1000),
    )
    HOME_CONSUMPTION = Descriptor(
        251659009,
        "Total Home Consumption",
        "Total energy consumed by the home.",
        "Wh",
        DescriptorOptions(multiplication_factor=1000),
    )
    SELF_CONSUMPTION = Descriptor(
        251659265,
        "Total Self Consumption",
        "Total energy consumed by the home, that was provided by the PV generator & battery.",
        "Wh",
        DescriptorOptions(multiplication_factor=1000),
    )
    SELF_CONSUMPTION_RATE = Descriptor(
        251659280,
        "Total Self Consumtion Rate",
        "All-time rate of self consumption.",
        "%",
    )
    DEGREE_OF_SELF_SUFFICIENCY = Descriptor(
        251659281,
        "Total Degree of Self Sufficiency",
        "All-time degree of self sufficiency.",
        "%",
    )
    OPERATION_TIME = Descriptor(
        251658496, "Operation Time", "Running time of the inverter.", "h"
    )

    LIST = [
        YIELD,
        HOME_CONSUMPTION,
        SELF_CONSUMPTION,
        SELF_CONSUMPTION_RATE,
        DEGREE_OF_SELF_SUFFICIENCY,
        OPERATION_TIME,
    ]
    LIST_ALL = LIST


LIST = []
LIST_ALL = LIST + Day.LIST_ALL + Total.LIST_ALL
