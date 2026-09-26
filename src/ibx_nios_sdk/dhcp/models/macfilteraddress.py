# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Macfilteraddress - NIOS DHCP MAC filter address.

All 22 properties from ``components.schemas.Macfilteraddress`` in the v2.14 DHCP
swagger are represented here.

NOTE: ``filter`` shadows the builtin but is not a keyword - kept as ``filter``.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "fingerprint",
        "is_registered_user",
        "uuid",
    }
)


class Macfilteraddress(BaseModel):
    """NIOS DHCP MAC filter address."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    authentication_time: int | None = Field(
        default=None,
        description="The absolute UNIX time (in seconds) since the address was last authenticated.",
    )
    comment: str | None = Field(
        default=None, description="Comment for the MAC filter address; maximum 256 characters."
    )
    expiration_time: int | None = Field(
        default=None, description="The absolute UNIX time (in seconds) until the address expires."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    filter: str | None = Field(
        default=None, description="Name of the MAC filter to which this address belongs."
    )  # noqa: A003 - shadows builtin, kept per NOTES.md

    # read-only
    fingerprint: str | None = Field(default=None, description="DHCP fingerprint for the address.")
    guest_custom_field1: str | None = Field(default=None, description="Guest custom field 1.")
    guest_custom_field2: str | None = Field(default=None, description="Guest custom field 2.")
    guest_custom_field3: str | None = Field(default=None, description="Guest custom field 3.")
    guest_custom_field4: str | None = Field(default=None, description="Guest custom field 4.")
    guest_email: str | None = Field(default=None, description="Guest e-mail.")
    guest_first_name: str | None = Field(default=None, description="Guest first name.")
    guest_last_name: str | None = Field(default=None, description="Guest last name.")
    guest_middle_name: str | None = Field(default=None, description="Guest middle name.")
    guest_phone: str | None = Field(default=None, description="Guest phone number.")  # read-only
    is_registered_user: bool | None = Field(
        default=None, description="Determines if the user has been authenticated or not."
    )
    mac: str | None = Field(default=None, description="MAC Address.")
    never_expires: bool | None = Field(
        default=None, description="Determines if MAC address expiration is enabled or disabled."
    )
    reserved_for_infoblox: str | None = Field(default=None, description="Reserved for future use.")
    username: str | None = Field(
        default=None, description="Username for authenticated DHCP purposes."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
