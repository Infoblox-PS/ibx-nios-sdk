# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""TftpfiledirResource - NIOS TFTP file directory, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.tftpfiledir import READONLY_FIELDS, Tftpfiledir


class TftpfiledirResource(WapiResource[Tftpfiledir]):
    """Manage NIOS TFTP file directory objects."""

    _wapi_type = "tftpfiledir"
    _model = Tftpfiledir
    _default_return_fields = ["name", "type", "directory"]
    _readonly_fields = set(READONLY_FIELDS)
    _create_only_fields = {"directory", "type"}
