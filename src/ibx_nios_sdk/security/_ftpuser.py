# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""FtpuserResource - full implementation."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.security.models.ftpuser import READONLY_FIELDS, Ftpuser


class FtpuserResource(WapiResource[Ftpuser]):
    """Manage NIOS FTP user objects."""

    _wapi_type = "ftpuser"
    _model = Ftpuser
    _default_return_fields = ["username"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"home_dir", "username"}
