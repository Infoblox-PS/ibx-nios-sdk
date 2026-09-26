# IPAM domain - swagger-vs-reality notes + resource pattern

## Per-object file layout

For each new WAPI object type ``<wapi:type>``:

1. **Model** → ``src/ibx_nios_sdk/ipam/models/<snake_case>.py`` containing:
   - A ``READONLY_FIELDS: frozenset[str]`` of field names the swagger marks
     ``readOnly: true``. These are stripped on PUT.
   - Inline nested-type classes for schemas not reused elsewhere.
   - The main BaseModel class with ``ConfigDict(populate_by_name=True, extra="allow")``.
   - ``ref: str | None = Field(default=None, alias="_ref")``.
   - Every field from the swagger, typed as ``<type> | None = None``.
   - Python keyword collisions use trailing underscore + ``Field(alias="...")``.

2. **Resource** → ``src/ibx_nios_sdk/ipam/_<snake_case>.py``:
   - Subclass ``WapiResource[<Model>]``.
   - ``_wapi_type`` = exact WAPI type string (e.g. ``"network"``).
   - ``_model`` = the pydantic class.
   - ``_default_return_fields`` = 5–10 identity/human-readable fields.
   - ``_readonly_fields`` = ``set(<ModelModule>.READONLY_FIELDS)``.
   - Typed method wrappers ONLY for functions used in >50% of user scripts.
     Others use ``.call_function(ref, ...)``.

3. **Service wiring** → add ``@cached_property`` in ``ipam/_service.py``.

4. **Export** from ``ipam/__init__.py`` and ``ipam/models/__init__.py``.

5. **Tests** → ``tests/ipam/test_<snake_case>.py`` covering:
   - list (with representative filter)
   - get by _ref
   - find_one
   - create (body content + _return_as_object param)
   - update (readonly field strip)
   - delete (returns ref)
   - extattrs round-trip (for objects that support extattrs)
   - one function call (if any typed wrappers added)

## Swagger-vs-reality deltas

Record any places where the NIOS v2.14 WAPI behavior diverges from
`schemas/v2.14/ipam.json`. Each entry should include:

- Object and field affected
- What the swagger claims
- What WAPI actually does
- Workaround in the SDK (e.g. model override, readonly strip, etc.)

_(Populated as issues are discovered during implementation.)_
