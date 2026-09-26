# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# src/ibx_nios_sdk/_paging.py
"""AsyncPageIterator - transparent multi-page async iteration over WAPI list responses."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)

Fetcher = Callable[[str | None], Awaitable[tuple[list[dict[str, Any]], str | None]]]


class AsyncPageIterator(Generic[TModel]):
    """Async iterator yielding parsed model instances from a paged WAPI response.

    Callers pass a ``fetch`` coroutine that takes a ``page_id`` (or ``None``
    for the first page) and returns ``(rows, next_page_id)``. Iteration
    terminates when ``next_page_id`` is ``None`` or ``""``.
    """

    def __init__(self, *, fetch: Fetcher, model: type[TModel]) -> None:
        """Initialize the page iterator.

        Args:
            fetch: Async callable that accepts a ``page_id`` (or ``None`` for
                the first page) and returns a ``(rows, next_page_id)`` tuple.
                ``next_page_id`` should be ``None`` or ``""`` to signal the
                last page.
            model: Pydantic model class used to validate each row dict via
                ``model.model_validate(row)``.
        """
        self._fetch = fetch
        self._model = model

    def __aiter__(self) -> AsyncIterator[TModel]:
        """Return an async iterator that pages through all results.

        Returns:
            An async generator yielding validated model instances one by one
            across all pages.
        """
        return self._iter()

    async def _iter(self) -> AsyncIterator[TModel]:
        page_id: str | None = None
        first = True
        while first or page_id:
            first = False
            rows, page_id = await self._fetch(page_id)
            for row in rows:
                yield self._model.model_validate(row)

    async def all(self) -> list[TModel]:
        """Collect all pages into a single list.

        Exhausts the iterator, fetching every page, and returns the combined
        results. Prefer async iteration (``async for``) for large result sets
        to avoid loading everything into memory at once.

        Returns:
            A list of validated model instances from all pages.

        Example:
            Fetch all records at once::

                iterator = resource.list(name="example")
                records = await iterator.all()
        """
        return [item async for item in self]
