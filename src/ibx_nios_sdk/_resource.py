# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# src/ibx_nios_sdk/_resource.py
"""Base resource class for NIOS WAPI objects."""

from __future__ import annotations

from typing import Any, ClassVar, Generic, TypeVar

from pydantic import BaseModel

from ibx_nios_sdk._exceptions import UnsupportedOperationError
from ibx_nios_sdk._http import HttpClient
from ibx_nios_sdk._paging import AsyncPageIterator
from ibx_nios_sdk._query import build_filter_params, build_return_fields_params
from ibx_nios_sdk._restrictions import restricted_ops

TModel = TypeVar("TModel", bound=BaseModel)

# Module-level alias so annotations inside the class body can reference `list`
# without mypy confusing it with the `WapiResource.list` method.
_StrList = list[str]


class WapiResource(Generic[TModel]):
    """Base class for a single WAPI object type.

    Provides list/get/create/update/delete/call_function operations against a
    NIOS WAPI endpoint. Subclasses must set three class variables:

    - ``_wapi_type``: WAPI object type string, e.g. ``"record:a"``.
    - ``_model``: Pydantic model class used to parse response rows.
    - ``_default_return_fields``: Fields requested by default via
      ``_return_fields+``.

    Optionally set ``_readonly_fields`` to a set of field names that must be
    stripped from PUT payloads on update. Set ``_create_only_fields`` for
    fields that are writable on POST but readonly on PUT (WAPI ``supports``
    flag ``rw`` / ``rws`` - no ``u``). These are kept on ``create()`` and
    stripped on ``update()``.

    Read/create/update/delete are gated on the object type's WAPI restrictions
    (see :mod:`ibx_nios_sdk._restrictions`): an operation NIOS does not support
    raises :class:`~ibx_nios_sdk._exceptions.UnsupportedOperationError` without
    issuing a request. ``_restricted_ops`` is derived per subclass from
    ``_wapi_type``; a subclass may set it explicitly to override the table.
    ``call_function`` is never gated - function-only types such as ``dtc``
    restrict every other operation.
    """

    _wapi_type: ClassVar[str]
    _model: ClassVar[type[BaseModel]]
    _default_return_fields: ClassVar[list[str]]
    _readonly_fields: ClassVar[set[str]] = set()
    _create_only_fields: ClassVar[set[str]] = set()
    _create_exclude: ClassVar[set[str]] = {"ref"}
    _update_exclude: ClassVar[set[str]] = {"ref"}
    _restricted_ops: ClassVar[frozenset[str]] = frozenset()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._create_exclude = {"ref"}
        cls._update_exclude = {"ref"} | cls._readonly_fields | cls._create_only_fields
        if "_restricted_ops" not in cls.__dict__ and "_wapi_type" in cls.__dict__:
            cls._restricted_ops = restricted_ops(cls._wapi_type)

    def __init__(self, client: HttpClient) -> None:
        """Initialize the resource with an HTTP client.

        Args:
            client: The :class:`~ibx_nios_sdk._http.HttpClient` instance used
                to make WAPI requests.
        """
        self._client = client

    def _path(self) -> str:
        """Return the WAPI URL path prefix for this object type.

        Returns:
            A string of the form ``"/<wapi_type>"`` (e.g. ``"/record:a"``).
        """
        return f"/{self._wapi_type}"

    def _validate_ref(self, ref: str) -> None:
        """Assert that a WAPI object reference belongs to this resource type.

        Args:
            ref: WAPI object reference string (e.g.
                ``"record:a/ZG5z...:1.2.3.4/default"``).

        Raises:
            ValueError: If ``ref`` does not start with ``"<wapi_type>/"``.
        """
        prefix = f"{self._wapi_type}/"
        if not ref.startswith(prefix):
            raise ValueError(f"ref {ref!r} does not match wapi_type {self._wapi_type!r}")

    def _require_op(self, operation: str) -> None:
        """Raise if this object type does not support ``operation``.

        Args:
            operation: One of ``read``, ``create``, ``update``, ``delete``.

        Raises:
            UnsupportedOperationError: If WAPI restricts ``operation`` for this
                object type and the client enforces restrictions.
        """
        if operation in self._restricted_ops and self._client.enforce_restrictions:
            raise UnsupportedOperationError(wapi_type=self._wapi_type, operation=operation)

    async def list_page(
        self,
        *,
        page_id: str | None = None,
        max_results: int = 1000,
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
        **filters: Any,
    ) -> tuple[list[TModel], str | None]:
        """Fetch a single page of WAPI results.

        Args:
            page_id: Continuation token from a previous response. Pass ``None``
                to start from the first page.
            max_results: Maximum number of records per page (WAPI
                ``_max_results``).
            return_fields: Exact list of fields to return; mutually exclusive
                with ``return_fields_plus``.
            return_fields_plus: Extra fields to add on top of
                ``_default_return_fields``; mutually exclusive with
                ``return_fields``.
            **filters: Field-level filters using kwarg conventions (e.g.
                ``name="foo"``, ``comment__like="bar"``,
                ``extattr_Site="NYC"``).

        Returns:
            A ``(rows, next_page_id)`` tuple. ``rows`` is a list of validated
            model instances; ``next_page_id`` is the token for the next page, or
            ``None`` if this was the last page.

        Raises:
            ValueError: If both ``return_fields`` and ``return_fields_plus`` are
                provided, or if an unknown filter operator suffix is used.
            UnsupportedOperationError: If WAPI does not support reads of this
                object type.
            NiosError: Or a subclass for WAPI errors.

        Example:
            Fetch the first two pages manually::

                rows, next_id = await resource.list_page(max_results=100)
                if next_id:
                    more, _ = await resource.list_page(page_id=next_id)
        """
        self._require_op("read")
        params: dict[str, str] = {
            "_paging": "1",
            "_return_as_object": "1",
            "_max_results": str(max_results),
        }
        params.update(build_filter_params(filters))
        params.update(
            build_return_fields_params(
                model_fields=self._default_return_fields,
                return_fields=return_fields,
                return_fields_plus=return_fields_plus,
            )
        )
        if page_id:
            params["_page_id"] = page_id

        data = await self._client.get(self._path(), params=params)
        body = data or {}
        rows = body.get("result", []) or []
        next_id = body.get("next_page_id") or None
        parsed = [self._model.model_validate(row) for row in rows]
        return parsed, next_id  # type: ignore[return-value]

    def list(
        self,
        *,
        max_results: int = 1000,
        return_fields: list[str] | None = None,
        return_fields_plus: list[str] | None = None,
        **filters: Any,
    ) -> AsyncPageIterator[TModel]:
        """Return an auto-paginated async iterator over all matching objects.

        Fetches pages on demand as the caller iterates. Use ``await .all()``
        on the returned iterator to collect every record into a list at once.

        Args:
            max_results: Maximum records per page (WAPI ``_max_results``).
            return_fields: Exact list of fields to return; mutually exclusive
                with ``return_fields_plus``.
            return_fields_plus: Extra fields on top of ``_default_return_fields``;
                mutually exclusive with ``return_fields``.
            **filters: Field-level filters (see :func:`build_filter_params`).

        Returns:
            An :class:`~ibx_nios_sdk._paging.AsyncPageIterator` that yields
            validated model instances across all pages.

        Raises:
            UnsupportedOperationError: If WAPI does not support reads of this
                object type. Raised by this call, not by the first iteration.

        Example:
            Iterate lazily::

                async for record in resource.list(name="example"):
                    print(record.ref)

            Collect all at once::

                records = await resource.list(comment__like="prod").all()
        """

        self._require_op("read")

        async def _fetch(page_id: str | None) -> tuple[list[dict[str, Any]], str | None]:
            params: dict[str, str] = {
                "_paging": "1",
                "_return_as_object": "1",
                "_max_results": str(max_results),
            }
            params.update(build_filter_params(filters))
            params.update(
                build_return_fields_params(
                    model_fields=self._default_return_fields,
                    return_fields=return_fields,
                    return_fields_plus=return_fields_plus,
                )
            )
            if page_id:
                params["_page_id"] = page_id
            data = await self._client.get(self._path(), params=params)
            body = data or {}
            return body.get("result", []) or [], body.get("next_page_id") or None

        return AsyncPageIterator(fetch=_fetch, model=self._model)  # type: ignore[arg-type]

    async def find_one(
        self,
        *,
        return_fields: _StrList | None = None,
        return_fields_plus: _StrList | None = None,
        **filters: Any,
    ) -> TModel | None:
        """Return the first matching object, or None if no match is found.

        Requests at most one result (``max_results=1``) to minimise data
        transfer.

        Args:
            return_fields: Exact list of fields to return; mutually exclusive
                with ``return_fields_plus``.
            return_fields_plus: Extra fields on top of ``_default_return_fields``;
                mutually exclusive with ``return_fields``.
            **filters: Field-level filters (see :func:`build_filter_params`).

        Returns:
            The first matching validated model instance, or ``None`` if the
            WAPI returns an empty result set.

        Raises:
            NiosError: Or a subclass for WAPI errors.

        Example:
            Look up a record by name::

                record = await resource.find_one(name="foo.example.com")
                if record is None:
                    print("not found")
        """
        rows, _ = await self.list_page(
            max_results=1,
            return_fields=return_fields,
            return_fields_plus=return_fields_plus,
            **filters,
        )
        return rows[0] if rows else None

    async def get(
        self,
        ref: str,
        *,
        return_fields: _StrList | None = None,
        return_fields_plus: _StrList | None = None,
    ) -> TModel:
        """Fetch a single WAPI object by its ``_ref``.

        Args:
            ref: The WAPI object reference string (e.g.
                ``"record:a/ZG5z...:1.2.3.4/default"``).
            return_fields: Exact list of fields to return; mutually exclusive
                with ``return_fields_plus``.
            return_fields_plus: Extra fields on top of ``_default_return_fields``;
                mutually exclusive with ``return_fields``.

        Returns:
            A validated model instance for the requested object.

        Raises:
            ValueError: If ``ref`` does not belong to this resource type.
            NotFoundError: If the object no longer exists in NIOS.
            UnsupportedOperationError: If WAPI does not support reads of this
                object type.
            NiosError: Or a subclass for other WAPI errors.

        Example:
            Fetch a record by ref::

                record = await resource.get("record:a/ZG5z...:1.2.3.4/default")
                print(record.ipv4addr)
        """
        self._require_op("read")
        self._validate_ref(ref)
        params = build_return_fields_params(
            model_fields=self._default_return_fields,
            return_fields=return_fields,
            return_fields_plus=return_fields_plus,
        )
        data = await self._client.get(f"/{ref}", params=params or None)
        return self._model.model_validate(data or {})  # type: ignore[return-value]

    async def create(
        self,
        obj: BaseModel | dict[str, Any],
        *,
        return_fields: _StrList | None = None,
        return_fields_plus: _StrList | None = None,
    ) -> TModel:
        """Create a new WAPI object and return the populated model.

        Args:
            obj: A Pydantic model instance or plain dict containing the fields
                for the new object. ``None`` values and the ``ref`` field are
                excluded from the POST body automatically.
            return_fields: Exact list of fields to return; mutually exclusive
                with ``return_fields_plus``.
            return_fields_plus: Extra fields on top of ``_default_return_fields``;
                mutually exclusive with ``return_fields``.

        Returns:
            A validated model instance for the newly created object, populated
            with the fields requested via ``_return_as_object=1``.

        Raises:
            UnsupportedOperationError: If WAPI does not support creating this
                object type.
            ConflictError: If the object already exists.
            BadRequestError: If the request body contains invalid fields.
            NiosError: Or a subclass for other WAPI errors.

        Example:
            Create an A record::

                record = await resource.create(
                    {"name": "host.example.com", "ipv4addr": "1.2.3.4"}
                )
                print(record.ref)
        """
        self._require_op("create")
        payload = self._dump(obj, exclude_readonly=False)
        params: dict[str, str] = {"_return_as_object": "1"}
        params.update(
            build_return_fields_params(
                model_fields=self._default_return_fields,
                return_fields=return_fields,
                return_fields_plus=return_fields_plus,
            )
        )
        data = await self._client.post(self._path(), params=params, json=payload)
        if isinstance(data, dict) and list(data) == ["result"]:
            data = data["result"]
        return self._model.model_validate(data or {})  # type: ignore[return-value]

    async def update(
        self,
        ref: str,
        obj: BaseModel | dict[str, Any],
        *,
        return_fields: _StrList | None = None,
        return_fields_plus: _StrList | None = None,
    ) -> TModel:
        """Update an existing WAPI object and return the refreshed model.

        Sends a PUT request with ``_return_as_object=1``. Read-only fields
        listed in ``_readonly_fields`` are stripped from the payload
        automatically.

        Args:
            ref: WAPI object reference string identifying the object to update.
            obj: A Pydantic model instance or plain dict of fields to update.
                ``None`` values, ``ref``, and read-only fields are excluded.
            return_fields: Exact list of fields to return; mutually exclusive
                with ``return_fields_plus``.
            return_fields_plus: Extra fields on top of ``_default_return_fields``;
                mutually exclusive with ``return_fields``.

        Returns:
            A validated model instance reflecting the object's state after the
            update.

        Raises:
            ValueError: If ``ref`` does not belong to this resource type.
            NotFoundError: If the object no longer exists in NIOS.
            UnsupportedOperationError: If WAPI does not support updating this
                object type.
            NiosError: Or a subclass for other WAPI errors.

        Example:
            Change the comment on a host record::

                updated = await resource.update(
                    "record:host/ZG5z...",
                    {"comment": "updated by SDK"},
                )
        """
        self._require_op("update")
        self._validate_ref(ref)
        payload = self._dump(obj, exclude_readonly=True)
        params: dict[str, str] = {"_return_as_object": "1"}
        params.update(
            build_return_fields_params(
                model_fields=self._default_return_fields,
                return_fields=return_fields,
                return_fields_plus=return_fields_plus,
            )
        )
        data = await self._client.put(f"/{ref}", params=params, json=payload)
        if isinstance(data, dict) and list(data) == ["result"]:
            data = data["result"]
        return self._model.model_validate(data or {})  # type: ignore[return-value]

    async def delete(self, ref: str) -> str:
        """Delete a WAPI object by its ``_ref``.

        Args:
            ref: WAPI object reference string identifying the object to delete.

        Returns:
            The ``_ref`` of the deleted object as returned by NIOS, which may
            differ from the input ``ref`` in some WAPI versions. Falls back to
            the input ``ref`` if NIOS does not return a value.

        Raises:
            ValueError: If ``ref`` does not belong to this resource type.
            NotFoundError: If the object does not exist in NIOS.
            UnsupportedOperationError: If WAPI does not support deleting this
                object type.
            NiosError: Or a subclass for other WAPI errors.

        Example:
            Delete an A record::

                deleted_ref = await resource.delete("record:a/ZG5z...:1.2.3.4/default")
        """
        self._require_op("delete")
        self._validate_ref(ref)
        data = await self._client.delete(f"/{ref}")
        if isinstance(data, dict) and "_value" in data:
            return str(data["_value"])
        return ref

    async def call_function(
        self,
        ref: str | None,
        function: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Call a WAPI function on a specific object or on the object type.

        Uses ``POST /<ref>?_function=<name>`` when ``ref`` is provided, or
        ``POST /<wapi_type>?_function=<name>`` for type-level functions.
        ``None`` kwarg values are excluded from the request body.

        Args:
            ref: WAPI object reference, or ``None`` to call a type-level
                function.
            function: WAPI function name (e.g. ``"nextavailableip"``).
            **kwargs: Function arguments passed as the POST body.

        Returns:
            The parsed JSON response body from the function call as a dict
            (empty dict if the WAPI returns no body).

        Raises:
            ValueError: If ``ref`` is provided but does not belong to this
                resource type.
            NiosError: Or a subclass for WAPI errors.

        Example:
            Find the next available IP in a network::

                result = await resource.call_function(
                    "network/ZG5z...",
                    "nextavailableip",
                    num=1,
                )
                print(result["ips"])
        """
        if ref is not None:
            self._validate_ref(ref)
            path = f"/{ref}"
        else:
            path = self._path()
        params = {"_function": function}
        body = {k: v for k, v in kwargs.items() if v is not None}
        data = await self._client.post(path, params=params, json=body or None)
        return data or {}

    async def set_extattrs(self, ref: str, **kwargs: Any) -> TModel:
        """Set extensible attributes on a WAPI object.

        Wraps kwarg key/value pairs into the WAPI ``extattrs`` nested shape
        (``{"<name>": {"value": <val>}}``) and delegates to
        :meth:`update`.

        Args:
            ref: WAPI object reference string identifying the target object.
            **kwargs: Extensible-attribute name/value pairs to set (e.g.
                ``Site="NYC"``, ``Owner="ops-team"``).

        Returns:
            A validated model instance reflecting the object's state after the
            update.

        Raises:
            ValueError: If ``ref`` does not belong to this resource type.
            NiosError: Or a subclass for WAPI errors.

        Example:
            Tag a host record with a site attribute::

                updated = await resource.set_extattrs(
                    "record:host/ZG5z...",
                    Site="NYC",
                    Owner="ops-team",
                )
        """
        extattrs = {name: {"value": value} for name, value in kwargs.items()}
        return await self.update(ref, {"extattrs": extattrs})

    def _dump(self, obj: BaseModel | dict[str, Any], *, exclude_readonly: bool) -> dict[str, Any]:
        """Serialise a model or dict into a WAPI-compatible request body.

        For Pydantic models, uses ``model_dump(by_alias=True, exclude_none=True)``
        and always strips ``ref``. When ``exclude_readonly`` is True, also
        removes fields listed in ``_readonly_fields``.  For plain dicts, simply
        drops ``None`` values (the caller is responsible for the correct shape).

        Args:
            obj: A Pydantic model instance or plain dict to serialise.
            exclude_readonly: When True, strip read-only fields from the
                serialised output (used for PUT/update payloads).

        Returns:
            A dict ready to send as the JSON body of a WAPI request.
        """
        if isinstance(obj, BaseModel):
            exclude = self._update_exclude if exclude_readonly else self._create_exclude
            return obj.model_dump(by_alias=True, exclude_none=True, exclude=exclude)
        # dict passthrough - caller is responsible for shape.
        return {k: v for k, v in obj.items() if v is not None}
