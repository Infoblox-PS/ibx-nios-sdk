# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridThreatprotection - NIOS Grid threat protection settings.

All properties from ``components.schemas.GridThreatprotection`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "grid_name",
        "last_checked_for_update",
        "last_rule_update_timestamp",
        "last_rule_update_version",
        "uuid",
    }
)


class GridThreatprotection(BaseModel):
    """NIOS Grid threat protection settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    current_ruleset: str | None = Field(default=None, description="The current Grid ruleset.")
    disable_multiple_dns_tcp_request: bool | None = Field(
        default=None,
        description="Determines if multiple BIND responses via TCP connection are disabled.",
    )
    enable_accel_resp_before_threat_protection: bool | None = Field(
        default=None,
        description="Determines if DNS responses are sent from acceleration cache before applying Threat Protection rules. Recommended for better performance when using DNS Cache Acceleration.",
    )
    enable_auto_download: bool | None = Field(
        default=None, description="Determines if auto download service is enabled."
    )
    enable_nat_rules: bool | None = Field(
        default=None,
        description="Determines if NAT (Network Address Translation) mapping for threat protection is enabled or not.",
    )
    enable_scheduled_download: bool | None = Field(
        default=None,
        description="Determines if scheduled download is enabled. The default frequency is once in every 24 hours if it is disabled.",
    )
    events_per_second_per_rule: int | None = Field(
        default=None, description="The number of events logged per second per rule."
    )  # read-only
    grid_name: str | None = Field(default=None, description="The Grid name.")  # read-only
    last_checked_for_update: int | None = Field(
        default=None, description="The time when the Grid last checked for updates."
    )  # read-only
    last_rule_update_timestamp: int | None = Field(
        default=None, description="The last rule update timestamp."
    )  # read-only
    last_rule_update_version: str | None = Field(
        default=None, description="The version of last rule update."
    )
    nat_rules: list[dict[str, Any]] | None = Field(
        default=None, description="The list of NAT mapping rules for threat protection."
    )
    outbound_settings: dict[str, Any] | None = Field(
        default=None, description="Outbound update/sync settings."
    )
    rule_update_policy: Literal["AUTOMATIC", "MANUAL"] | str | None = Field(
        default=None, description="The update rule policy."
    )
    scheduled_download: dict[str, Any] | None = Field(
        default=None, description="Settings for scheduled threat-data downloads."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    atp_object_reset: object | None = Field(default=None)
    test_atp_server_connectivity: object | None = Field(default=None)
