# RPZ domain - swagger-vs-reality notes + resource pattern

## Per-object file layout

For each new WAPI object type `<wapi:type>`:

1. **Model** → `src/ibx_nios_sdk/rpz/models/<snake_case>.py` containing:
   - A `READONLY_FIELDS: frozenset[str]` of field names the swagger marks
     `readOnly: true`. These are stripped on PUT.
   - The main BaseModel class with `ConfigDict(populate_by_name=True, extra="allow")`.
   - `ref: str | None = Field(default=None, alias="_ref")`.
   - Every field from the swagger, typed as `<type> | None = None`.
   - Python keyword collisions use trailing underscore + `Field(alias="...")`.

2. **Resource** → `src/ibx_nios_sdk/rpz/_<snake_case>.py`:
   - Subclass `WapiResource[<Model>]`.
   - `_wapi_type` = exact WAPI type string (e.g. `"record:rpz:a"`).
   - `_model` = the pydantic class.
   - `_default_return_fields` = identity/human-readable fields.
   - `_readonly_fields` = `set(<ModelModule>.READONLY_FIELDS)`.

3. **Service wiring** → add `@cached_property` in `rpz/_service.py`.

4. **Export** from `rpz/__init__.py`.

5. **Tests** → `tests/rpz/test_<snake_case>.py` covering:
   - list (with representative filter)
   - get by _ref
   - find_one
   - create (body content + _return_as_object param)
   - update (readonly field strip)
   - delete (returns ref)

## RPZ-specific field notes

- `rpz_type` - string enum in practice, typed as `str | None`.
- `zone` - read-only on all RPZ record types (set by the server from `rp_zone`).
- `rp_zone` - the writable zone reference (used in create/update instead of `zone`).
- `uuid` - read-only on all RPZ record types.
- `Allrpzrecords.type` - Python keyword collision; aliased as `type_` with `Field(alias="type")`.

## Allrpzrecords: approximated fields

`Allrpzrecords` is read-only aggregate. All 12 non-`_ref` properties are
read-only per swagger. No create/update/delete operations are meaningful.

## RecordRpzHttps / RecordRpzSvcb: approximated fields

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `RecordRpzHttps.svc_parameters` | array of SvcParameters items | SvcParam entries are complex structured types keyed by SVCB key codes; typed as `list[dict[str, Any]]`. |
| `RecordRpzSvcb.svc_parameters` | array of SvcParameters items | Same rationale as RecordRpzHttps. Typed as `list[dict[str, Any]]`. |
