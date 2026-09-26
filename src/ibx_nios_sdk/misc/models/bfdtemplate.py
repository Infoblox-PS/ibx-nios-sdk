# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Bfdtemplate - NIOS BFD template object.

Operations: GET collection, POST, GET by ref, PUT, DELETE (full CRUD).

WAPI type: bfdtemplate

NOTES:
- 'uuid' is read-only.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "uuid",
    }
)


class Bfdtemplate(BaseModel):
    """NIOS BFD template."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )  # --- writable ---
    detection_multiplier: int | None = Field(
        default=None,
        description="The detection time multiplier value for BFD protocol. The negotiated transmit interval, multiplied by this value, provides the detection time for the receiving system in asynchronous BFD mode. Valid values are between 3 and 50.",
    )
    min_rx_interval: int | None = Field(
        default=None,
        description="The minimum receive time (in seconds) for BFD protocol. Valid values are between 50 and 9999. From NIOS 9.1.0 onwards, the BFD default value has been changed from 100 to 300.",
    )
    min_tx_interval: int | None = Field(
        default=None,
        description="The minimum transmission time (in seconds) for BFD protocol. Valid values are between 50 and 9999. From NIOS 9.1.0 onwards, the BFD default value has been changed from 100 to 300.",
    )
    name: str | None = Field(default=None, description="The name of the BFD template object.")
