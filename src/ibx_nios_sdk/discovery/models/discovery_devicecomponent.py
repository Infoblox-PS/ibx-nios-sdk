# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DiscoveryDevicecomponent - NIOS discovered device component (read-only).

Operations: GET (collection and by ref) only.

NOTE: ``type`` is a Python keyword collision - aliased as ``type_``.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "component_name",
        "description",
        "device",
        "model",
        "serial",
        "type",
        "type_",
    }
)


class DiscoveryDevicecomponent(BaseModel):
    """NIOS discovered device component - read-only aggregate."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    component_name: str | None = Field(default=None, description="The component name.")
    description: str | None = Field(
        default=None, description="The description of the device component."
    )
    device: str | None = Field(
        default=None, description="A reference to a device, to which this component belongs to."
    )
    model: str | None = Field(default=None, description="The model of the device component.")
    serial: str | None = Field(
        default=None, description="The serial number of the device component."
    )  # Python keyword collision: type → type_
    type_: str | None = Field(default=None, alias="type", description="Object type discriminator.")
