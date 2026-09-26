# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DxlEndpoint - NIOS DXL endpoint object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
Functions: POST /dxl:endpoint/clear_outbound_worker_log,
           POST /dxl:endpoint/{ref}/test_broker_connectivity.

WAPI type: dxl:endpoint

NOTES:
- 'uuid', 'client_certificate_subject', 'client_certificate_valid_from',
  'client_certificate_valid_to' are read-only.
- 'brokers' is a list of nested objects; typed as list[dict[str, Any]] | None.
- 'template_instance', 'clear_outbound_worker_log', 'test_broker_connectivity'
  are deeply-nested; typed as dict[str, Any] | None.
- 'outbound_members' and 'topics' are list fields.
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


class DxlEndpoint(BaseModel):
    """NIOS DXL endpoint."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    client_certificate_subject: str | None = Field(
        default=None, description="The client certificate subject of a DXL endpoint."
    )
    client_certificate_valid_from: int | None = Field(
        default=None,
        description="The timestamp when client certificate for a DXL endpoint was created.",
    )
    client_certificate_valid_to: int | None = Field(
        default=None,
        description="The timestamp when the client certificate for a DXL endpoint expires.",
    )  # --- writable ---
    brokers: list[dict[str, Any]] | None = Field(
        default=None,
        description="The list of DXL endpoint brokers. Note that you cannot specify brokers and brokers_import_token at the same time.",
    )
    brokers_import_token: str | None = Field(
        default=None,
        description="The token returned by the uploadinit function call in object fileop for a DXL broker configuration file. Note that you cannot specify brokers and brokers_import_token at the same time.",
    )
    clear_outbound_worker_log: dict[str, Any] | None = Field(
        default=None,
        description="Function-call payload for the clear-outbound-worker-log operation.",
    )
    client_certificate_token: str | None = Field(
        default=None,
        description="The token returned by the uploadinit function call in object fileop for a DXL endpoint client certificate.",
    )
    comment: str | None = Field(default=None, description="The comment of a DXL endpoint.")
    disable: bool | None = Field(
        default=None, description="Determines whether a DXL endpoint is disabled."
    )
    extattrs: dict[str, Any] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    log_level: Literal["ERROR", "WARNING", "INFO", "DEBUG"] | str | None = Field(
        default=None, description="The log level for a DXL endpoint."
    )
    name: str | None = Field(default=None, description="The name of a DXL endpoint.")
    outbound_member_type: Literal["MEMBER", "GM"] | str | None = Field(
        default=None, description="The outbound member that will generate events."
    )
    outbound_members: list[str] | None = Field(
        default=None, description="The list of members for outbound events."
    )
    template_instance: dict[str, Any] | None = Field(
        default=None, description="Reference to the template this object was instantiated from."
    )
    test_broker_connectivity: dict[str, Any] | None = Field(default=None)
    timeout: int | None = Field(
        default=None, description="The timeout of session management (in seconds)."
    )
    topics: list[str] | None = Field(default=None, description="DXL topics")
    vendor_identifier: str | None = Field(default=None, description="The vendor identifier.")
    wapi_user_name: str | None = Field(
        default=None, description="The user name for WAPI integration."
    )
    wapi_user_password: str | None = Field(
        default=None, description="The user password for WAPI integration."
    )
