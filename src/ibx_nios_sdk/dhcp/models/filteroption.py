# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Filteroption - NIOS DHCP option filter."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Filteroption(BaseModel):
    """NIOS DHCP option filter."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    apply_as_class: bool | None = Field(
        default=None,
        description='Determines if apply as class is enabled or not. If this flag is set to "true" the filter is treated as global DHCP class, e.g it is written to dhcpd config file even if it is not present in any DHCP range.',
    )
    bootfile: str | None = Field(
        default=None, description="A name of boot file of a DHCP filter option object."
    )
    bootserver: str | None = Field(
        default=None,
        description="Determines the boot server of a DHCP filter option object. You can specify the name and/or IP address of the boot server that host needs to boot.",
    )
    comment: str | None = Field(
        default=None, description="The descriptive comment of a DHCP filter option object."
    )
    expression: str | None = Field(
        default=None, description="The conditional expression of a DHCP filter option object."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    lease_time: int | None = Field(
        default=None, description="Determines the lease time of a DHCP filter option object."
    )
    name: str | None = Field(default=None, description="The name of a DHCP option filter object.")
    next_server: str | None = Field(
        default=None,
        description="Determines the next server of a DHCP filter option object. You can specify the name and/or IP address of the next server that the host needs to boot.",
    )
    option_list: list[dict[str, Any]] | None = Field(
        default=None,
        description="An array of DHCP option dhcpoption structs that lists the DHCP options associated with the object.",
    )
    option_space: str | None = Field(
        default=None, description="The option space of a DHCP filter option object."
    )
    pxe_lease_time: int | None = Field(
        default=None,
        description="Determines the PXE (Preboot Execution Environment) lease time of a DHCP filter option object. To specify the duration of time it takes a host to connect to a boot server, such as a TFTP server, and download the file it needs to boot.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
