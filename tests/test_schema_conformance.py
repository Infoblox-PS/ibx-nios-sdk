# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Typed-model conformance against the WAPI ``?_schema`` snapshot.

For every resource the SDK ships, each readable schema field must (a) exist on the
pydantic model and (b) be annotated with a type that accepts the JSON shape NIOS
puts on the wire (list vs scalar, object vs string, integer vs string). A model
field the schema does not know about is also flagged.

Regenerate the snapshot from a grid with ``tools/refresh_wapi_schema_snapshot.py``.
"""

from __future__ import annotations

import pytest

from tests.wapi_schema import (
    ResourceInfo,
    accepted_kinds,
    expected_kinds,
    iter_resources,
    kinds_satisfied,
    load_snapshot,
    schema_fields,
)

RESOURCES = [r for r in iter_resources() if r.wapi_type in load_snapshot()["objects"]]


def _ids(r: ResourceInfo) -> str:
    return r.wapi_type


def test_snapshot_covers_every_resource() -> None:
    """Every SDK resource type must be a real WAPI object type with a schema in the snapshot."""
    missing = {r.wapi_type for r in iter_resources()} - set(load_snapshot()["objects"])
    assert not missing, f"resources without a schema snapshot: {missing}"


@pytest.mark.parametrize("res", RESOURCES, ids=_ids)
def test_model_fields_match_wire_shape(res: ResourceInfo) -> None:
    by_alias = {(fi.alias or name): fi for name, fi in res.model.model_fields.items()}
    problems: list[str] = []
    for field in schema_fields(res.wapi_type):
        if not field.readable:
            continue
        info = by_alias.get(field.name)
        if info is None:
            problems.append(f"{field.name}: readable in schema but missing from model")
            continue
        expected = expected_kinds(res.wapi_type, field)
        accepted = accepted_kinds(info.annotation)
        if not kinds_satisfied(expected, accepted):
            problems.append(
                f"{field.name}: schema type={list(field.type)} is_array={field.is_array} "
                f"expects {sorted(expected)}; model annotation {info.annotation} "
                f"accepts {sorted(accepted)}"
            )
    assert not problems, f"{res.model.__name__}:\n  " + "\n  ".join(problems)


@pytest.mark.parametrize("res", RESOURCES, ids=_ids)
def test_model_has_no_fields_unknown_to_schema(res: ResourceInfo) -> None:
    schema_names = {f.name for f in schema_fields(res.wapi_type)} | {"_ref"}
    model_names = {fi.alias or name for name, fi in res.model.model_fields.items()}
    unknown = model_names - schema_names
    assert not unknown, f"{res.model.__name__} declares fields WAPI does not: {sorted(unknown)}"
