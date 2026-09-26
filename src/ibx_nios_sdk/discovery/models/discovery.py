# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Discovery - NIOS discovery object.

Operations: GET (collection and by ref), PUT (update settings).
Also has function endpoints (POST) for various discovery tasks.

NOTE: The function sub-paths (clear_network_port_assignment, etc.) are
represented as ``dict[str, Any] | None`` fields here since they are
function schemas, not stored properties.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset()


class Discovery(BaseModel):
    """NIOS discovery object."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- writable / function descriptors (deeply nested → dict) ---
    clear_network_port_assignment: dict[str, Any] | None = Field(default=None)
    control_switch_port: dict[str, Any] | None = Field(default=None)
    discovery_data_conversion: dict[str, Any] | None = Field(default=None)
    get_device_support_info: dict[str, Any] | None = Field(default=None)
    get_job_devices: dict[str, Any] | None = Field(default=None)
    get_job_process_details: dict[str, Any] | None = Field(default=None)
    import_device_support_bundle: dict[str, Any] | None = Field(default=None)
    modify_sdn_assignment: dict[str, Any] | None = Field(default=None)
    modify_vrf_assignment: dict[str, Any] | None = Field(default=None)
    provision_network_dhcp_relay: dict[str, Any] | None = Field(default=None)
    provision_network_port: dict[str, Any] | None = Field(default=None)
