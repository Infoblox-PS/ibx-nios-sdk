# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Filterrelayagent - NIOS DHCP relay agent filter."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ibx_nios_sdk._common.models import ExtAttrValue

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Filterrelayagent(BaseModel):
    """NIOS DHCP relay agent filter."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    circuit_id_name: str | None = Field(
        default=None,
        description="The circuit_id_name of a DHCP relay agent filter object. This filter identifies the circuit between the remote host and the relay agent. For example, the identifier can be the ingress interface number of the circuit access unit, perhaps concatenated with the unit ID number and slot number. Also, the circuit ID can be an ATM virtual circuit ID or cable data virtual circuit ID.",
    )
    circuit_id_substring_length: int | None = Field(
        default=None, description="The circuit ID substring length."
    )
    circuit_id_substring_offset: int | None = Field(
        default=None, description="The circuit ID substring offset."
    )
    comment: str | None = Field(
        default=None, description="A descriptive comment of a DHCP relay agent filter object."
    )
    extattrs: dict[str, ExtAttrValue] | None = Field(
        default=None,
        description="Extensible attributes associated with the object. For valid values for extensible attributes, see {extattrs:values}.",
    )
    is_circuit_id: Literal["MATCHES_VALUE", "NOT_SET", "ANY"] | str | None = Field(
        default=None,
        description='The circuit ID matching rule of a DHCP relay agent filter object. The circuit_id value takes effect only if the value is "MATCHES_VALUE".',
    )
    is_circuit_id_substring: bool | None = Field(
        default=None,
        description="Determines if the substring of circuit ID, instead of the full circuit ID, is matched.",
    )
    is_remote_id: Literal["MATCHES_VALUE", "NOT_SET", "ANY"] | str | None = Field(
        default=None,
        description="The remote ID matching rule of a DHCP relay agent filter object. The remote_id value takes effect only if the value is Matches_Value.",
    )
    is_remote_id_substring: bool | None = Field(
        default=None,
        description="Determines if the substring of remote ID, instead of the full remote ID, is matched.",
    )
    name: str | None = Field(
        default=None, description="The name of a DHCP relay agent filter object."
    )
    remote_id_name: str | None = Field(
        default=None,
        description="The remote ID name attribute of a relay agent filter object. This filter identifies the remote host. The remote ID name can represent many different things such as the caller ID telephone number for a dial-up connection, a user name for logging in to the ISP, a modem ID, etc. When the remote ID name is defined on the relay agent, the DHCP server will have a trusted relationship to identify the remote host. The remote ID name is considered as a trusted identifier.",
    )
    remote_id_substring_length: int | None = Field(
        default=None, description="The remote ID substring length."
    )
    remote_id_substring_offset: int | None = Field(
        default=None, description="The remote ID substring offset."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
