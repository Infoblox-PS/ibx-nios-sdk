# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Gcpuser - NIOS GCP user object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

NOTE: The 'type' field from WAPI is aliased to 'type_' to avoid collision with
Python's built-in 'type'. Serialized as 'type' via Field(alias='type').
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "auth_provider_x509_cert_url",
        "auth_uri",
        "client_email",
        "client_id",
        "client_x509_cert_url",
        "file_name",
        "private_key_id",
        "project_id",
        "status",
        "token_uri",
        "type",
        "uuid",
    }
)


class Gcpuser(BaseModel):
    """NIOS GCP user.

    NOTES:
    - 'type_' is the SDK alias for the WAPI field 'type' (Python keyword collision).
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    status: Literal["UNUSED", "SUCCESSFUL", "UNSUCCESSFUL"] | str | None = Field(
        default=None, description="Indicate the validity status of this GCP user."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    auth_provider_x509_cert_url: str | None = Field(
        default=None,
        description="The URL where the public key certificates provided by the authentication provider can be retrieved.. Maximum 255 characters.",
    )
    auth_uri: str | None = Field(
        default=None,
        description="The URI where authentication requests should be directed.. Maximum 255 characters.",
    )
    client_email: str | None = Field(
        default=None,
        description="The email address associated with the service account. Maximum 255 characters.",
    )
    client_id: str | None = Field(
        default=None,
        description="The unique identifier for the service account. Maximum 64 characts.er",
    )
    client_x509_cert_url: str | None = Field(
        default=None,
        description="The URL where the public key certificate for the service account can be retrieved. Maximum 255 characters.",
    )
    file_name: str | None = Field(
        default=None, description="GCP client credentials file name.. Maximum 255 characters."
    )
    private_key_id: str | None = Field(
        default=None,
        description="The identifier for the private key associated with the service account. Maximum 64 characters.",
    )
    project_id: str | None = Field(
        default=None,
        description="The ID of the GCP project associated with the service account. Maximum 64 characters.",
    )
    token_uri: str | None = Field(
        default=None,
        description="The URI where token requests should be directed.. Maximum 255 characters.",
    )
    type_: str | None = Field(default=None, alias="type", description="Object type discriminator.")
    user_name: str | None = Field(
        default=None, description="The GCP client's user name. Maximum 64 characters."
    )
    last_used: int | None = Field(
        default=None, description="The timestamp when this Azure user credentials was last used."
    )
    private_key: str | None = Field(
        default=None,
        description="The private key used for authentication. Maximum 255 characters.",
    )
