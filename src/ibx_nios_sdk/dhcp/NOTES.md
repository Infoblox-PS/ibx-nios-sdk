# DHCP domain - swagger-vs-reality notes + resource pattern

## Per-object file layout

For each new WAPI object type `<wapi:type>`:

1. **Model** → `src/ibx_nios_sdk/dhcp/models/<snake_case>.py` containing:
   - A `READONLY_FIELDS: frozenset[str]` of field names the swagger marks
     `readOnly: true`. These are stripped on PUT.
   - Inline nested-type classes for schemas not reused elsewhere.
   - The main BaseModel class with `ConfigDict(populate_by_name=True, extra="allow")`.
   - `ref: str | None = Field(default=None, alias="_ref")`.
   - Every field from the swagger, typed as `<type> | None = None`.
   - Python keyword collisions use trailing underscore + `Field(alias="...")`.

2. **Resource** → `src/ibx_nios_sdk/dhcp/_<snake_case>.py`:
   - Subclass `WapiResource[<Model>]`.
   - `_wapi_type` = exact WAPI type string (e.g. `"range"`).
   - `_model` = the pydantic class.
   - `_default_return_fields` = 5–10 identity/human-readable fields.
   - `_readonly_fields` = `set(<ModelModule>.READONLY_FIELDS)`.
   - Typed method wrappers ONLY for functions used in >50% of user scripts.
     Others use `.call_function(ref, ...)`.

3. **Service wiring** → add `@cached_property` in `dhcp/_service.py`.

4. **Export** from `dhcp/__init__.py` and `dhcp/models/__init__.py`.

5. **Tests** → `tests/dhcp/test_<snake_case>.py` covering:
   - list (with representative filter)
   - get by _ref
   - find_one
   - create (body content + _return_as_object param)
   - update (readonly field strip)
   - delete (returns ref)
   - one function call (if any typed wrappers added)

## Python naming notes

- `type` field → `type_` alias: `type_: str | None = Field(default=None, alias="type")`
- `Macfilteraddress.filter` shadows builtin but is not a keyword - keep as `filter`.
- `DhcpStatistics` wapi_type is `dhcp:statistics` (colon in type string).
- `Lease` and `DhcpStatistics` are read-only aggregates.
- `Orderedranges` is read-only aggregate.

## Deeply nested types (inlined as dicts)

- Range: `cloud_info`, `discovery_basic_poll_settings`, `discovery_blackout_setting`,
  `ms_ad_user_data`, `subscribe_settings`, `port_control_blackout_setting`,
  `options`, `fingerprint_filter_rules`, `logic_filter_rules`, `mac_filter_rules`,
  `ms_options`, `nac_filter_rules`, `option_filter_rules`, `relay_agent_filter_rules`,
  `exclude` (member exclusions)
- Fixedaddress: `cloud_info`, `cli_credentials`, `discovered_data`, `logic_filter_rules`,
  `ms_ad_user_data`, `ms_options`, `options`, `snmp3_credential`, `snmp_credential`
- Sharednetwork: `ms_ad_user_data`, `logic_filter_rules`, `options`, `networks`
- Dhcpfailover: (all standard fields)
- Roaminghost: `options`, `ipv6_options`

## Swagger-vs-reality deltas

Record any places where the NIOS v2.14 WAPI behavior diverges from
`schemas/v2.14/dhcp.json`. Each entry should include:

- Object and field affected
- What the swagger claims
- What WAPI actually does
- Workaround in the SDK (e.g. model override, readonly strip, etc.)

_(Populated as issues are discovered during implementation.)_
