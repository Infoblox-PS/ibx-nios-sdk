# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Networkview - NIOS IPAM network view.

All 17 properties from ``components.schemas.Networkview`` in the v2.14 IPAM
swagger are represented here.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue
from ibx_nios_sdk.ipam.models._shared import _IpamNested

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "associated_dns_views",
        "associated_members",
        "is_default",
        "ms_ad_user_data",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Networkview-specific nested types
# ---------------------------------------------------------------------------


class NetworkviewCloudInfo(_IpamNested):
    """Cloud provider metadata for a network view.

    NOTE: Deeply nested delegated_member varies by context; typed as Any.
    """

    authority_type: Literal["NONE", "GM", "CP"] | str | None = Field(
        default=None, description="Type of authority over the object."
    )
    delegated_member: Any | None = Field(
        default=None,
        description="The Cloud Platform Appliance to which authority of the object is delegated.",
    )
    delegated_root: str | None = Field(
        default=None,
        description="Indicates the root of the delegation if delegated_scope is SUBTREE or RECLAIMING. This is not set otherwise.",
    )
    delegated_scope: Literal["NONE", "ROOT", "SUBTREE", "RECLAIMING"] | str | None = Field(
        default=None,
        description="Indicates the scope of delegation for the object. This can be one of the following: NONE (outside any delegation), ROOT (the delegation point), SUBTREE (within the scope of a delegation), RECLAIMING (within the scope of a delegation being reclaimed, either as the delegation point or in the subtree).",
    )
    mgmt_platform: str | None = Field(
        default=None, description="Indicates the specified cloud management platform."
    )
    owned_by_adaptor: bool | None = Field(
        default=None,
        description="Determines whether the object was created by the cloud adapter or not.",
    )
    tenant: str | None = Field(
        default=None,
        description="Reference to the tenant object associated with the object, if any.",
    )
    usage: Literal["NONE", "ADAPTER", "USED_BY", "DELEGATED"] | str | None = Field(
        default=None, description="Indicates the cloud origin of the object."
    )


class NetworkviewMsAdUserData(_IpamNested):
    """Microsoft Active Directory user data for a network view."""

    active_users_count: int | None = Field(
        default=None, description="The number of active users."
    )  # ---------------------------------------------------------------------------


# Main Networkview model
# ---------------------------------------------------------------------------


class Networkview(BaseModel):
    """NIOS IPAM network view.

    All 17 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    associated_dns_views: list[str] | None = Field(
        default=None, description="The list of DNS views associated with this network view."
    )
    associated_members: list[dict[str, Any]] | None = Field(
        default=None, description="The list of members associated with a network view."
    )  # --- cloud info ---
    cloud_info: NetworkviewCloudInfo | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common ---
    comment: str | None = Field(
        default=None, description="Comment for the network view; maximum 256 characters."
    )  # --- DDNS ---
    ddns_dns_view: str | None = Field(
        default=None,
        description="DNS views that will receive the updates if you enable the appliance to send updates to Grid members.",
    )
    ddns_zone_primaries: list[dict[str, Any]] | None = Field(
        default=None,
        description="An array of Ddns Zone Primary dhcpddns structs that lists the information of primary zone to which DDNS updates should be sent.",
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- realms ---
    federated_realms: list[dict[str, Any]] | None = Field(
        default=None,
        description="This field contains the federated realms associated to this network view",
    )  # --- zones ---
    internal_forward_zones: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of linked authoritative DNS zones."
    )  # --- read-only ---
    is_default: bool | None = Field(
        default=None,
        description="The NIOS appliance provides one default network view. You can rename the default view and change its settings, but you cannot delete it. There must always be at least one network view in the appliance.",
    )  # --- private cloud management ---
    mgm_private: bool | None = Field(
        default=None,
        description="This field controls whether this object is synchronized with the Multi-Grid Master. If this field is set to True, objects are not synchronized.",
    )  # --- MS AD user data ---
    ms_ad_user_data: NetworkviewMsAdUserData | None = Field(
        default=None, description="Microsoft Active Directory user-related information."
    )  # --- core identity ---
    name: str | None = Field(
        default=None, description="Name of the network view."
    )  # --- remote zones ---
    remote_forward_zones: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of forward-mapping zones to which the DHCP server sends the updates.",
    )
    remote_reverse_zones: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of reverse-mapping zones to which the DHCP server sends the updates.",
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
