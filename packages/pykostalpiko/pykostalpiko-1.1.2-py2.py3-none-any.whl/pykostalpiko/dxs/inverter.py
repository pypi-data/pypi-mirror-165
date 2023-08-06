"""DxsEntries concering the properties of the inverter itself."""
from dataclasses import dataclass

from pykostalpiko.dxs.entry import (
    ConfigurableDescriptor,
    Descriptor,
    DescriptorOptions,
    MapperException,
)


def _operation_status_mapper(val: int) -> str:
    """Map the operation status to a string."""

    if val == 0:
        return "Off"
    if val == 1:
        return "Idle"
    if val == 2:
        return "Starting"
    if val == 3:
        return "Feed MPP"
    if val == 4:
        return "Deactivated"
    if val == 5:
        return "Feed"
    raise MapperException("Failed mapping Operation Status", val)


OPERATION_STATUS = Descriptor(
    16780032,
    "Operation Status",
    "Current status of the Inverter",
    options=DescriptorOptions(mapper_function=_operation_status_mapper),
)
SERIAL_NUMBER = Descriptor(16777728, "Serial Number", "Serial number of the inverter.")
ARTICLE_NUMBER = Descriptor(
    16777472, "Article Number", "Article number of the inverter."
)
COUNTRY_SETTINGS = Descriptor(
    16779522, "Country Settings", "Country settings of the inverter."
)
COUNTRY_SETTINGS_VERSION = Descriptor(
    16779521, "Country Settings Version", "Country settings version of the inverter."
)

NAME = ConfigurableDescriptor(16777984, "Name", "Name of the inverter.")
MODEL = Descriptor(16780544, "Model", "Model of the inverter.")

# TODO: /settings/general/login


@dataclass
class Versions:
    """DxsEntries describing the versions of the inverter."""

    USER_INTERFACE = Descriptor(
        16779267, "User Interface Version", "User interface version."
    )
    FIRMWARE = Descriptor(16779265, "Firmware Version", "Firmware version.")
    HARDWARE = Descriptor(16779266, "Hardware Version", "Hardware version.")
    # This is likely some abbreviation
    PAR = Descriptor(16779268, "PAR Version", "PAR version.")

    LIST = [USER_INTERFACE, FIRMWARE, HARDWARE, PAR]
    LIST_ALL = LIST


