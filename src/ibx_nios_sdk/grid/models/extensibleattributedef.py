# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Extensibleattributedef - NIOS extensible attribute definition."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

READONLY_FIELDS: frozenset[str] = frozenset(
    {
        "namespace",
        "uuid",
    }
)


class Extensibleattributedef(BaseModel):
    """NIOS extensible attribute definition."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    ref: str | None = Field(default=None, alias="_ref", description="The reference to the object.")

    allowed_object_types: list[str] | None = Field(
        default=None,
        description="The object types this extensible attribute is allowed to associate with.",
    )
    comment: str | None = Field(
        default=None,
        description="Comment for the Extensible Attribute Definition; maximum 256 characters.",
    )
    default_value: str | None = Field(
        default=None,
        description="Default value used to pre-populate the attribute value in the GUI. For email, URL, and string types, the value is a string with a maximum of 256 characters. For an integer, the value is an integer from -2147483648 through 2147483647. For a date, the value is the number of seconds that have elapsed since January 1st, 1970 UTC.",
    )
    descendants_action: dict[str, object] | None = Field(
        default=None, description="Action to apply to descendant objects when this object changes."
    )
    flags: str | None = Field(
        default=None,
        description="This field contains extensible attribute flags. Possible values: (A)udited, (C)loud API, Cloud (G)master, (I)nheritable, (L)isted, (M)andatory value, MGM (P)rivate, (R)ead Only, (S)ort enum values, Multiple (V)alues If there are two or more flags in the field, you must list them according to the order they are listed above. For example, 'CR' is a valid value for the 'flags' field because C = Cloud API is listed before R = Read only. However, the value 'RC' is invalid because the order for the 'flags' field is broken.",
    )
    list_values: list[dict[str, object]] | None = Field(
        default=None,
        description="List of Values. Applicable if the extensible attribute type is ENUM.",
    )
    max: int | None = Field(
        default=None,
        description="Maximum allowed value of extensible attribute. Applicable if the extensible attribute type is INTEGER.",
    )
    min: int | None = Field(
        default=None,
        description="Minimum allowed value of extensible attribute. Applicable if the extensible attribute type is INTEGER.",
    )
    name: str | None = Field(
        default=None, description="The name of the Extensible Attribute Definition."
    )  # read-only
    namespace: Literal["CLOUD", "CLOUD_GM", "MSADSITES", "RIPE", "default"] | str | None = Field(
        default=None, description="Namespace for the Extensible Attribute Definition."
    )  # "type" is a Python builtin - use alias
    type_: Literal["STRING", "INTEGER", "EMAIL", "DATE", "ENUM", "URL"] | str | None = Field(
        default=None, alias="type", description="Object type discriminator."
    )

    # read-only
    uuid: str | None = Field(
        default=None, description="Universally Unique ID assigned for this object"
    )
