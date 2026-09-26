# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Vdiscoverytask - NIOS virtual discovery task.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).
Also has a function sub-path vdiscovery_control (POST).

NOTE: scheduled_run and vdiscovery_control → dict[str, Any] | None.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "accounts_list",
        "last_run",
        "state",
        "state_msg",
        "uuid",
    }
)


class Vdiscoverytask(BaseModel):
    """NIOS virtual discovery task."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    last_run: int | None = Field(default=None, description="Timestamp of last run.")
    state: (
        Literal[
            "IDLE",
            "READY",
            "RUNNING",
            "COMPLETE",
            "CANCEL_COMPLETE",
            "ERROR",
            "CANCEL_PENDING",
            "WARNING",
        ]
        | str
        | None
    ) = Field(default=None, description="Current state of this task.")
    state_msg: str | None = Field(
        default=None, description="State message of the complete discovery process."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    accounts_list: str | None = Field(
        default=None,
        description="The AWS Account IDs or GCP Project IDs list associated with this task.",
    )
    allow_unsecured_connection: bool | None = Field(
        default=None,
        description="Allow unsecured connection over HTTPS and bypass validation of the remote SSL certificate.",
    )
    auto_consolidate_cloud_ea: bool | None = Field(
        default=None, description="Whether to insert or update cloud EAs with discovery data."
    )
    auto_consolidate_managed_tenant: bool | None = Field(
        default=None, description="Whether to replace managed tenant with discovery tenant data."
    )
    auto_consolidate_managed_vm: bool | None = Field(
        default=None,
        description="Whether to replace managed virtual machine with discovery vm data.",
    )
    auto_create_dns_hostname_template: str | None = Field(
        default=None, description="Template string used to generate host name."
    )
    auto_create_dns_record: bool | None = Field(
        default=None,
        description="Control whether to create or update DNS record using discovered data.",
    )
    auto_create_dns_record_type: Literal["HOST_RECORD", "A_PTR_RECORD"] | str | None = Field(
        default=None,
        description="Indicates the type of record to create if the auto create DNS record is enabled.",
    )
    cdiscovery_file_token: str | None = Field(
        default=None, description="The AWS account IDs or GCP Project IDs file's token."
    )
    comment: str | None = Field(default=None, description="Comment on the task.")
    credentials_type: Literal["DIRECT", "INDIRECT"] | str | None = Field(
        default=None,
        description="Credentials type used for connecting to the cloud management platform.",
    )
    dns_view_private_ip: str | None = Field(
        default=None, description="The DNS view name for private IPs."
    )
    dns_view_public_ip: str | None = Field(
        default=None, description="The DNS view name for public IPs."
    )
    domain_name: str | None = Field(
        default=None, description="The name of the domain to use with keystone v3."
    )
    driver_type: Literal["VMWARE", "AWS", "OPENSTACK", "AZURE", "GCP"] | str | None = Field(
        default=None, description="Type of discovery driver."
    )
    enable_filter: bool | None = Field(
        default=None, description="Enable filter for cloud discovery task"
    )
    enabled: bool | None = Field(
        default=None, description="Whether to enabled the cloud discovery or not."
    )
    fqdn_or_ip: str | None = Field(
        default=None, description="FQDN or IP of the cloud management platform."
    )
    govcloud_enabled: bool | None = Field(
        default=None, description="Indicates if gov cloud is enabled or disabled."
    )
    identity_version: Literal["KEYSTONE_V2", "KEYSTONE_V3"] | str | None = Field(
        default=None, description="Identity service version."
    )
    member: str | None = Field(
        default=None, description="Member on which cloud discovery will be run."
    )
    merge_data: bool | None = Field(
        default=None, description="Whether to replace the old data with new or not."
    )
    multiple_accounts_sync_policy: Literal["DISCOVER", "UPLOAD"] | str | None = Field(
        default=None,
        description="Discover all child accounts or Upload child account ids to discover..",
    )
    name: str | None = Field(
        default=None, description="Name of this cloud discovery task. Uniquely identify a task."
    )
    network_filter: Literal["NONE", "INCLUDE", "EXCLUDE"] | str | None = Field(
        default=None, description="Options to filter the networks in cdiscovery task."
    )
    network_list: list[str] | None = Field(
        default=None, description="List of networks to filter in cdiscovery task."
    )
    password: str | None = Field(
        default=None, description="Password used for connecting to the cloud management platform."
    )
    port: int | None = Field(
        default=None,
        description="Connection port used for connecting to the cloud management platform.",
    )
    private_network_view: str | None = Field(
        default=None, description="Network view for private IPs."
    )
    private_network_view_mapping_policy: Literal["DIRECT", "AUTO_CREATE"] | str | None = Field(
        default=None,
        description="Mapping policy for the network view for private IPs in discovery data.",
    )
    protocol: Literal["HTTP", "HTTPS"] | str | None = Field(
        default=None,
        description="Connection protocol used for connecting to the cloud management platform.",
    )
    public_network_view: str | None = Field(
        default=None, description="Network view for public IPs."
    )
    public_network_view_mapping_policy: Literal["DIRECT", "AUTO_CREATE"] | str | None = Field(
        default=None,
        description="Mapping policy for the network view for public IPs in discovery data.",
    )
    role_arn: str | None = Field(
        default=None, description="Role ARN for syncing child accounts; maximum 128 characters."
    )
    scheduled_run: dict[str, Any] | None = Field(
        default=None, description="Schedule for periodic execution of the task."
    )
    selected_regions: str | None = Field(
        default=None,
        description="String containing selected regions for discovery in comma separated format.",
    )
    service_account_file: str | None = Field(
        default=None, description="The service_account_file for GCP."
    )
    service_account_file_token: str | None = Field(
        default=None, description="Service account file's token."
    )
    sync_child_accounts: bool | None = Field(
        default=None, description="Synchronizing child accounts is enabled or disabled."
    )
    update_dns_view_private_ip: bool | None = Field(
        default=None,
        description="If set to true, the appliance uses a specific DNS view for private IPs.",
    )
    update_dns_view_public_ip: bool | None = Field(
        default=None,
        description="If set to true, the appliance uses a specific DNS view for public IPs.",
    )
    update_metadata: bool | None = Field(
        default=None,
        description="Whether to update metadata as a result of this network discovery.",
    )
    use_identity: bool | None = Field(
        default=None,
        description='If set true, all keystone connection will use "/identity" endpoint and port value will be ignored.',
    )
    username: str | None = Field(
        default=None, description="Username used for connecting to the cloud management platform."
    )
    vdiscovery_control: dict[str, Any] | None = Field(default=None)
