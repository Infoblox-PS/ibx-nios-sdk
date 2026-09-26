# DNS domain - swagger-vs-reality notes + resource pattern

## Per-object file layout

For each new WAPI object type ``<wapi:type>``:

1. **Model** → ``src/ibx_nios_sdk/dns/models/<snake_case>.py`` containing:
   - A ``READONLY_FIELDS: frozenset[str]`` of field names the swagger marks
     ``readOnly: true``. These are stripped on PUT.
   - Inline nested-type classes for schemas not reused elsewhere
     (e.g. ``RecordAAwsRte53RecordInfo``).
   - The main BaseModel class with ``ConfigDict(populate_by_name=True, extra="allow")``.
   - ``ref: str | None = Field(default=None, alias="_ref")``.
   - Every field from the swagger, typed as ``<type> | None = None``.
   - Python keyword collisions use trailing underscore + ``Field(alias="...")``.

2. **Resource** → ``src/ibx_nios_sdk/dns/_<snake_case>.py``:
   - Subclass ``WapiResource[<Model>]``.
   - ``_wapi_type`` = exact WAPI type string (e.g. ``"record:a"``).
   - ``_model`` = the pydantic class.
   - ``_default_return_fields`` = 5–10 identity/human-readable fields.
   - ``_readonly_fields`` = ``set(<ModelModule>.READONLY_FIELDS)``.
   - Typed method wrappers ONLY for functions used in >50% of user scripts
     (e.g. ``zone_auth.copy_zone_records``). Others use ``.call_function(ref, ...)``.

3. **Service wiring** → add ``@cached_property`` in ``dns/_service.py``.

4. **Export** from ``dns/__init__.py`` and ``dns/models/__init__.py``.

5. **Tests** → ``tests/dns/test_<snake_case>.py`` covering:
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
`schemas/v2.14/dns.json`. Each entry should include:

- Object and field affected
- What the swagger claims
- What WAPI actually does
- Workaround in the SDK (e.g. model override, readonly strip, etc.)

_(Populated as issues are discovered during implementation.)_

---

## ZoneAuth: approximated fields

The following `ZoneAuth` fields are typed as `dict[str, Any]` (or
`list[dict[str, Any]]`) rather than fully modelled nested classes. All
129 swagger properties appear on the model; only sub-fields of complex nested
objects are approximated.

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `aws_rte53_zone_info` | `ZoneAuthAwsRte53ZoneInfo` | All 7 sub-fields are `readOnly`; typed as `dict[str, Any]` |
| `copyzonerecords` | `ZoneAuthCopyzonerecords` | Function-type field (not a data field); typed as `dict[str, Any]` |
| `dnssec_export` | `ZoneAuthDnssecExport` | Function-type field; typed as `dict[str, Any]` |
| `dnssec_get_zone_keys` | `ZoneAuthDnssecGetZoneKeys` | Function-type field; typed as `dict[str, Any]` |
| `dnssec_key_params.ksk_algorithms` | `list[ZoneauthdnseckeyparamsKskAlgorithms]` | Deep nested DNSSEC algorithm list; typed as `list[dict[str, Any]]` |
| `dnssec_key_params.zsk_algorithms` | `list[ZoneauthdnseckeyparamsZskAlgorithms]` | Same as above |
| `dnssec_operation` | `ZoneAuthDnssecOperation` | Function-type field; typed as `dict[str, Any]` |
| `dnssec_set_zone_keys` | `ZoneAuthDnssecSetZoneKeys` | Function-type field; typed as `dict[str, Any]` |
| `dnssecgetkskrollover` | `ZoneAuthDnssecgetkskrollover` | Function-type field; typed as `dict[str, Any]` |
| `execute_dns_parent_check` | `ZoneAuthExecuteDnsParentCheck` | Function-type field; typed as `dict[str, Any]` |
| `lock_unlock_zone` | `ZoneAuthLockUnlockZone` | Function-type field (use `ZoneAuthResource.lock_unlock_zone()` wrapper instead) |
| `run_scavenging` | `ZoneAuthRunScavenging` | Function-type field (zero properties in swagger); typed as `dict[str, Any]` |
| `scavenging_settings.scavenging_schedule` | `ZoneauthscavengingsettingsScavengingSchedule` | Deep nested schedule config; ZoneAuth-only, rarely written |
| `scavenging_settings.expression_list` | `list[ZoneauthscavengingsettingsExpressionList]` | Filter expression list; ZoneAuth-only, rarely written |
| `scavenging_settings.ea_expression_list` | `list[ZoneauthscavengingsettingsEaExpressionList]` | Same shape; ZoneAuth-only, rarely written |