@dataclass
class Communication:
    """DxsEntries describing the communication with the inverter."""

    INVERTER_ADDRESS = ConfigurableDescriptor(
        117441025, "Inverter Address", "RS485 address of the inverter."
    )

    @dataclass
    class Network:
        """DxsEntries describing the network connection with the inverter."""

        MAC_ADDRESS = Descriptor(
            117440811, "MAC Address", "MAC address of the inverter."
        )

        @dataclass
        class IPAddress:
            """DxsEntries describing the IPv4 Address."""

            PART_1 = ConfigurableDescriptor(
                117440791, "IP Address Part 1", "First quadrant of the IPv4 address."
            )
            PART_2 = ConfigurableDescriptor(
                117440792, "IP Address Part 2", "Second quadrant of the IPv4 address."
            )
            PART_3 = ConfigurableDescriptor(
                117440793, "IP Address Part 3", "Third quadrant of the IPv4 address."
            )
            PART_4 = ConfigurableDescriptor(
                117440794, "IP Address Part 4", "Fourth quadrant of the IPv4 address."
            )

            LIST = [PART_1, PART_2, PART_3, PART_4]
            LIST_ALL = LIST

        @dataclass
        class SubnetMask:
            """DxsEntries describing the Subnet Mask."""

            PART_1 = ConfigurableDescriptor(
                117440795, "Subnet Mask Part 1", "First quadrant of the Subnet Mask."
            )
            PART_2 = ConfigurableDescriptor(
                117440796, "Subnet Mask Part 2", "Second quadrant of the Subnet Mask."
            )
            PART_3 = ConfigurableDescriptor(
                117440797, "Subnet Mask Part 3", "Third quadrant of the Subnet Mask."
            )
            PART_4 = ConfigurableDescriptor(
                117440798, "Subnet Mask Part 4", "Fourth quadrant of the Subnet Mask."
            )

            LIST = [PART_1, PART_2, PART_3, PART_4]
            LIST_ALL = LIST

        @dataclass
        class DefaultGateway:
            """DxsEntries describing the Default Gateway."""

            PART_1 = ConfigurableDescriptor(
                117440799,
                "Default Gateway Part 1",
                "First quadrant of the Default Gateway address.",
            )
            PART_2 = ConfigurableDescriptor(
                117440800,
                "Default Gateway Part 2",
                "Second quadrant of the Default Gateway address.",
            )
            PART_3 = ConfigurableDescriptor(
                117440801,
                "Default Gateway Part 3",
                "Third quadrant of the Default Gateway address.",
            )
            PART_4 = ConfigurableDescriptor(
                117440802,
                "Default Gateway Part 4",
                "Fourth quadrant of the Default Gateway address.",
            )

            LIST = [PART_1, PART_2, PART_3, PART_4]
            LIST_ALL = LIST

        @dataclass
        class DNSServer:
            """DxsEntries describing the DNS Server."""

            PART_1 = ConfigurableDescriptor(
                117440807,
                "DNS Server Part 1",
                "First quadrant of the DNS Server address.",
            )
            PART_2 = ConfigurableDescriptor(
                117440808,
                "DNS Server Part 2",
                "Second quadrant of the DNS Server address.",
            )
            PART_3 = ConfigurableDescriptor(
                117440809,
                "DNS Server Part 3",
                "Third quadrant of the DNS Server address.",
            )
            PART_4 = ConfigurableDescriptor(
                117440810,
                "DNS Server Part 4",
                "Fourth quadrant of the DNS Server address.",
            )

            LIST = [PART_1, PART_2, PART_3, PART_4]
            LIST_ALL = LIST

        LIST = [MAC_ADDRESS]
        LIST_ALL = (
            LIST
            + IPAddress.LIST_ALL
            + SubnetMask.LIST_ALL
            + DefaultGateway.LIST_ALL
            + DNSServer.LIST_ALL
        )

    LIST = [INVERTER_ADDRESS]
    LIST_ALL = LIST + Network.LIST_ALL


def _protocol_mapper(val: int) -> str:
    """Map the protocol to a string."""

    if val == 0:
        return "KOSTAL"
    if val == 1:
        return "Modbus"
    raise MapperException("Failed mapping Protocol", val)


@dataclass
class RS485:
    """DxsEntries describing the RS485 communication."""

    BUS_TERMINATION = ConfigurableDescriptor(117441027, "RS485 Bus Termination")
    BUS_BIAS_VOLTAGE = ConfigurableDescriptor(117441026, "RS485 Bus Bias Voltage")
    PROTOCOL = ConfigurableDescriptor(
        117441028,
        "RS485 Protocol",
        "DESCRIPTION",
        options=DescriptorOptions(mapper_function=_protocol_mapper),
    )
    BAUD_RATE = ConfigurableDescriptor(117441029, "RS485 Baud Rate", None)

    LIST = [BUS_TERMINATION, BUS_BIAS_VOLTAGE, PROTOCOL, BAUD_RATE]
    LIST_ALL = LIST


# TODO: /settings/communication/modem


@dataclass
class PortalConfiguration:
    """DxsEntries describing the portal configuration."""

    ACTIVE_PORTAL = Descriptor(117441538, "Active Portal", "Name of the active portal.")
    # 117441542 is an unknown dxsId

    LIST = [ACTIVE_PORTAL]
    LIST_ALL = LIST


@dataclass
class DataLogger:
    """DxsEntries describing the data logger."""

    LOG_INTERVAL = ConfigurableDescriptor(150995968, "Log Interval")

    LIST = [LOG_INTERVAL]
    LIST_ALL = LIST


# TODO: /settings/generator-configuration

# TODO: /settings/battery-configuration

# TODO: /settings/switching-output

# TODO: /settings/analog-inputs

LIST = [
    NAME,
    MODEL,
    OPERATION_STATUS,
    SERIAL_NUMBER,
    ARTICLE_NUMBER,
    COUNTRY_SETTINGS,
    COUNTRY_SETTINGS_VERSION,
]
LIST_ALL = (
    LIST
    + Versions.LIST_ALL
    + Communication.LIST_ALL
    + RS485.LIST_ALL
    + PortalConfiguration.LIST_ALL
    + DataLogger.LIST_ALL
)
