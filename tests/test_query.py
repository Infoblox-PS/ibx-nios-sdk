# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/test_query.py
"""Tests for the WAPI query-param builder."""

from __future__ import annotations

import pytest

from ibx_nios_sdk._query import build_filter_params, build_return_fields_params


def test_exact_filter() -> None:
    assert build_filter_params({"name": "host.example.com"}) == {"name": "host.example.com"}


def test_like_operator() -> None:
    assert build_filter_params({"name__like": "host"}) == {"name~": "host"}


def test_comparison_operators() -> None:
    assert build_filter_params({"count__gte": 5}) == {"count>": "5"}
    assert build_filter_params({"count__lte": 5}) == {"count<": "5"}
    assert build_filter_params({"name__not": "x"}) == {"name!": "x"}


def test_extattr_filter() -> None:
    assert build_filter_params({"extattr_Site": "NYC"}) == {"*Site": "NYC"}


def test_none_values_dropped() -> None:
    assert build_filter_params({"name": None, "view": "default"}) == {"view": "default"}


def test_unknown_operator_raises() -> None:
    with pytest.raises(ValueError, match="unknown filter operator"):
        build_filter_params({"name__weird": "x"})


def test_bool_values_lowercased() -> None:
    assert build_filter_params({"disable": True, "locked": False}) == {
        "disable": "true",
        "locked": "false",
    }


def test_return_fields_default_model_fields() -> None:
    params = build_return_fields_params(
        model_fields=["name", "view"], return_fields=None, return_fields_plus=None
    )
    assert params == {"_return_fields+": "name,view"}


def test_return_fields_exact() -> None:
    params = build_return_fields_params(
        model_fields=["name", "view"], return_fields=["name"], return_fields_plus=None
    )
    assert params == {"_return_fields": "name"}


def test_return_fields_plus() -> None:
    params = build_return_fields_params(
        model_fields=["name"], return_fields=None, return_fields_plus=["extattrs"]
    )
    assert params == {"_return_fields+": "name,extattrs"}


def test_return_fields_both_raises() -> None:
    with pytest.raises(ValueError, match="cannot pass both"):
        build_return_fields_params(
            model_fields=["name"], return_fields=["name"], return_fields_plus=["x"]
        )


def test_return_fields_empty_model_fields_plus_only() -> None:
    params = build_return_fields_params(
        model_fields=[], return_fields=None, return_fields_plus=["extattrs"]
    )
    assert params == {"_return_fields+": "extattrs"}


def test_return_fields_empty_model_fields_no_extras_returns_empty_dict() -> None:
    """When model_fields is empty and neither extra arg is given, return {}."""
    params = build_return_fields_params(
        model_fields=[], return_fields=None, return_fields_plus=None
    )
    assert params == {}
