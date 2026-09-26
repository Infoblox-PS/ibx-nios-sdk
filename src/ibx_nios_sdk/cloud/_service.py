# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""CloudService - entry point for cloud platform resources."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ibx_nios_sdk._http import HttpClient

if TYPE_CHECKING:
    from ibx_nios_sdk.cloud._awsrte53taskgroup import Awsrte53taskgroupResource
    from ibx_nios_sdk.cloud._awsuser import AwsuserResource
    from ibx_nios_sdk.cloud._azurednstaskgroup import AzurednstaskgroupResource
    from ibx_nios_sdk.cloud._azureuser import AzureuserResource
    from ibx_nios_sdk.cloud._gcpdnstaskgroup import GcpdnstaskgroupResource
    from ibx_nios_sdk.cloud._gcpuser import GcpuserResource
    from ibx_nios_sdk.cloud._multiregions import MultiregionsResource


class CloudService:
    """Entry point for NIOS cloud platform resources. Each resource is lazily constructed."""

    def __init__(self, client: HttpClient) -> None:
        """Initialise CloudService with an authenticated HTTP client."""
        self._client = client

    @cached_property
    def awsrte53taskgroup(self) -> Awsrte53taskgroupResource:
        """Entry point for NIOS AWS Route 53 task group resources."""
        from ibx_nios_sdk.cloud._awsrte53taskgroup import Awsrte53taskgroupResource

        return Awsrte53taskgroupResource(self._client)

    @cached_property
    def awsuser(self) -> AwsuserResource:
        """Entry point for NIOS AWS user credential resources."""
        from ibx_nios_sdk.cloud._awsuser import AwsuserResource

        return AwsuserResource(self._client)

    @cached_property
    def azurednstaskgroup(self) -> AzurednstaskgroupResource:
        """Entry point for NIOS Azure DNS task group resources."""
        from ibx_nios_sdk.cloud._azurednstaskgroup import AzurednstaskgroupResource

        return AzurednstaskgroupResource(self._client)

    @cached_property
    def azureuser(self) -> AzureuserResource:
        """Entry point for NIOS Azure user credential resources."""
        from ibx_nios_sdk.cloud._azureuser import AzureuserResource

        return AzureuserResource(self._client)

    @cached_property
    def gcpdnstaskgroup(self) -> GcpdnstaskgroupResource:
        """Entry point for NIOS GCP DNS task group resources."""
        from ibx_nios_sdk.cloud._gcpdnstaskgroup import GcpdnstaskgroupResource

        return GcpdnstaskgroupResource(self._client)

    @cached_property
    def gcpuser(self) -> GcpuserResource:
        """Entry point for NIOS GCP user credential resources."""
        from ibx_nios_sdk.cloud._gcpuser import GcpuserResource

        return GcpuserResource(self._client)

    @cached_property
    def multiregions(self) -> MultiregionsResource:
        """Entry point for NIOS cloud multi-region resources."""
        from ibx_nios_sdk.cloud._multiregions import MultiregionsResource

        return MultiregionsResource(self._client)
