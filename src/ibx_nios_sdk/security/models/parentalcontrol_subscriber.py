# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscriber - NIOS parental-control subscriber configuration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset({"uuid", "zvelo_update_failure_in_days"})


class ParentalcontrolSubscriber(BaseModel):
    """NIOS parental-control subscriber configuration."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    alt_subscriber_id: str | None = Field(
        default=None, description="RADIUS attribute used as alternate subscriber id."
    )
    alt_subscriber_id_regexp: str | None = Field(
        default=None, description="Regex applied to the alternate subscriber id."
    )
    alt_subscriber_id_subexpression: int | None = Field(
        default=None, description="Regex sub-expression index for the alternate subscriber id."
    )
    ancillaries: list[str] | None = Field(
        default=None, description="List of ancillary RADIUS attribute names."
    )
    cat_acctname: str | None = Field(default=None, description="Category update account name.")
    cat_password: str | None = Field(default=None, description="Category update account password.")
    cat_update_frequency: int | None = Field(
        default=None, description="Category update frequency, in hours."
    )
    category_url: str | None = Field(default=None, description="Category update URL.")
    enable_mgmt_only_nas: bool | None = Field(
        default=None, description="Enable management-only NAS."
    )
    enable_parental_control: bool | None = Field(
        default=None, description="Enable parental control."
    )
    interim_accounting_interval: int | None = Field(
        default=None, description="Interim accounting interval, in seconds."
    )
    ip_anchors: list[str] | None = Field(default=None, description="IP anchor addresses.")
    ip_space_disc_regexp: str | None = Field(
        default=None, description="Regex applied to the IP space discriminator."
    )
    ip_space_disc_subexpression: int | None = Field(
        default=None, description="Regex sub-expression index for IP space discriminator."
    )
    ip_space_discriminator: str | None = Field(
        default=None, description="RADIUS attribute used as IP space discriminator."
    )
    local_id: str | None = Field(default=None, description="RADIUS attribute used as local id.")
    local_id_regexp: str | None = Field(default=None, description="Regex applied to the local id.")
    local_id_subexpression: int | None = Field(
        default=None, description="Regex sub-expression index for local id."
    )
    log_guest_lookups: bool | None = Field(default=None, description="Log guest lookups.")
    nas_context_info: str | None = Field(default=None, description="NAS context info.")
    pc_zone_name: str | None = Field(default=None, description="Parental-control zone name.")
    proxy_password: str | None = Field(default=None, description="Proxy password.")
    proxy_url: str | None = Field(default=None, description="Proxy URL.")
    proxy_username: str | None = Field(default=None, description="Proxy username.")
    subscriber_id: str | None = Field(
        default=None, description="RADIUS attribute used as subscriber id."
    )
    subscriber_id_regexp: str | None = Field(
        default=None, description="Regex applied to the subscriber id."
    )
    subscriber_id_subexpression: int | None = Field(
        default=None, description="Regex sub-expression index for subscriber id."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object."
    )  # RO
    zvelo_update_failure_in_days: int | None = Field(
        default=None, description="Days since the last Zvelo update failure."
    )  # RO
