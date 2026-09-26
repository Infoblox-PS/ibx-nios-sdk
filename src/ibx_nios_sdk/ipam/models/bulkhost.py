# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Bulkhost - NIOS IPAM bulk host object.

All 21 properties from ``components.schemas.Bulkhost`` in the v2.14 IPAM
swagger are represented here.

NOTE: The following complex nested schemas are inlined as dicts:
  - BulkhostCloudInfo
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "cloud_info",
        "dns_prefix",
        "last_queried",
        "network_view",
        "policy",
        "template_format",
        "uuid",
    }
)


# ---------------------------------------------------------------------------
# Main Bulkhost model
# ---------------------------------------------------------------------------


class Bulkhost(BaseModel):
    """NIOS IPAM bulk host object.

    All 21 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- cloud info (complex nested - dict) ---
    cloud_info: dict[str, Any] | None = Field(
        default=None, description="Cloud API related information for the object."
    )  # --- common ---
    comment: str | None = Field(
        default=None, description="The descriptive comment."
    )  # --- state ---
    disable: bool | None = Field(
        default=None, description="The disable flag of a DNS BulkHost record."
    )  # --- read-only ---
    dns_prefix: str | None = Field(
        default=None, description="The prefix, in punycode format, for the bulk host."
    )  # --- range ---
    end_addr: str | None = Field(
        default=None, description="The last IP address in the address range for the bulk host."
    )  # --- extended attributes ---
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )  # --- read-only ---
    last_queried: int | None = Field(
        default=None, description="The time of the last DNS query in Epoch seconds format."
    )  # --- naming ---
    name_template: str | None = Field(
        default=None, description="The bulk host name template."
    )  # --- read-only ---
    network_view: str | None = Field(
        default=None, description="The network view associated with the bulk host view."
    )  # --- read-only ---
    policy: str | None = Field(
        default=None,
        description="The hostname policy for records under the bulk host parent zone.",
    )  # --- identity ---
    prefix: str | None = Field(
        default=None,
        description="The prefix for the bulk host. The prefix is the name (or a series of characters) inserted at the beginning of each host name.",
    )  # --- reverse DNS ---
    reverse: bool | None = Field(
        default=None, description="The reverse flag of the BulkHost record."
    )  # --- range ---
    start_addr: str | None = Field(
        default=None, description="The first IP address in the address range for the bulk host."
    )  # --- read-only ---
    template_format: str | None = Field(
        default=None, description="The bulk host name template format."
    )  # --- TTL ---
    ttl: int | None = Field(
        default=None, description="The Time to Live (TTL) value."
    )  # --- naming flags ---
    use_name_template: bool | None = Field(default=None, description="Use flag for: name_template")
    use_ttl: bool | None = Field(
        default=None, description="Use flag for: ttl"
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- DNS view ---
    view: str | None = Field(
        default=None, description="The view for the bulk host."
    )  # --- DNS zone ---
    zone: str | None = Field(default=None, description="The zone name.")
