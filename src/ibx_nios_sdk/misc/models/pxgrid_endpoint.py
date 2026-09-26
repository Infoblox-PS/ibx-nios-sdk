# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""PxgridEndpoint - NIOS pxGrid endpoint object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
Function: POST /pxgrid:endpoint/{ref}/test_connection.

WAPI type: pxgrid:endpoint

NOTES:
- 'uuid', 'client_certificate_subject', 'client_certificate_valid_from',
  'client_certificate_valid_to' are read-only.
- 'publish_settings', 'subscribe_settings', 'template_instance', 'test_connection'
  are deeply-nested; typed as dict[str, Any] | None.
- 'outbound_members' is a list field.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "client_certificate_subject",
        "client_certificate_valid_from",
        "client_certificate_valid_to",
        "uuid",
    }
)


class PxgridEndpoint(BaseModel):
    """NIOS pxGrid endpoint."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    client_certificate_subject: str | None = Field(
        default=None, description="The Cisco ISE client certificate subject."
    )
    client_certificate_valid_from: int | None = Field(
        default=None, description="The pxgrid endpoint client certificate valid from."
    )
    client_certificate_valid_to: int | None = Field(
        default=None, description="The pxgrid endpoint client certificate valid to."
    )  # --- writable ---
    address: str | None = Field(
        default=None,
        description="The pxgrid endpoint IPv4 Address or IPv6 Address or Fully-Qualified Domain Name (FQDN)",
    )
    client_certificate_token: str | None = Field(
        default=None,
        description="The token returned by the uploadinit function call in object fileop for Cisco ISE client certificate.",
    )
    comment: str | None = Field(
        default=None, description="The Cisco ISE endpoint descriptive comment."
    )
    disable: bool | None = Field(
        default=None,
        description="Determines whether a Cisco ISE endpoint is disabled or not. When this is set to False, the Cisco ISE endpoint is enabled.",
    )
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    log_level: Literal["ERROR", "WARNING", "INFO", "DEBUG"] | str | None = Field(
        default=None, description="The log level for a notification pxgrid endpoint."
    )
    name: str | None = Field(default=None, description="The name of the pxgrid endpoint.")
    network_view: str | None = Field(default=None, description="The pxgrid network view name.")
    outbound_member_type: Literal["MEMBER", "GM"] | str | None = Field(
        default=None, description="The outbound member that will generate events."
    )
    outbound_members: list[str] | None = Field(
        default=None, description="The list of members for outbound events."
    )
    publish_settings: dict[str, Any] | None = Field(
        default=None, description="Publish settings for outbound updates."
    )
    subscribe_settings: dict[str, Any] | None = Field(
        default=None,
        description="Subscription settings for receiving updates from upstream sources.",
    )
    template_instance: dict[str, Any] | None = Field(
        default=None, description="Reference to the template this object was instantiated from."
    )
    test_connection: dict[str, Any] | None = Field(
        default=None, description="Function-call payload for the test-connection operation."
    )
    timeout: int | None = Field(
        default=None, description="The timeout of session management (in seconds)."
    )
    vendor_identifier: str | None = Field(default=None, description="The vendor identifier.")
    wapi_user_name: str | None = Field(
        default=None, description="The user name for WAPI integration."
    )
    wapi_user_password: str | None = Field(
        default=None, description="The user password for WAPI integration."
    )
