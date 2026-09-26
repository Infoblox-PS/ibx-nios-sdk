# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Orderedresponsepolicyzones resource - ordered RPZ CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.dns.models.orderedresponsepolicyzones import (
    READONLY_FIELDS,
    Orderedresponsepolicyzones,
)


class OrderedresponsepolicyzonesResource(WapiResource[Orderedresponsepolicyzones]):
    """Manage NIOS ordered response policy zones configurations."""

    _wapi_type = "orderedresponsepolicyzones"
    _model = Orderedresponsepolicyzones
    _default_return_fields = ["view", "rp_zones"]
    _readonly_fields = set(READONLY_FIELDS)
