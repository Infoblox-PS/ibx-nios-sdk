# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MemberFiledistribution - NIOS member file distribution settings."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "ftp_status",
        "host_name",
        "http_status",
        "ipv4_address",
        "ipv6_address",
        "status",
        "tftp_status",
    }
)


class MemberFiledistribution(BaseModel):
    """NIOS member file distribution settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    allow_uploads: bool | None = Field(
        default=None, description="Determines whether uploads to the Grid member are allowed."
    )  # read-only
    comment: str | None = Field(default=None, description="The Grid member descriptive comment.")
    enable_ftp: bool | None = Field(
        default=None,
        description="Determines whether the FTP prtocol is enabled for file distribution.",
    )
    enable_ftp_filelist: bool | None = Field(
        default=None, description="Determines whether the LIST command for FTP is enabled."
    )
    enable_ftp_passive: bool | None = Field(
        default=None, description="Determines whether the passive mode for FTP is enabled."
    )
    enable_http: bool | None = Field(
        default=None,
        description="Determines whether the HTTP prtocol is enabled for file distribution.",
    )
    enable_http_acl: bool | None = Field(
        default=None,
        description="Determines whether the HTTP prtocol access control (AC) settings are enabled.",
    )
    enable_tftp: bool | None = Field(
        default=None,
        description="Determines whether the TFTP prtocol is enabled for file distribution.",
    )
    ftp_acls: list[dict[str, Any]] | None = Field(
        default=None, description="Access control (AC) settings for the FTP protocol."
    )
    ftp_port: int | None = Field(
        default=None, description="The network port used by the FTP protocol."
    )  # read-only
    ftp_status: Literal["UNKNOWN", "INACTIVE", "WORKING", "WARNING", "FAILED"] | str | None = (
        Field(default=None, description="The FTP protocol status.")
    )
    http_acls: list[dict[str, Any]] | None = Field(
        default=None, description="Access control (AC) settings for the HTTP protocol."
    )  # read-only
    host_name: str | None = Field(default=None, description="The Grid member host name.")
    http_status: Literal["UNKNOWN", "INACTIVE", "WORKING", "WARNING", "FAILED"] | str | None = (
        Field(default=None, description="The HTTP protocol status.")
    )  # read-only
    ipv4_address: str | None = Field(
        default=None, description="The IPv4 address of the Grid member."
    )  # read-only
    ipv6_address: str | None = Field(
        default=None, description="The IPv6 address of the Grid member."
    )  # read-only
    status: Literal["UNKNOWN", "INACTIVE", "WORKING", "WARNING", "FAILED"] | str | None = Field(
        default=None, description="The Grid member file distribution status."
    )
    tftp_acls: list[dict[str, Any]] | None = Field(
        default=None, description="The access control (AC) settings for the TFTP protocol."
    )
    tftp_port: int | None = Field(
        default=None, description="The network port used by the TFTP protocol."
    )  # read-only
    tftp_status: Literal["UNKNOWN", "INACTIVE", "WORKING", "WARNING", "FAILED"] | str | None = (
        Field(default=None, description="The TFTP protocol status.")
    )
    use_allow_uploads: bool | None = Field(default=None)
    uuid: str | None = Field(default=None)
