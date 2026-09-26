# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Tests for shared cross-domain models."""

from __future__ import annotations

from ibx_nios_sdk._common.models import ExtAttrValue


def test_extattr_value_value_only() -> None:
    ea = ExtAttrValue.model_validate({"value": "NYC"})
    assert ea.value == "NYC"
    assert ea.inheritance_source is None


def test_extattr_value_with_inheritance() -> None:
    payload = {
        "value": "NYC",
        "inheritance_source": {"_ref": "network/abc:10.0.0.0/8/default"},
    }
    ea = ExtAttrValue.model_validate(payload)
    assert ea.value == "NYC"
    assert ea.inheritance_source == {"_ref": "network/abc:10.0.0.0/8/default"}


def test_extattr_value_serialize_excludes_none() -> None:
    ea = ExtAttrValue(value="NYC")
    dumped = ea.model_dump(exclude_none=True)
    assert dumped == {"value": "NYC"}


def test_extattr_value_extra_fields_allowed() -> None:
    ea = ExtAttrValue.model_validate(
        {"value": "NYC", "descendants_action": {"option_with_ea": "INHERIT"}}
    )
    assert ea.value == "NYC"
