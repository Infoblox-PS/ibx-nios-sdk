# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""MssuperscopeResource - NIOS MS server superscope, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.microsoftserver.models.mssuperscope import READONLY_FIELDS, Mssuperscope


class MssuperscopeResource(WapiResource[Mssuperscope]):
    """Manage NIOS Microsoft server superscope objects."""

    _wapi_type = "mssuperscope"
    _model = Mssuperscope
    _default_return_fields = ["name", "network_view", "comment"]
    _readonly_fields = set(READONLY_FIELDS)
