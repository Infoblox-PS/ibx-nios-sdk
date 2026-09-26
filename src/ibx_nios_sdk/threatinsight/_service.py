# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatinsightService - entry point for threat insight resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.threatinsight._allowlist import ThreatinsightAllowlistResource
    from ibx_nios_sdk.threatinsight._cloudclient import ThreatinsightCloudclientResource
    from ibx_nios_sdk.threatinsight._insight_allowlist import ThreatinsightInsightAllowlistResource
    from ibx_nios_sdk.threatinsight._moduleset import ThreatinsightModulesetResource


class ThreatinsightService:
    """Entry point for NIOS threat insight resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise ThreatinsightService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def allowlist(self) -> ThreatinsightAllowlistResource:
        """Entry point for NIOS Threat Insight allowlist resources."""
        from ibx_nios_sdk.threatinsight._allowlist import ThreatinsightAllowlistResource

        return ThreatinsightAllowlistResource(self._client)

    @cached_property
    def cloudclient(self) -> ThreatinsightCloudclientResource:
        """Entry point for NIOS Threat Insight cloud client resources."""
        from ibx_nios_sdk.threatinsight._cloudclient import ThreatinsightCloudclientResource

        return ThreatinsightCloudclientResource(self._client)

    @cached_property
    def insight_allowlist(self) -> ThreatinsightInsightAllowlistResource:
        """Entry point for NIOS Threat Insight per-insight allowlist resources."""
        from ibx_nios_sdk.threatinsight._insight_allowlist import (
            ThreatinsightInsightAllowlistResource,
        )

        return ThreatinsightInsightAllowlistResource(self._client)

    @cached_property
    def moduleset(self) -> ThreatinsightModulesetResource:
        """Entry point for NIOS Threat Insight module set resources."""
        from ibx_nios_sdk.threatinsight._moduleset import ThreatinsightModulesetResource

        return ThreatinsightModulesetResource(self._client)
