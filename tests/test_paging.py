# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# tests/test_paging.py
"""AsyncPageIterator: transparent multi-page iteration across WAPI _paging responses."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import BaseModel

from ibx_nios_sdk._paging import AsyncPageIterator


class Item(BaseModel):
    _ref: str = ""
    name: str


def make_fetcher(
    pages: list[tuple[list[dict[str, Any]], str | None]],
) -> tuple[
    Callable[[str | None], Awaitable[tuple[list[dict[str, Any]], str | None]]],
    list[str | None],
]:
    calls: list[str | None] = []
    idx = 0

    async def fetch(page_id: str | None) -> tuple[list[dict[str, Any]], str | None]:
        nonlocal idx
        calls.append(page_id)
        page = pages[idx]
        idx += 1
        return page

    return fetch, calls


async def test_iterate_single_page() -> None:
    fetch, calls = make_fetcher([([{"name": "a"}, {"name": "b"}], None)])
    it = AsyncPageIterator(fetch=fetch, model=Item)
    items = [x async for x in it]
    assert [i.name for i in items] == ["a", "b"]
    assert calls == [None]


async def test_iterate_multi_page() -> None:
    fetch, calls = make_fetcher(
        [
            ([{"name": "a"}], "pg2"),
            ([{"name": "b"}], "pg3"),
            ([{"name": "c"}], None),
        ]
    )
    it = AsyncPageIterator(fetch=fetch, model=Item)
    items = [x async for x in it]
    assert [i.name for i in items] == ["a", "b", "c"]
    assert calls == [None, "pg2", "pg3"]


async def test_all_collects_into_list() -> None:
    fetch, _ = make_fetcher([([{"name": "a"}], "pg2"), ([{"name": "b"}], None)])
    it = AsyncPageIterator(fetch=fetch, model=Item)
    items = await it.all()
    assert [i.name for i in items] == ["a", "b"]


async def test_empty_first_page_terminates() -> None:
    fetch, calls = make_fetcher([([], None)])
    it = AsyncPageIterator(fetch=fetch, model=Item)
    items = [x async for x in it]
    assert items == []
    assert calls == [None]
