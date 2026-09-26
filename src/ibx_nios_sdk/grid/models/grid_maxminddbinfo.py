# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridMaxminddbinfo - NIOS Grid MaxMind DB info (read-only)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "binary_major_version",
        "binary_minor_version",
        "build_time",
        "database_type",
        "deployment_time",
        "member",
        "topology_type",
        "uuid",
    }
)


class GridMaxminddbinfo(BaseModel):
    """NIOS Grid MaxMind DB info (read-only)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    binary_major_version: int | None = Field(
        default=None, description="The major version of DB binary format."
    )  # read-only
    binary_minor_version: int | None = Field(
        default=None, description="The minor version of DB binary format."
    )  # read-only
    build_time: int | None = Field(
        default=None, description="The time at which the DB was built."
    )  # read-only
    database_type: str | None = Field(
        default=None,
        description='The structure of data records ("GeoLite2-Country", GeoLite2-City", etc.).',
    )  # read-only
    deployment_time: int | None = Field(
        default=None, description="The time at which the current Topology DB was deployed."
    )  # read-only
    member: str | None = Field(
        default=None, description="The member for testing the connection."
    )  # read-only
    topology_type: Literal["GEOIP", "EA"] | str | None = Field(
        default=None, description="The topology type."
    )  # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
