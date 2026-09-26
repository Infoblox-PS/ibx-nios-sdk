# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""ThreatprotectionService - entry point for threat protection resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.threatprotection._grid_rule import ThreatprotectionGridRuleResource
    from ibx_nios_sdk.threatprotection._profile import ThreatprotectionProfileResource
    from ibx_nios_sdk.threatprotection._profile_rule import ThreatprotectionProfileRuleResource
    from ibx_nios_sdk.threatprotection._rule import ThreatprotectionRuleResource
    from ibx_nios_sdk.threatprotection._rulecategory import ThreatprotectionRulecategoryResource
    from ibx_nios_sdk.threatprotection._ruleset import ThreatprotectionRulesetResource
    from ibx_nios_sdk.threatprotection._ruletemplate import ThreatprotectionRuletemplateResource
    from ibx_nios_sdk.threatprotection._statistics import ThreatprotectionStatisticsResource


class ThreatprotectionService:
    """Entry point for NIOS threat protection resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise ThreatprotectionService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def grid_rule(self) -> ThreatprotectionGridRuleResource:
        """Entry point for NIOS Threat Protection Grid-level rule resources."""
        from ibx_nios_sdk.threatprotection._grid_rule import ThreatprotectionGridRuleResource

        return ThreatprotectionGridRuleResource(self._client)

    @cached_property
    def profile(self) -> ThreatprotectionProfileResource:
        """Entry point for NIOS Threat Protection profile resources."""
        from ibx_nios_sdk.threatprotection._profile import ThreatprotectionProfileResource

        return ThreatprotectionProfileResource(self._client)

    @cached_property
    def profile_rule(self) -> ThreatprotectionProfileRuleResource:
        """Entry point for NIOS Threat Protection profile rule resources."""
        from ibx_nios_sdk.threatprotection._profile_rule import ThreatprotectionProfileRuleResource

        return ThreatprotectionProfileRuleResource(self._client)

    @cached_property
    def rule(self) -> ThreatprotectionRuleResource:
        """Entry point for NIOS Threat Protection rule resources."""
        from ibx_nios_sdk.threatprotection._rule import ThreatprotectionRuleResource

        return ThreatprotectionRuleResource(self._client)

    @cached_property
    def rulecategory(self) -> ThreatprotectionRulecategoryResource:
        """Entry point for NIOS Threat Protection rule category resources."""
        from ibx_nios_sdk.threatprotection._rulecategory import (
            ThreatprotectionRulecategoryResource,
        )

        return ThreatprotectionRulecategoryResource(self._client)

    @cached_property
    def ruleset(self) -> ThreatprotectionRulesetResource:
        """Entry point for NIOS Threat Protection rule set resources."""
        from ibx_nios_sdk.threatprotection._ruleset import ThreatprotectionRulesetResource

        return ThreatprotectionRulesetResource(self._client)

    @cached_property
    def ruletemplate(self) -> ThreatprotectionRuletemplateResource:
        """Entry point for NIOS Threat Protection rule template resources."""
        from ibx_nios_sdk.threatprotection._ruletemplate import (
            ThreatprotectionRuletemplateResource,
        )

        return ThreatprotectionRuletemplateResource(self._client)

    @cached_property
    def statistics(self) -> ThreatprotectionStatisticsResource:
        """Entry point for NIOS Threat Protection statistics resources."""
        from ibx_nios_sdk.threatprotection._statistics import ThreatprotectionStatisticsResource

        return ThreatprotectionStatisticsResource(self._client)
