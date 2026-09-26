# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""NotificationRestEndpoint - NIOS notification REST endpoint object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

WAPI type: notification:rest:endpoint

NOTES:
- 'clear_outbound_worker_log', 'template_instance', 'test_connection' are nested
  structures; typed as dict[str, Any] | None.
- 'outbound_members' is typed as list[str] | None.
- 'client_certificate_subject', 'client_certificate_valid_from',
  'client_certificate_valid_to', 'uuid' are read-only.
- 'client_certificate_token', 'password', 'wapi_user_password' are write-only
  (not returned by WAPI reads).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "client_certificate_subject",
        "client_certificate_valid_from",
        "client_certificate_valid_to",
        "uuid",
    }
)


class NotificationRestEndpoint(BaseModel):
    """NIOS notification REST endpoint."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    client_certificate_subject: str | None = Field(
        default=None, description="The client certificate subject of a notification REST endpoint."
    )
    client_certificate_valid_from: int | None = Field(
        default=None,
        description="The timestamp when client certificate for a notification REST endpoint was created.",
    )
    client_certificate_valid_to: int | None = Field(
        default=None,
        description="The timestamp when client certificate for a notification REST endpoint expires.",
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- write-only (not returned by WAPI reads) ---
    client_certificate_token: str | None = Field(
        default=None,
        description="The token returned by the uploadinit function call in object fileop for a notification REST endpoint client certificate.",
    )
    password: str | None = Field(
        default=None,
        description="The password of the user that can log into a notification REST endpoint.",
    )
    wapi_user_password: str | None = Field(
        default=None, description="The user password for WAPI integration."
    )  # --- writable ---
    clear_outbound_worker_log: dict[str, Any] | None = Field(
        default=None,
        description="Function-call payload for the clear-outbound-worker-log operation.",
    )
    comment: str | None = Field(
        default=None, description="The comment of a notification REST endpoint."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    log_level: Literal["ERROR", "WARNING", "INFO", "DEBUG"] | str | None = Field(
        default=None, description="The log level for a notification REST endpoint."
    )
    name: str | None = Field(default=None, description="The name of a notification REST endpoint.")
    outbound_member_type: Literal["MEMBER", "GM"] | str | None = Field(
        default=None, description="The outbound member which will generate an event."
    )
    outbound_members: list[str] | None = Field(
        default=None, description="The list of members for outbound events."
    )
    server_cert_validation: (
        Literal["NO_VALIDATION", "CA_CERT", "CA_CERT_NO_HOSTNAME"] | str | None
    ) = Field(default=None, description="The server certificate validation type.")
    sync_disabled: bool | None = Field(
        default=None,
        description="Determines if the sync process is disabled for a notification REST endpoint.",
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
    uri: str | None = Field(default=None, description="The URI of a notification REST endpoint.")
    username: str | None = Field(
        default=None,
        description="The username of the user that can log into a notification REST endpoint.",
    )
    vendor_identifier: str | None = Field(default=None, description="The vendor identifier.")
    wapi_user_name: str | None = Field(
        default=None, description="The user name for WAPI integration."
    )
