# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2026 Infoblox, Inc.
# src/ibx_nios_sdk/_query.py
"""Translate Python kwargs into WAPI query parameters.

WAPI operator conventions:
  field=value       -> exact match
  field~=value      -> regex/substring match   (kwarg: field__like)
  field<=value      -> less than or equal       (kwarg: field__lte)
  field>=value      -> greater than or equal    (kwarg: field__gte)
  field!=value      -> not equal                (kwarg: field__not)
  *EA_name=value    -> extensible-attr filter   (kwarg: extattr_EA_name)
"""

from __future__ import annotations

from typing import Any

_OPERATOR_SUFFIX_MAP: dict[str, str] = {
    "like": "~",
    "gte": ">",
    "lte": "<",
    "not": "!",
}


def _stringify(value: Any) -> str:
    """Convert a Python value to a WAPI-compatible query-parameter string.

    Booleans are lowercased (``True`` → ``"true"``), all other types use
    ``str()``.

    Args:
        value: The Python value to convert.

    Returns:
        A string representation suitable for use as a WAPI query-param value.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build_filter_params(filters: dict[str, Any]) -> dict[str, str]:
    """Translate kwarg-style filters into WAPI query-param key/value pairs.

    Keys with a ``__<op>`` suffix map to the corresponding WAPI operator
    (``like`` → ``~``, ``gte`` → ``>``, ``lte`` → ``<``, ``not`` → ``!``).
    Keys prefixed with ``extattr_`` are mapped to ``*<EA_name>`` for
    extensible-attribute filtering. ``None`` values are silently dropped.

    Args:
        filters: Dict of filter kwargs, typically the ``**filters`` captured
            by a resource method (e.g. ``{"name": "foo", "age__gte": 5}``).

    Returns:
        A dict of WAPI query-parameter name/value pairs ready to pass as
        ``params`` to an HTTP request.

    Raises:
        ValueError: If an unknown ``__<op>`` suffix is encountered.

    Example:
        Build filters for a WAPI list request::

            params = build_filter_params({"name": "foo", "comment__like": "bar"})
            # {"name": "foo", "comment~": "bar"}
    """
    out: dict[str, str] = {}
    for key, value in filters.items():
        if value is None:
            continue

        if key.startswith("extattr_"):
            ea_name = key[len("extattr_") :]
            out[f"*{ea_name}"] = _stringify(value)
            continue

        if "__" in key:
            field, _, suffix = key.rpartition("__")
            op = _OPERATOR_SUFFIX_MAP.get(suffix)
            if op is None:
                raise ValueError(f"unknown filter operator: {suffix!r} in kwarg {key!r}")
            out[f"{field}{op}"] = _stringify(value)
            continue

        out[key] = _stringify(value)

    return out


def build_return_fields_params(
    *,
    model_fields: list[str],
    return_fields: list[str] | None,
    return_fields_plus: list[str] | None,
) -> dict[str, str]:
    """Build the ``_return_fields`` / ``_return_fields+`` query params.

    Selection rules:

    - Both ``None`` → ``_return_fields+=<model_fields>`` so the full model
      can be populated from the response.
    - ``return_fields=[..]`` → ``_return_fields=<exact list>`` (caller
      controls exactly which fields are returned).
    - ``return_fields_plus=[..]`` → ``_return_fields+=<model_fields + extras>``
      (model fields plus caller-specified extras).
    - Passing both → ``ValueError``.

    Args:
        model_fields: Fields declared on the SDK model used as the default set.
        return_fields: Explicit list of fields; mutually exclusive with
            ``return_fields_plus``.
        return_fields_plus: Extra fields to append to ``model_fields``; mutually
            exclusive with ``return_fields``.

    Returns:
        A dict containing either ``_return_fields`` or ``_return_fields+``, or
        an empty dict when ``model_fields`` is empty and both optional args are
        ``None``.

    Raises:
        ValueError: If both ``return_fields`` and ``return_fields_plus`` are
            non-None.

    Example:
        Request only specific fields::

            params = build_return_fields_params(
                model_fields=["name", "comment"],
                return_fields=["name"],
                return_fields_plus=None,
            )
            # {"_return_fields": "name"}
    """
    if return_fields is not None and return_fields_plus is not None:
        raise ValueError("cannot pass both return_fields and return_fields_plus")

    if return_fields is not None:
        return {"_return_fields": ",".join(return_fields)}

    combined = list(model_fields)
    if return_fields_plus:
        combined.extend(return_fields_plus)
    if not combined:
        return {}
    return {"_return_fields+": ",".join(combined)}
