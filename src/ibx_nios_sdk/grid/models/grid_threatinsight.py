# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridThreatinsight - NIOS Grid threat insight settings.

All properties from ``components.schemas.GridThreatinsight`` in the v2.14 grid swagger.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "current_allowlist",
        "current_moduleset",
        "last_allowlist_update_time",
        "last_allowlist_update_version",
        "last_checked_for_allowlist_update",
        "last_checked_for_package_update",
        "last_checked_for_update",
        "last_module_update_time",
        "last_module_update_version",
        "last_updated_package_version",
        "name",
        "uuid",
    }
)


class GridThreatinsight(BaseModel):
    """NIOS Grid threat insight settings."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    allowlist_update_policy: Literal["MANUAL", "AUTOMATIC"] | str | None = Field(
        default=None, description="allowlist update policy (manual or automatic)"
    )
    configure_domain_collapsing: bool | None = Field(
        default=None, description="Disable domain collapsing at grid level"
    )  # read-only
    current_allowlist: str | None = Field(
        default=None, description="The Grid allowlist."
    )  # read-only
    current_moduleset: str | None = Field(
        default=None, description="The current threat insight module set."
    )
    dns_tunnel_block_list_rpz_zones: list[str] | None = Field(
        default=None, description="The list of response policy zones for DNS tunnelling requests."
    )
    domain_collapsing_level: int | None = Field(
        default=None, description="Level of domain collapsing"
    )
    enable_allowlist_auto_download: bool | None = Field(
        default=None, description="Indicates whether auto download service is enabled"
    )
    enable_allowlist_scheduled_download: bool | None = Field(
        default=None,
        description="Indicates whether the custom scheduled settings for auto download is enabled. If false then default frequency is once per 24 hours",
    )
    enable_auto_download: bool | None = Field(
        default=None,
        description="Determines whether the automatic threat insight module set download is enabled.",
    )
    enable_scheduled_download: bool | None = Field(
        default=None,
        description="Determines whether the scheduled download of the threat insight module set is enabled.",
    )  # read-only
    last_allowlist_update_time: int | None = Field(
        default=None, description="The last update time for the threat insight allowlist."
    )  # read-only
    last_allowlist_update_version: str | None = Field(
        default=None,
        description="The version number of the last updated threat insight allowlist.",
    )  # read-only
    last_checked_for_allowlist_update: int | None = Field(
        default=None, description="Timestamp of last checked allowlist"
    )  # read-only
    last_checked_for_package_update: int | None = Field(
        default=None, description="The last update time for the threat insight moduleset package."
    )  # read-only
    last_checked_for_update: int | None = Field(
        default=None,
        description="The last time when the threat insight module set was checked for the update.",
    )  # read-only
    last_module_update_time: int | None = Field(
        default=None, description="The last update time for the threat insight module set."
    )  # read-only
    last_module_update_version: str | None = Field(
        default=None,
        description="The version number of the last updated threat insight module set.",
    )  # read-only
    last_updated_package_version: str | None = Field(
        default=None, description="The version number of the last updated Moduleset package."
    )
    module_update_policy: Literal["AUTOMATIC", "MANUAL"] | str | None = Field(
        default=None, description="The update policy for the threat insight module set."
    )  # read-only
    name: str | None = Field(default=None, description="The Grid name.")
    scheduled_allowlist_download: dict[str, Any] | None = Field(default=None)
    scheduled_download: dict[str, Any] | None = Field(
        default=None, description="Settings for scheduled threat-data downloads."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
    download_threat_insight_allowlist_update: object | None = Field(default=None)
    download_threat_insight_moduleset_update: object | None = Field(default=None)
    move_blocklist_rpz_to_allow_list: object | None = Field(default=None)
    set_last_uploaded_threat_insight_moduleset: object | None = Field(default=None)
    test_threat_insight_server_connectivity: object | None = Field(default=None)
    update_threat_insight_moduleset: object | None = Field(default=None)
