# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CertificateAuthservice - NIOS certificate authentication service.

All 20 properties from ``components.schemas.CertificateAuthservice`` in the
v2.14 security swagger are represented here. Complex nested fields
``ca_certificates``, ``ocsp_responders``, and ``test_ocsp_responder_settings``
are modelled as ``list[dict[str, Any]] | None`` / ``dict[str, Any] | None``
(see NOTES.md).

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true) - Python attribute names
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class CertificateAuthservice(BaseModel):
    """NIOS certificate authentication service.

    Read-only fields are collected in :data:`READONLY_FIELDS`; the resource
    strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    auto_populate_login: (
        Literal[
            "SERIAL_NUMBER", "S_DN_CN", "S_DN_EMAIL", "SAN_UPN", "SAN_EMAIL", "AD_SUBJECT_ISSUER"
        ]
        | str
        | None
    ) = Field(
        default=None,
        description="Specifies the value of the client certificate for automatically populating the NIOS login name.",
    )
    ca_certificates: list[dict[str, Any] | str] | None = Field(
        default=None, description="The list of CA certificates."
    )
    comment: str | None = Field(
        default=None,
        description="The descriptive comment for the certificate authentication service.",
    )
    disabled: bool | None = Field(
        default=None,
        description="Determines if this certificate authentication service is enabled or disabled.",
    )
    enable_password_request: bool | None = Field(
        default=None,
        description="Determines if username/password authentication together with client certificate authentication is enabled or disabled.",
    )
    enable_remote_lookup: bool | None = Field(
        default=None,
        description="Determines if the lookup for user group membership information on remote services is enabled or disabled.",
    )
    max_retries: int | None = Field(
        default=None,
        description="The number of validation attempts before the appliance contacts the next responder.",
    )
    name: str | None = Field(
        default=None, description="The name of the certificate authentication service."
    )
    ocsp_check: Literal["MANUAL", "AIA_ONLY", "AIA_AND_MANUAL", "DISABLED"] | str | None = Field(
        default=None, description="Specifies the source of OCSP settings."
    )
    ocsp_responders: list[dict[str, Any]] | None = Field(
        default=None,
        description="An ordered list of OCSP responders that are part of the certificate authentication service.",
    )
    recovery_interval: int | None = Field(
        default=None,
        description="The period of time the appliance waits before it attempts to contact a responder that is out of service again. The value must be between 1 and 600 seconds.",
    )
    remote_lookup_password: str | None = Field(
        default=None, description="The password for the service account."
    )
    remote_lookup_service: str | None = Field(
        default=None, description="The service that will be used for remote lookup."
    )
    remote_lookup_username: str | None = Field(
        default=None, description="The username for the service account."
    )
    response_timeout: int | None = Field(
        default=None, description="The validation timeout period in milliseconds."
    )
    test_ocsp_responder_settings: dict[str, Any] | None = Field(default=None)
    trust_model: Literal["DIRECT", "DELEGATED"] | str | None = Field(
        default=None, description="The OCSP trust model."
    )
    user_match_type: Literal["DIRECT_MATCH", "AUTO_MATCH"] | str | None = Field(
        default=None, description="Specifies how to search for a user."
    )
