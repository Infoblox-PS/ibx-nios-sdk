# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ParentalcontrolSubscriberrecord - NIOS parental-control subscriber record."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset()


class ParentalcontrolSubscriberrecord(BaseModel):
    """NIOS parental-control subscriber record."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    accounting_session_id: str | None = Field(default=None, description="Accounting session id.")
    alt_ip_addr: str | None = Field(default=None, description="Alternate IP address.")
    ans0: str | None = Field(default=None, description="Ancillary field 0.")
    ans1: str | None = Field(default=None, description="Ancillary field 1.")
    ans2: str | None = Field(default=None, description="Ancillary field 2.")
    ans3: str | None = Field(default=None, description="Ancillary field 3.")
    ans4: str | None = Field(default=None, description="Ancillary field 4.")
    black_list: str | None = Field(default=None, description="Black list name.")
    bwflag: bool | None = Field(default=None, description="Black/white list flag.")
    dynamic_category_policy: bool | None = Field(
        default=None, description="Dynamic category policy flag."
    )
    flags: str | None = Field(default=None, description="Subscriber record flags.")
    ip_addr: str | None = Field(default=None, description="Subscriber IP address.")
    ipsd: str | None = Field(default=None, description="IP space discriminator value.")
    localid: str | None = Field(default=None, description="Local id.")
    nas_contextual: str | None = Field(default=None, description="NAS contextual info.")
    op_code: str | None = Field(default=None, description="Operation code.")
    parental_control_policy: str | None = Field(
        default=None, description="Parental control policy."
    )
    prefix: int | None = Field(default=None, description="IP prefix length.")
    proxy_all: bool | None = Field(default=None, description="Proxy all flag.")
    site: str | None = Field(default=None, description="Subscriber site name.")
    subscriber_id: str | None = Field(default=None, description="Subscriber id.")
    subscriber_secure_policy: str | None = Field(
        default=None, description="Subscriber secure policy."
    )
    unknown_category_policy: bool | None = Field(
        default=None, description="Unknown category policy flag."
    )
    white_list: str | None = Field(default=None, description="White list name.")
    wpc_category_policy: str | None = Field(default=None, description="WPC category policy.")
