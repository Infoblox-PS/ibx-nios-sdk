# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Helpers for checking typed models against the WAPI ``?_schema`` snapshot.

The snapshot (``tests/fixtures/wapi_schema_v2.14.json``) is a compact dump of
``GET /wapi/v2.14/<object>?_schema&_schema_version=2`` for every object type the
SDK exposes. Field shapes on the wire follow these rules:

* ``is_array`` -> JSON list
* ``primitive == "struct"`` -> JSON object
* ``type`` is a scalar (string/enum/uint/int/bool/timestamp/float/extattr)
  -> the matching JSON scalar (timestamps are epoch integers; extattr is an object)
* ``type`` names another WAPI object -> a ``_ref`` string, or an inline object for
  child objects whose type name extends the parent's (``record:host`` ->
  ``record:host_ipv4addr``); a self-reference may be either
* ``primitive == "funccall"`` -> not a data field; never returned by ``list``
"""

from __future__ import annotations

import importlib
import inspect
import json
import pkgutil
import types
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any, Literal, Union, get_args, get_origin

from pydantic import BaseModel

import ibx_nios_sdk
from ibx_nios_sdk._resource import WapiResource

SNAPSHOT = Path(__file__).parent / "fixtures" / "wapi_schema_v2.14.json"

SCALAR_KINDS: dict[str, str] = {
    "string": "str",
    "enum": "str",
    "date": "str",
    "uint": "int",
    "int": "int",
    "timestamp": "int",
    "bool": "bool",
    "float": "float",
    "extattr": "dict",
}

# Fields where NIOS 9.1 sends a different shape than its own ``?_schema`` declares.
# Each entry was confirmed against a live grid; the model must accept the wire shape.
WIRE_OVERRIDES: dict[tuple[str, str], frozenset[str]] = {
    ("grid", "restart_status"): frozenset({"dict"}),  # schema: string; wire: restartstatus struct
    ("grid:servicerestart:group", "status"): frozenset({"dict"}),  # schema: string; wire: object
    ("member:dhcpproperties", "failover_association_utilization"): frozenset({"float"}),  # uint
    ("dtc:object", "object"): frozenset(
        {"dict"}
    ),  # schema: string; wire: inline dtc:server object
    ("record:dtclbdn", "lbdn"): frozenset(
        {"dict"}
    ),  # schema: string; wire: inline dtc:lbdn object
}


@dataclass(frozen=True)
class SchemaField:
    name: str
    type: tuple[str, ...]
    is_array: bool
    supports: str
    primitive: str | None

    @property
    def readable(self) -> bool:
        return "r" in self.supports and self.primitive != "funccall"


@dataclass(frozen=True)
class ResourceInfo:
    wapi_type: str
    resource: type[WapiResource[Any]]
    model: type[BaseModel]


@cache
def load_snapshot() -> dict[str, Any]:
    with SNAPSHOT.open() as fh:
        data: dict[str, Any] = json.load(fh)
    return data


@cache
def schema_fields(wapi_type: str) -> tuple[SchemaField, ...]:
    obj = load_snapshot()["objects"].get(wapi_type)
    if obj is None:
        return ()
    return tuple(
        SchemaField(
            name=f["name"],
            type=tuple(f["type"]),
            is_array=f["is_array"],
            supports=f["supports"],
            primitive=f.get("primitive"),
        )
        for f in obj["fields"]
    )


def readable_field_names(wapi_type: str) -> list[str]:
    """Every field ``list()`` may legitimately request for this object type."""
    return [f.name for f in schema_fields(wapi_type) if f.readable]


@cache
def iter_resources() -> tuple[ResourceInfo, ...]:
    """Discover every concrete ``WapiResource`` subclass shipped in the SDK."""
    found: list[ResourceInfo] = []
    for mod_info in pkgutil.walk_packages(ibx_nios_sdk.__path__, "ibx_nios_sdk."):
        if ".models" in mod_info.name or ".bin" in mod_info.name:
            continue
        module = importlib.import_module(mod_info.name)
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(cls, WapiResource)
                and cls is not WapiResource
                and cls.__module__ == mod_info.name
            ):
                found.append(ResourceInfo(cls._wapi_type, cls, cls._model))
    return tuple(sorted(found, key=lambda r: r.wapi_type))


# --------------------------------------------------------------------------
# Wire-shape reasoning
# --------------------------------------------------------------------------


def _object_kinds(parent_type: str, element_type: str) -> set[str]:
    """Wire kinds for a field typed as another WAPI object.

    Child objects whose type name extends the parent's (``record:host`` ->
    ``record:host_ipv4addr``) are returned inline; a self-reference
    (``scheduledtask.dependent_tasks``) may be either; anything else is a ``_ref``.
    """
    if element_type == parent_type:
        return {"str", "dict"}
    if element_type.startswith(parent_type):
        return {"dict"}
    return {"str"}


def expected_kinds(parent_type: str, field: SchemaField) -> frozenset[str]:
    """JSON kinds the wire can carry for ``field``: ``list``, ``list:<k>``, or a scalar kind.

    For object-typed fields the result contains both ``str`` and ``dict`` when the
    referenced type is a child of the parent (inline object), else just ``str``.
    """
    override = WIRE_OVERRIDES.get((parent_type, field.name))
    if override is not None:
        return override
    if field.is_array:
        inner = expected_kinds(
            parent_type,
            SchemaField(field.name, field.type, False, field.supports, field.primitive),
        )
        return frozenset({"list"} | {f"list:{k}" for k in inner})
    if field.primitive == "struct":
        return frozenset({"dict"})
    kinds: set[str] = set()
    for t in field.type:
        if t in SCALAR_KINDS:
            kinds.add(SCALAR_KINDS[t])
        else:
            kinds |= _object_kinds(parent_type, t)
    return frozenset(kinds)


def accepted_kinds(annotation: Any) -> frozenset[str]:
    """JSON kinds a pydantic field annotation will validate without error."""
    origin = get_origin(annotation)
    if annotation is Any or annotation is object:
        return frozenset({"any"})
    if origin in (Union, types.UnionType):
        out: set[str] = set()
        for arg in get_args(annotation):
            out |= accepted_kinds(arg)
        return frozenset(out)
    if origin is Literal:
        return frozenset({"str"})
    if origin in (list, tuple, set) or annotation in (list, tuple, set):
        args = get_args(annotation)
        inner = accepted_kinds(args[0]) if args else frozenset({"any"})
        return frozenset({"list"} | {f"list:{k}" for k in inner})
    if origin is dict or annotation is dict:
        return frozenset({"dict"})
    if annotation is type(None):
        return frozenset()
    if annotation is str:
        return frozenset({"str"})
    if annotation is bool:
        return frozenset({"bool"})
    if annotation is int:
        return frozenset({"int"})
    if annotation is float:
        return frozenset({"float", "int"})
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return frozenset({"dict"})
    return frozenset({f"?{annotation!r}"})


def kinds_satisfied(expected: frozenset[str], accepted: frozenset[str]) -> bool:
    if "any" in accepted:
        return True
    if "list:any" in accepted:
        accepted = accepted | {k for k in expected if k.startswith("list:")}
    return expected <= accepted


# --------------------------------------------------------------------------
# Synthetic wire rows
# --------------------------------------------------------------------------


def synthesize_value(parent_type: str, field: SchemaField) -> Any:
    """Build a representative JSON value for ``field`` following the wire rules."""
    kinds = expected_kinds(parent_type, field)
    if "list" in kinds:
        inner = SchemaField(field.name, field.type, False, field.supports, field.primitive)
        return [synthesize_value(parent_type, inner)]
    if "dict" in kinds:
        if field.type == ("extattr",):
            return {"Site": {"value": "HQ"}}
        return {"_struct": field.type[0], "name": "x"}
    if "bool" in kinds:
        return True
    if "float" in kinds:
        return 1.5
    if "int" in kinds:
        return 1
    return "x"


def synthesize_row(wapi_type: str) -> dict[str, Any]:
    """A full wire row for ``wapi_type`` with every readable field populated."""
    row: dict[str, Any] = {"_ref": f"{wapi_type}/ZG5z:synthetic"}
    for field in schema_fields(wapi_type):
        if field.readable:
            row[field.name] = synthesize_value(wapi_type, field)
    return row
