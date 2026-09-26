# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Cross-domain pydantic models shared across all WAPI domains."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ExtAttrValue(BaseModel):
    """Extensible-attribute value with optional inheritance metadata.

    WAPI shape:
        {"value": "NYC", "inheritance_source": {"_ref": "..."}}

    ``inheritance_source`` is only populated when the caller requested it
    via ``return_fields_plus=[..., "extattrs.<name>.inheritance_source"]``.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    value: str | int | bool | float = Field(description="The extensible-attribute value.")
    inheritance_source: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Inheritance metadata returned when the caller requests it via "
            "``return_fields_plus=[..., 'extattrs.<name>.inheritance_source']``."
        ),
    )


class DhcpOption(BaseModel):
    """A DHCP option entry (WAPI ``dhcpoption`` struct).

    Appears on objects that expose an ``options`` array such as networks,
    ranges, fixed addresses, shared networks, and their template variants.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    name: str | None = Field(default=None, description="Name of the DHCP option.")
    num: int | None = Field(default=None, description="The code of the DHCP option.")
    vendor_class: str | None = Field(
        default=None,
        description="The name of the space this DHCP option is associated to.",
    )
    value: str | None = Field(default=None, description="Value of the DHCP option")
    use_option: bool | None = Field(
        default=None,
        description=(
            "Only applies to special options that are displayed separately from other "
            "options and have a use flag. These options are: * routers * router-templates "
            "* domain-name-servers * domain-name * broadcast-address * "
            "broadcast-address-offset * dhcp-lease-time * dhcp6.name-servers"
        ),
    )


class MsDhcpOption(BaseModel):
    """A Microsoft DHCP option entry (WAPI ``msdhcpoption`` struct).

    Appears on objects that expose an ``ms_options`` array such as fixed
    addresses, ranges, and their template variants.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    num: int | None = Field(default=None, description="The code of the DHCP option.")
    value: str | None = Field(default=None, description="Value of the DHCP option.")
    name: str | None = Field(default=None, description="The name of the DHCP option.")
    vendor_class: str | None = Field(
        default=None,
        description="The name of the vendor class with which this DHCP option is associated.",
    )
    user_class: str | None = Field(
        default=None,
        description="The name of the user class with which this DHCP option is associated.",
    )
    type: str | None = Field(
        default=None,
        description=(
            'The DHCP option type. Valid values are: * "16-bit signed integer" * '
            '"16-bit unsigned integer" * "32-bit signed integer" * '
            '"32-bit unsigned integer" * "64-bit unsigned integer" * '
            '"8-bit signed integer" * "8-bit unsigned integer (1,2,4,8)" * '
            '"8-bit unsigned integer" * "array of 16-bit integer" * '
            '"array of 16-bit unsigned integer" * "array of 32-bit integer" * '
            '"array of 32-bit unsigned integer" * "array of 64-bit unsigned integer" * '
            '"array of 8-bit integer" * "array of 8-bit unsigned integer" * '
            '"array of ip-address pair" * "array of ip-address" * "array of string" * '
            '"binary" * "boolean array of ip-address" * "boolean" * "boolean-text" * '
            '"domain-list" * "domain-name" * "encapsulated" * "ip-address" * '
            '"string" * "text"'
        ),
    )


class LogicFilterRule(BaseModel):
    """A logic-filter rule entry (WAPI ``logicfilterrule`` struct).

    Appears on objects that expose a ``logic_filter_rules`` array such as
    networks, ranges, fixed addresses, shared networks, and grid/member
    DHCP properties.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    filter: str | None = Field(default=None, description="The filter name.")
    type: str | None = Field(
        default=None,
        description="The filter type. Valid values are: * MAC * NAC * Option",
    )
