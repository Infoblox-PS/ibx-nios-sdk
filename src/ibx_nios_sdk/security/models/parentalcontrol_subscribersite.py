# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscribersite - NIOS parental-control subscriber site."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset({"api_port", "uuid"})


class ParentalcontrolSubscribersite(BaseModel):
    """NIOS parental-control subscriber site."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    abss: list[dict[str, object]] | None = Field(
        default=None, description="Anycast border session servers."
    )
    api_members: list[dict[str, object]] | None = Field(
        default=None, description="API member configurations."
    )
    api_port: int | None = Field(default=None, description="API port.")  # RO
    block_size: int | None = Field(default=None, description="NAT block size.")
    blocking_ipv4_vip1: str | None = Field(default=None, description="Primary IPv4 blocking VIP.")
    blocking_ipv4_vip2: str | None = Field(
        default=None, description="Secondary IPv4 blocking VIP."
    )
    blocking_ipv6_vip1: str | None = Field(default=None, description="Primary IPv6 blocking VIP.")
    blocking_ipv6_vip2: str | None = Field(
        default=None, description="Secondary IPv6 blocking VIP."
    )
    comment: str | None = Field(default=None, description="Comment for the site.")
    dca_sub_bw_list: bool | None = Field(
        default=None, description="Enable DCA subscriber black/white list."
    )
    dca_sub_query_count: bool | None = Field(
        default=None, description="Enable DCA subscriber query count."
    )
    enable_gcp_precedence_over_allowed_list: bool | None = Field(
        default=None, description="Enable global content policy precedence over allow list."
    )
    enable_global_allow_list_rpz: bool | None = Field(
        default=None, description="Enable global allow-list RPZ."
    )
    enable_global_content_policy: bool | None = Field(
        default=None, description="Enable global content policy."
    )
    enable_rpz_filtering_bypass: bool | None = Field(
        default=None, description="Enable RPZ filtering bypass."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None, description="Extensible attributes associated with the object."
    )
    first_port: int | None = Field(default=None, description="First NAT port.")
    global_allow_list_rpz: int | None = Field(
        default=None, description="Global allow-list RPZ ordinal."
    )
    global_content_policy_bit_numbers: str | None = Field(
        default=None, description="Global content policy bit numbers."
    )
    maximum_subscribers: int | None = Field(
        default=None, description="Maximum number of subscribers."
    )
    members: list[dict[str, object]] | None = Field(
        default=None, description="Site member configurations."
    )
    msps: list[dict[str, object]] | None = Field(
        default=None, description="Managed service provider configurations."
    )
    name: str | None = Field(default=None, description="Site name.")
    nas_gateways: list[dict[str, object]] | None = Field(
        default=None, description="NAS gateway configurations."
    )
    nas_port: int | None = Field(default=None, description="NAS port.")
    proxy_rpz_passthru: bool | None = Field(default=None, description="Proxy RPZ pass-through.")
    spms: list[dict[str, object]] | None = Field(
        default=None, description="Service provider manager configurations."
    )
    stop_anycast: bool | None = Field(default=None, description="Stop anycast flag.")
    strict_nat: bool | None = Field(default=None, description="Strict NAT flag.")
    subscriber_collection_type: Literal["RADIUS", "API"] | str | None = Field(
        default=None, description="Subscriber collection type."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object."
    )  # RO
