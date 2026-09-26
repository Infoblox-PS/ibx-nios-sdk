# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Tests for DNS shared nested-type models."""

from __future__ import annotations

from ibx_nios_sdk.dns.models._shared import (
    CloudInfo,
    ExtServer,
    MemberServer,
)


def test_ext_server_parses_minimal_payload() -> None:
    ext = ExtServer.model_validate({"address": "10.0.0.1", "name": "dns1.example.com"})
    assert ext.address == "10.0.0.1"
    assert ext.name == "dns1.example.com"


def test_ext_server_supports_stealth_and_tsig() -> None:
    ext = ExtServer.model_validate(
        {
            "address": "10.0.0.1",
            "name": "dns1.example.com",
            "stealth": True,
            "tsig_key_name": "my-key",
            "tsig_key_alg": "HMAC-SHA256",
            "use_tsig_key_name": True,
        }
    )
    assert ext.stealth is True
    assert ext.tsig_key_alg == "HMAC-SHA256"


def test_member_server_parses() -> None:
    ms = MemberServer.model_validate(
        {
            "name": "member1.local",
            "enable_preferred_primaries": False,
            "grid_replicate": True,
            "lead": False,
            "stealth": False,
        }
    )
    assert ms.name == "member1.local"
    assert ms.grid_replicate is True


def test_cloud_info_parses() -> None:
    ci = CloudInfo.model_validate(
        {
            "authority_type": "GM",
            "delegated_scope": "ROOT",
        }
    )
    assert ci.authority_type == "GM"


def test_extra_fields_allowed() -> None:
    ext = ExtServer.model_validate({"address": "1.1.1.1", "name": "x", "some_new_field": 123})
    assert ext.address == "1.1.1.1"
