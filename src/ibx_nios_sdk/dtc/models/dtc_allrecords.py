# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""DtcAllrecords - NIOS DTC aggregate read-only record view.

Operations: GET (collection and by ref), PUT (for ttl). Mostly read-only.

``type`` is a Python keyword collision - aliased as ``type_``.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "comment",
        "disable",
        "dtc_server",
        "record",
        "type",
        "type_",
    }
)


class DtcAllrecords(BaseModel):
    """NIOS DTC aggregate record view - mostly read-only.

    ``type`` (Python keyword collision) is exposed as ``type_`` with
    ``Field(alias="type")``.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # --- read-only ---
    comment: str | None = Field(default=None, description="The record comment.")
    disable: bool | None = Field(
        default=None,
        description='The disable value determines if the record is disabled or not. "False" means the record is enabled.',
    )
    dtc_server: str | None = Field(
        default=None,
        description="The name of the DTC Server object with which the record is associated.",
    )
    record: str | None = Field(
        default=None,
        description='The record object, if supported by the WAPI. Otherwise, the value is "None".',
    )  # Python keyword collision: type → type_
    type_: (
        Literal[
            "ALL",
            "dtc:record:a",
            "dtc:record:aaaa",
            "dtc:record:cname",
            "dtc:record:naptr",
            "dtc:record:srv",
        ]
        | str
        | None
    ) = Field(default=None, alias="type", description="Object type discriminator.")

    # --- writable ---
    ttl: int | None = Field(
        default=None,
        description="The TTL value of the record associated with the DTC AllRecords object.",
    )
