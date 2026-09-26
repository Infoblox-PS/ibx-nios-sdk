# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""GridServicerestartRequestChangedobject - NIOS Grid service-restart changed object."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "action",
        "changed_properties",
        "changed_time",
        "object_name",
        "object_type",
        "user_name",
        "uuid",
    }
)


class GridServicerestartRequestChangedobject(BaseModel):
    """NIOS Grid service-restart changed object."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    # read-only
    action: (
        Literal[
            "DELETED",
            "CREATED",
            "MODIFIED",
            "CALLED",
            "MESSAGE",
            "LOGIN_ALLOWED",
            "LOGIN_DENIED",
            "LOGOUT",
        ]
        | str
        | None
    ) = Field(default=None, description="The operation on the changed object.")
    changed_properties: list[str] | None = Field(
        default=None, description="The list of changed properties in the object."
    )
    changed_time: int | None = Field(
        default=None, description="The time when the object was changed."
    )
    object_name: str | None = Field(default=None, description="The name of the changed object.")
    object_type: str | None = Field(
        default=None,
        description="The type of the changed object. This is undefined if the object is not supported.",
    )
    user_name: str | None = Field(
        default=None, description="The name of the user who changed the object properties."
    )
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
