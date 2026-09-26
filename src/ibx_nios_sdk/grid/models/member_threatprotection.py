# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberThreatprotection - NIOS member threat protection settings."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "hardware_model",
        "hardware_type",
        "host_name",
        "ipv4address",
        "ipv6address",
        "uuid",
    }
)


class MemberThreatprotection(BaseModel):
    """NIOS member threat protection settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    comment: str | None = Field(
        default=None,
        description="The human readable comment for member threat protection properties.",
    )
    current_ruleset: str | None = Field(
        default=None, description="The ruleset used for threat protection."
    )
    disable_multiple_dns_tcp_request: bool | None = Field(
        default=None,
        description="Determines if multiple BIND responses via TCP connection is enabled or not.",
    )
    enable_accel_resp_before_threat_protection: bool | None = Field(
        default=None,
        description="Determines if DNS responses are sent from acceleration cache before applying Threat Protection rules. Recommended for better performance when using DNS Cache Acceleration.",
    )
    enable_nat_rules: bool | None = Field(
        default=None,
        description="Determines if NAT (Network Address Translation) mapping for threat protection is enabled or not.",
    )
    enable_service: bool | None = Field(
        default=None, description="Determines if the Threat protection service is enabled or not."
    )
    events_per_second_per_rule: int | None = Field(
        default=None, description="The number of events logged per second per rule."
    )  # read-only
    hardware_model: str | None = Field(
        default=None, description="The hardware model of the member."
    )  # read-only
    hardware_type: str | None = Field(
        default=None, description="The hardware type of the member."
    )  # read-only
    host_name: str | None = Field(default=None, description="A Grid member name.")  # read-only
    ipv4address: str | None = Field(
        default=None, description="The IPv4 address of member threat protection service."
    )  # read-only
    ipv6address: str | None = Field(
        default=None, description="The IPv6 address of member threat protection service."
    )
    nat_rules: list[dict[str, Any]] | None = Field(
        default=None, description="The list of NAT rules."
    )
    outbound_settings: dict[str, Any] | None = Field(
        default=None, description="Outbound update/sync settings."
    )
    profile: str | None = Field(
        default=None, description="The Threat Protection profile associated with the member."
    )
    use_current_ruleset: bool | None = Field(
        default=None, description="Use flag for: current_ruleset"
    )
    use_events_per_second_per_rule: bool | None = Field(
        default=None, description="Use flag for: events_per_second_per_rule"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    use_disable_multiple_dns_tcp_request: bool | None = Field(default=None)
    use_enable_accel_resp_before_threat_protection: bool | None = Field(default=None)
    use_enable_nat_rules: bool | None = Field(default=None)
    use_outbound_settings: bool | None = Field(default=None)
