# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Discoverytask - NIOS IPAM discovery task object.

All 24 properties from ``components.schemas.Discoverytask`` in the v2.14
IPAM swagger are represented here.

NOTE: _wapi_type is ``discovery:discoverytask`` (colon in type string).
The snake accessor on IpamService is ``discovery_discoverytask``.

NOTE: The following complex nested schemas are inlined as dicts:
  - DiscoverytaskNetworkDiscoveryControl
  - DiscoverytaskScheduledRun
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Read-only fields (swagger readOnly: true)
# ---------------------------------------------------------------------------
READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "csv_file_name",
        "discovery_task_oid",
        "state",
        "state_time",
        "status",
        "status_time",
        "uuid",
        "warning",
    }
)


# ---------------------------------------------------------------------------
# Main Discoverytask model
# ---------------------------------------------------------------------------


class Discoverytask(BaseModel):
    """NIOS IPAM discovery task object.

    All 24 swagger properties are present. Read-only fields are collected in
    :data:`READONLY_FIELDS`; the resource strips them before PUT/POST.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    csv_file_name: str | None = Field(
        default=None, description="The network discovery CSV file name."
    )  # --- scanning options ---
    disable_ip_scanning: bool | None = Field(
        default=None, description="Determines whether IP scanning is disabled."
    )
    disable_vmware_scanning: bool | None = Field(
        default=None, description="Determines whether VMWare scanning is disabled."
    )  # --- read-only ---
    discovery_task_oid: str | None = Field(
        default=None, description="The discovery task identifier."
    )  # --- identity ---
    member_name: str | None = Field(
        default=None, description="The Grid member that runs the discovery."
    )  # --- merge ---
    merge_data: bool | None = Field(
        default=None,
        description="Determines whether to replace or merge new data with existing data.",
    )  # --- mode ---
    mode: Literal["FULL", "ICMP", "NETBIOS", "TCP", "CSV"] | str | None = Field(
        default=None, description="Network discovery scanning mode."
    )  # --- network discovery control (complex nested - dict) ---
    network_discovery_control: dict[str, Any] | None = Field(default=None)  # --- scope ---
    network_view: str | None = Field(
        default=None,
        description="Name of the network view in which target networks for network discovery reside.",
    )
    networks: list[str] | None = Field(
        default=None,
        description="The list of the networks on which the network discovery will be invoked.",
    )  # --- ping settings ---
    ping_retries: int | None = Field(
        default=None, description="The number of times to perform ping for ICMP and FULL modes."
    )
    ping_timeout: int | None = Field(
        default=None, description="The ping timeout for ICMP and FULL modes."
    )  # --- schedule (complex nested - dict) ---
    scheduled_run: dict[str, Any] | None = Field(
        default=None, description="Schedule for periodic execution of the task."
    )  # --- read-only ---
    state: (
        Literal["RUNNING", "PAUSED", "COMPLETE", "ERROR", "PAUSE_PENDING", "END_PENDING"]
        | str
        | None
    ) = Field(default=None, description="The network discovery process state.")
    state_time: int | None = Field(
        default=None, description="Time when the network discovery process state was last updated."
    )
    status: str | None = Field(
        default=None, description="The network discovery process descriptive status."
    )
    status_time: int | None = Field(
        default=None,
        description="The time when the network discovery process status was last updated.",
    )  # --- TCP scanning ---
    tcp_ports: list[dict[str, Any]] | None = Field(
        default=None, description="The ports to scan for FULL and TCP modes."
    )
    tcp_scan_technique: Literal["SYN", "CONNECT"] | str | None = Field(
        default=None, description="The TCP scan technique for FULL and TCP modes."
    )  # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- VMware ---
    v_network_view: str | None = Field(
        default=None,
        description="Name of the network view in which target networks for VMWare scanning reside.",
    )
    vservers: list[dict[str, Any]] | None = Field(
        default=None, description="The list of VMware vSphere servers for VM discovery."
    )  # --- read-only ---
    warning: str | None = Field(default=None, description="The network discovery process warning.")
