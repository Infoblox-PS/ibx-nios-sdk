# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Captiveportal - NIOS captive portal settings."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "name",
        "uuid",
    }
)


class Captiveportal(BaseModel):
    """NIOS captive portal settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    authn_server_group: str | None = Field(
        default=None,
        description="The authentication server group assigned to this captive portal.",
    )
    company_name: str | None = Field(
        default=None, description="The company name that appears in the guest registration page."
    )
    enable_syslog_auth_failure: bool | None = Field(
        default=None,
        description="Determines if authentication failures are logged to syslog or not.",
    )
    enable_syslog_auth_success: bool | None = Field(
        default=None,
        description="Determines if successful authentications are logged to syslog or not.",
    )
    enable_user_type: Literal["AUTHENTICATED", "BOTH", "GUEST"] | str | None = Field(
        default=None, description="The type of user to be enabled for the captive portal."
    )
    encryption: Literal["NONE", "SSL"] | str | None = Field(
        default=None, description="The encryption the captive portal uses."
    )
    files: list[dict[str, Any]] | None = Field(
        default=None, description="The list of files associated with the captive portal."
    )
    guest_custom_field1_name: str | None = Field(
        default=None,
        description="The name of the custom field that you are adding to the guest registration page.",
    )
    guest_custom_field1_required: bool | None = Field(
        default=None, description="Determines if the custom field is required or not."
    )
    guest_custom_field2_name: str | None = Field(
        default=None,
        description="The name of the custom field that you are adding to the guest registration page.",
    )
    guest_custom_field2_required: bool | None = Field(
        default=None, description="Determines if the custom field is required or not."
    )
    guest_custom_field3_name: str | None = Field(
        default=None,
        description="The name of the custom field that you are adding to the guest registration page.",
    )
    guest_custom_field3_required: bool | None = Field(
        default=None, description="Determines if the custom field is required or not."
    )
    guest_custom_field4_name: str | None = Field(
        default=None,
        description="The name of the custom field that you are adding to the guest registration page.",
    )
    guest_custom_field4_required: bool | None = Field(
        default=None, description="Determines if the custom field is required or not."
    )
    guest_email_required: bool | None = Field(
        default=None,
        description="Determines if the email address of the guest is required or not.",
    )
    guest_first_name_required: bool | None = Field(
        default=None, description="Determines if the first name of the guest is required or not."
    )
    guest_last_name_required: bool | None = Field(
        default=None, description="Determines if the last name of the guest is required or not."
    )
    guest_middle_name_required: bool | None = Field(
        default=None, description="Determines if the middle name of the guest is required or not."
    )
    guest_phone_required: bool | None = Field(
        default=None, description="Determines if the phone number of the guest is required or not."
    )
    helpdesk_message: str | None = Field(
        default=None,
        description="The helpdesk message that appears in the guest registration page.",
    )
    listen_address_ip: str | None = Field(
        default=None,
        description="Determines the IP address on which the captive portal listens. Valid if listen address type is 'IP'.",
    )
    listen_address_type: Literal["VIP", "LAN2", "IP"] | str | None = Field(
        default=None,
        description="Determines the type of the IP address on which the captive portal listens.",
    )  # read-only
    name: str | None = Field(
        default=None, description="The hostname of the Grid member that hosts the captive portal."
    )
    network_view: str | None = Field(
        default=None, description="The network view of the captive portal."
    )
    port: int | None = Field(
        default=None,
        description="The TCP port used by the Captive Portal service. The port is required when the Captive Portal service is enabled. Valid values are between 1 and 63999. Please note that setting the port number to 80 or 443 might impact performance.",
    )
    service_enabled: bool | None = Field(
        default=None, description="Determines if the captive portal service is enabled or not."
    )
    syslog_auth_failure_level: (
        Literal["EMERG", "INFO", "DEBUG", "WARNING", "NOTICE", "ALERT", "CRIT", "ERR"] | str | None
    ) = Field(
        default=None, description="The syslog level at which authentication failures are logged."
    )
    syslog_auth_success_level: (
        Literal["EMERG", "INFO", "DEBUG", "WARNING", "NOTICE", "ALERT", "CRIT", "ERR"] | str | None
    ) = Field(
        default=None,
        description="The syslog level at which successful authentications are logged.",
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    welcome_message: str | None = Field(
        default=None,
        description="The welcome message that appears in the guest registration page.",
    )
