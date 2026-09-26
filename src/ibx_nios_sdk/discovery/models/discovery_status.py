# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryStatus - NIOS discovery status (read-only aggregate).

Operations: GET (collection and by ref) only.

NOTE: ``type`` is a Python keyword collision - aliased as ``type_``.
Nested info objects → dict[str, Any] | None.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "address",
        "cli_collection_enabled",
        "cli_credential_info",
        "existence_info",
        "fingerprint_enabled",
        "fingerprint_info",
        "first_seen",
        "last_action",
        "last_seen",
        "last_timestamp",
        "name",
        "network_view",
        "reachable_info",
        "sdn_collection_enabled",
        "sdn_collection_info",
        "snmp_collection_enabled",
        "snmp_collection_info",
        "snmp_credential_info",
        "status",
        "type",
        "type_",
    }
)


class DiscoveryStatus(BaseModel):
    """NIOS discovery status - read-only aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    address: str | None = Field(
        default=None, description="The IPv4 Address or IPv6 Address of the device."
    )
    cli_collection_enabled: bool | None = Field(
        default=None, description="Indicates if CLI collection is enabled."
    )
    cli_credential_info: dict[str, Any] | None = Field(default=None)
    existence_info: dict[str, Any] | None = Field(default=None)
    fingerprint_enabled: bool | None = Field(
        default=None, description="Indicates if DHCP fingerprinting is enabled."
    )
    fingerprint_info: dict[str, Any] | None = Field(default=None)
    first_seen: int | None = Field(
        default=None, description="The timestamp when the device was first discovered."
    )
    last_action: str | None = Field(
        default=None, description="The timestamp of the last detected interface property change."
    )
    last_seen: int | None = Field(
        default=None, description="The timestamp when the device was last discovered."
    )
    last_timestamp: int | None = Field(
        default=None, description="The timestamp of the last executed action for the device."
    )
    name: str | None = Field(default=None, description="The name of the device.")
    network_view: str | None = Field(
        default=None, description="The name of the network view in which this device resides."
    )
    reachable_info: dict[str, Any] | None = Field(default=None)
    sdn_collection_enabled: bool | None = Field(
        default=None, description="Indicate whether SDN collection enabled for the device."
    )
    sdn_collection_info: dict[str, Any] | None = Field(default=None)
    snmp_collection_enabled: bool | None = Field(
        default=None, description="Indicates if SNMP collection is enabled."
    )
    snmp_collection_info: dict[str, Any] | None = Field(default=None)
    snmp_credential_info: dict[str, Any] | None = Field(default=None)
    status: Literal["OK", "ERROR", "NOT_REACHABLE"] | str | None = Field(
        default=None, description="The overall status of the device."
    )  # Python keyword collision: type → type_
    type_: str | None = Field(default=None, alias="type", description="Object type discriminator.")
