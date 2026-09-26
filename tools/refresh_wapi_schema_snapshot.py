#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
"""Regenerate ``tests/fixtures/wapi_schema_v2.14.json`` from a live NIOS grid.

Reads ``NIOS_GRID_URL``, ``NIOS_USERNAME``, ``NIOS_PASSWORD`` (and optionally
``NIOS_WAPI_VERSION``, ``NIOS_VERIFY=0``) and dumps the compact
``?_schema&_schema_version=2`` shape of every object type the SDK exposes.

    NIOS_GRID_URL=https://grid NIOS_USERNAME=admin NIOS_PASSWORD=... \\
        python tools/refresh_wapi_schema_snapshot.py [--nios-version 9.1.0-54969]

Run ``pytest tests/test_schema_conformance.py`` afterwards: any model whose field
types disagree with the refreshed schema fails there.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ibx_nios_sdk import NiosClient  # noqa: E402
from ibx_nios_sdk._exceptions import NiosError  # noqa: E402
from tests.wapi_schema import SNAPSHOT, iter_resources  # noqa: E402


def _compact(schema: dict[str, Any]) -> dict[str, Any]:
    fields = []
    for f in schema["fields"]:
        entry: dict[str, Any] = {
            "name": f["name"],
            "type": f["type"],
            "is_array": f["is_array"],
            "supports": f["supports"],
        }
        if f.get("wapi_primitive") == "funccall":
            entry["primitive"] = "funccall"
        elif "schema" in f or f.get("wapi_primitive") == "struct":
            entry["primitive"] = "struct"
        fields.append(entry)
    compact: dict[str, Any] = {"fields": fields}
    # Operations NIOS refuses on this object type (create/update/delete gate the
    # SDK's resource methods; csv/scheduling/etc. are kept for reference).
    if schema.get("restrictions"):
        compact["restrictions"] = sorted(schema["restrictions"])
    return compact


def _unwrap(value: Any) -> Any:
    return value["_value"] if isinstance(value, dict) and "_value" in value else value


async def main(nios_version: str, out: Path) -> int:
    client = NiosClient(
        grid_url=os.environ["NIOS_GRID_URL"],
        username=os.environ["NIOS_USERNAME"],
        password=os.environ["NIOS_PASSWORD"],
        wapi_version=os.environ.get("NIOS_WAPI_VERSION", "2.14"),
        verify=os.environ.get("NIOS_VERIFY", "1") not in ("0", "false", "no"),
    )
    params = {"_schema": "1", "_schema_version": "2"}
    objects: dict[str, Any] = {}
    failures: list[str] = []
    async with client:
        root = _unwrap(await client._http.get("/", params=params))
        for res in iter_resources():
            try:
                objects[res.wapi_type] = _compact(
                    _unwrap(await client._http.get(res.wapi_type, params=params))
                )
            except NiosError as exc:
                failures.append(f"{res.wapi_type}: {exc}")
    header = {
        "_comment": (
            "Compact snapshot of WAPI ?_schema&_schema_version=2 for every SDK object type. "
            "Regenerate with: python tools/refresh_wapi_schema_snapshot.py"
        ),
        "wapi_version": root["requested_version"],
        "schema_version": root["schema_version"],
        "nios_version": nios_version,
        "supported_objects": root["supported_objects"],
    }
    lines = [f"{json.dumps(k)}: {json.dumps(v)}" for k, v in header.items()]
    body = ",\n".join(
        f"  {json.dumps(t)}: {json.dumps(objects[t], separators=(',', ':'))}"
        for t in sorted(objects)
    )
    out.write_text("{\n" + ",\n".join(lines) + ',\n"objects": {\n' + body + "\n}\n}\n")
    print(f"wrote {len(objects)} object schemas to {out}")
    for line in failures:
        print("skipped", line, file=sys.stderr)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--nios-version", default="unknown", help="recorded in the snapshot header"
    )
    parser.add_argument("--out", type=Path, default=SNAPSHOT)
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.nios_version, args.out)))
