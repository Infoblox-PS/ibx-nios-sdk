# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Tests for NiosError hierarchy and exception_for_status dispatcher."""

from __future__ import annotations

import pytest

from ibx_nios_sdk._exceptions import (
    AuthenticationError,
    BadRequestError,
    ConflictError,
    NiosConnectionError,
    NiosError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
    exception_for_status,
)


def test_base_carries_attrs() -> None:
    err = NiosError(status_code=500, message="boom", wapi_code="X", wapi_text="t")
    assert err.status_code == 500
    assert err.message == "boom"
    assert err.wapi_code == "X"
    assert err.wapi_text == "t"
    assert str(err) == "boom"


def test_hierarchy_subclasses_nios_error() -> None:
    for cls in (
        AuthenticationError,
        NotFoundError,
        BadRequestError,
        ConflictError,
        RateLimitError,
        ServerError,
        ValidationError,
        NiosConnectionError,
    ):
        assert issubclass(cls, NiosError)


@pytest.mark.parametrize(
    ("status", "expected_cls"),
    [
        (400, BadRequestError),
        (401, AuthenticationError),
        (404, NotFoundError),
        (409, ConflictError),
        (429, RateLimitError),
        (500, ServerError),
        (502, ServerError),
        (503, ServerError),
        (599, ServerError),
    ],
)
def test_exception_for_status_dispatch(status: int, expected_cls: type) -> None:
    err = exception_for_status(status, "msg", {"Error": "details", "code": "C", "text": "T"})
    assert isinstance(err, expected_cls)
    assert err.status_code == status


def test_exception_for_status_extracts_wapi_fields() -> None:
    err = exception_for_status(
        400, "msg", {"Error": "bad", "code": "Client.Ibap.Data", "text": "field x"}
    )
    assert err.wapi_code == "Client.Ibap.Data"
    assert err.wapi_text == "field x"


def test_exception_for_status_unknown_returns_base() -> None:
    err = exception_for_status(418, "teapot", None)
    assert type(err) is NiosError
    assert err.status_code == 418


def test_rate_limit_retry_after() -> None:
    err = exception_for_status(429, "rate", None, retry_after=5.0)
    assert isinstance(err, RateLimitError)
    assert err.retry_after == 5.0
