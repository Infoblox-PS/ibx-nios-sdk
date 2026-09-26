# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryGridproperties - NIOS discovery grid properties.

Operations: GET (collection and by ref), PUT.
Also has function sub-paths (advisor_run_now, advisor_test_connection,
diagnostic, diagnostic_status) - represented as dict[str, Any] | None.

NOTE: Deeply nested settings structures → dict[str, Any] | None.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "grid_name",
        "uuid",
    }
)


class DiscoveryGridproperties(BaseModel):
    """NIOS discovery grid properties."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    grid_name: str | None = Field(default=None, description="The Grid name.")
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable (deeply nested → dict) ---
    advanced_polling_settings: dict[str, Any] | None = Field(default=None)
    advanced_sdn_polling_settings: dict[str, Any] | None = Field(default=None)
    advisor_run_now: dict[str, Any] | None = Field(default=None)
    advisor_settings: dict[str, Any] | None = Field(default=None)
    advisor_test_connection: dict[str, Any] | None = Field(default=None)
    auto_conversion_settings: list[dict[str, Any]] | None = Field(
        default=None, description="Automatic conversion settings."
    )
    basic_polling_settings: dict[str, Any] | None = Field(default=None)
    basic_sdn_polling_settings: dict[str, Any] | None = Field(default=None)
    cli_credentials: list[dict[str, Any]] | None = Field(
        default=None, description="Discovery CLI credentials."
    )
    device_hints: list[dict[str, Any]] | None = Field(default=None, description="Device Hints.")
    diagnostic: dict[str, Any] | None = Field(default=None)
    diagnostic_status: dict[str, Any] | None = Field(default=None)
    discovery_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Discovery blackout schedule for this object."
    )
    dns_lookup_option: Literal["ALL", "INFRAONLY", "OFF"] | str | None = Field(
        default=None, description="The type of the devices the DNS processor operates on."
    )
    dns_lookup_throttle: int | None = Field(
        default=None,
        description="The percentage of available capacity the DNS processor operates at. Valid values are unsigned integer between 1 and 100, inclusive.",
    )
    enable_advisor: bool | None = Field(
        default=None, description="Advisor application enabled/disabled."
    )
    enable_auto_conversion: bool | None = Field(
        default=None, description="The flag that enables automatic conversion of discovered data."
    )
    enable_auto_updates: bool | None = Field(
        default=None,
        description="The flag that enables updating discovered data for managed objects.",
    )
    ignore_conflict_duration: int | None = Field(
        default=None,
        description="Determines the timeout to ignore the discovery conflict duration (in seconds).",
    )
    port_control_blackout_setting: dict[str, Any] | None = Field(
        default=None, description="Port-control blackout schedule for this object."
    )
    ports: list[dict[str, Any]] | None = Field(default=None, description="Ports to scan.")
    same_port_control_discovery_blackout: bool | None = Field(
        default=None,
        description="Determines if the same port control is used for discovery blackout.",
    )
    snmpv1v2_credentials: list[dict[str, Any]] | None = Field(
        default=None, description="Discovery SNMP v1 and v2 credentials."
    )
    snmpv3_credentials: list[dict[str, Any]] | None = Field(
        default=None, description="Discovery SNMP v3 credentials."
    )
    unmanaged_ips_limit: int | None = Field(
        default=None,
        description="Limit of discovered unmanaged IP address which determines how frequently the user is notified about the new unmanaged IP address in a particular network.",
    )
    unmanaged_ips_timeout: int | None = Field(
        default=None,
        description="Determines the timeout between two notifications (in seconds) about the new unmanaged IP address in a particular network. The value must be between 60 seconds and the number of seconds remaining to Jan 2038.",
    )
    vrf_mapping_policy: Literal["NONE", "RULE_BASED", "RULE_AND_INTERNAL_BASED"] | str | None = (
        Field(
            default=None,
            description="The policy type used to define the behavior of the VRF mapping.",
        )
    )
    vrf_mapping_rules: list[dict[str, Any]] | None = Field(
        default=None, description="VRF mapping rules."
    )
