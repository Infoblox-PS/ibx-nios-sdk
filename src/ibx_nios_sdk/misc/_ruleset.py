# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""RulesetResource - NIOS ruleset, full CRUD."""

from __future__ import annotations

from ibx_nios_sdk._resource import WapiResource
from ibx_nios_sdk.misc.models.ruleset import READONLY_FIELDS, Ruleset


class RulesetResource(WapiResource[Ruleset]):
    """Manage NIOS ruleset objects."""

    _wapi_type = "ruleset"
    _model = Ruleset
    _default_return_fields = ["name", "comment", "type", "disabled"]
    _readonly_fields = set(READONLY_FIELDS)