`ZoneAuthDnssecKeyParams` and `ZoneAuthScavengingSettings` themselves are fully
modelled; only their deep sub-fields listed above are approximated.

---

## View: approximated fields

The following `View` fields are typed as `dict[str, Any]` rather than fully
modelled nested classes. They are all deeply nested, View-specific schemas
that are rarely used in practice.

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `run_scavenging` | `ViewRunScavenging` | Zero properties in swagger (empty object); typed as `dict[str, Any]` |
| `scavenging_settings.scavenging_schedule` | `ViewscavengingsettingsScavengingSchedule` | Deep nested schedule config; 12 fields, View-only, rarely written |
| `scavenging_settings.expression_list` | `list[ViewscavengingsettingsExpressionList]` | 5-field filter expression; View-only, rarely written |
| `scavenging_settings.ea_expression_list` | `list[ViewscavengingsettingsEaExpressionList]` | Same shape as expression_list; View-only, rarely written |

`ViewScavengingSettings` itself is fully modelled; only its three sub-fields
above are approximated as `dict[str, Any]`.

All other View-level fields (83 of 86 properties, excluding `_ref` counted in
swagger total) are fully typed.

---

## ZoneForward: approximated fields

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `lock_unlock_zone` | `ZoneForwardLockUnlockZone` | Function-type field; typed as `dict[str, Any]` |

All other 30 fields are fully typed.

---

## ZoneDelegated: approximated fields

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `lock_unlock_zone` | `ZoneDelegatedLockUnlockZone` | Function-type field; typed as `dict[str, Any]` |

All other 29 fields are fully typed.

---

## ZoneStub: approximated fields

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `lock_unlock_zone` | `ZoneStubLockUnlockZone` | Function-type field; typed as `dict[str, Any]` |

All other 37 fields are fully typed.

---

## RecordHttps / RecordSvcb: approximated fields

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `RecordHttps.svc_parameters` | array of `RecordHttpsSvcParameters` items | SvcParam entries are complex structured types keyed by SVCB key codes (alpn, port, ipv4hint, ipv6hint, ech, etc.); the schema is a heterogeneous union that varies per key code. Typed as `list[dict[str, Any]]`. |
| `RecordSvcb.svc_parameters` | array of `RecordSvcbSvcParameters` items | Same rationale as RecordHttps.svc_parameters above. Typed as `list[dict[str, Any]]`. |

---

## RecordUnknown: approximated fields

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `RecordUnknown.subfield_values` | array of per-record-type subfield items | Structure varies by `record_type`; no fixed schema. Typed as `list[dict[str, Any]]`. |

---

## ZoneRp: approximated fields

| Field | Swagger schema | Reason approximated |
|---|---|---|
| `copy_rpz_records` | `ZoneRpCopyRpzRecords` | Function-type field; typed as `dict[str, Any]` |
| `lock_unlock_zone` | `ZoneRpLockUnlockZone` | Function-type field; typed as `dict[str, Any]` |
| `fireeye_rule_mapping.fireeye_alert_mapping` | `list[ZoneRpFireeyeRuleMappingFireeyeAlertMapping]` | FireEye-specific alert-to-policy mapping; rarely configured; typed as `list[dict[str, Any]]` |

`ZoneRpFireeyeRuleMapping` itself is fully modelled (3 of its 3 top-level fields);
only the `fireeye_alert_mapping` sub-list items are approximated. All other
52 ZoneRp fields are fully typed.
