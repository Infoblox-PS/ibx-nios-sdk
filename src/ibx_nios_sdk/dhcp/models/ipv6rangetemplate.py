# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Ipv6rangetemplate - NIOS DHCP IPv6 range template.

All 16 properties from ``components.schemas.Ipv6rangetemplate`` in the v2.14 DHCP
swagger are represented here.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import LogicFilterRule

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Ipv6rangetemplate(BaseModel):
    """NIOS DHCP IPv6 range template."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    cloud_api_compatible: bool | None = Field(
        default=None,
        description="Determines whether the IPv6 DHCP range template can be used to create network objects in a cloud-computing deployment.",
    )
    comment: str | None = Field(
        default=None, description="The IPv6 DHCP range template descriptive comment."
    )
    delegated_member: dict[str, Any] | None = Field(
        default=None,
        description="The Cloud Platform Appliance to which authority of the object is delegated.",
    )
    exclude: list[dict[str, Any]] | None = Field(
        default=None,
        description="These are ranges of IPv6 addresses that the appliance does not use to assign to clients. You can use these excluded addresses as static IPv6 addresses. They contain the start and end addresses of the excluded range, and optionally, information about this excluded range.",
    )
    logic_filter_rules: list[LogicFilterRule] | None = Field(
        default=None,
        description="This field contains the logic filters to be applied on this IPv6 range. This list corresponds to the match rules that are written to the DHCPv6 configuration file.",
    )
    member: dict[str, Any] | None = Field(
        default=None, description="Reference to the Grid member that hosts this object."
    )
    name: str | None = Field(default=None, description="Name of the IPv6 DHCP range template.")
    number_of_addresses: int | None = Field(
        default=None, description="The number of addresses for the IPv6 DHCP range."
    )
    offset: int | None = Field(
        default=None, description="The start address offset for the IPv6 DHCP range."
    )
    option_filter_rules: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the Option filters to be applied to this IPv6 range. The appliance uses the matching rules of these filters to select the address range from which it assigns a lease.",
    )
    recycle_leases: bool | None = Field(
        default=None,
        description="Determines whether the leases are kept in Recycle Bin until one week after expiry. If this is set to False, the leases are permanently deleted.",
    )
    server_association_type: (
        Literal["NONE", "MEMBER", "FAILOVER", "MS_SERVER", "MS_FAILOVER"] | str | None
    ) = Field(
        default=None, description="The type of server that is going to serve the IPv6 DHCP range."
    )
    use_logic_filter_rules: bool | None = Field(
        default=None, description="Use flag for: logic_filter_rules"
    )
    use_recycle_leases: bool | None = Field(
        default=None, description="Use flag for: recycle_leases"
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
