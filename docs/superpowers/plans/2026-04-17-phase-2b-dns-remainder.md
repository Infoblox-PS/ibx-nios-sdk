# ibx-nios-sdk Phase 2b: DNS Remaining Objects Implementation Plan

> **For agentic workers:** Implementers should follow the pattern documented in `src/ibx_nios_sdk/dns/NOTES.md`, using `View`, `ZoneAuth`, and `RecordA` from Phase 2a as concrete precedents.

**Goal:** Implement the remaining 48 DNS object types grouped into 9 batches. Each batch produces multiple model+resource+test trios in one task, following the proven Phase 2a pattern.

**Precedents (read before starting each batch):**
- `src/ibx_nios_sdk/dns/models/record_a.py` - canonical record model shape
- `src/ibx_nios_sdk/dns/models/zone_auth.py` - canonical zone model shape (with function wrappers)
- `src/ibx_nios_sdk/dns/models/view.py` - canonical non-record, non-zone shape
- `src/ibx_nios_sdk/dns/NOTES.md` - per-object pattern guide

**Swagger:** `schemas/v2.14/dns.json`. Consult `components.schemas.<TagName>` for every object.

---

## Per-Object Pattern (reference for every task)

For each object type (example: `RecordAaaa`):

1. **Model file** `src/ibx_nios_sdk/dns/models/record_aaaa.py`:
   - Inline nested types if unique to this object (e.g. `RecordAaaaDiscoveredData`).
   - Shared types from `_shared.py`: `CloudInfo`, `ExtServer`, `MemberServer`.
   - `READONLY_FIELDS: frozenset[str]` with every swagger `readOnly: true` field.
   - Main class: `ConfigDict(populate_by_name=True, extra="allow")`, `ref: str | None = Field(default=None, alias="_ref")`, every swagger property as `<type> | None = None`.
   - Deep nested fields you don't want to model can be `dict[str, Any] | None` - add an entry to `dns/NOTES.md`.

2. **Resource file** `src/ibx_nios_sdk/dns/_<snake>.py`:
   - Subclass `WapiResource[<Model>]`.
   - `_wapi_type`, `_model`, `_default_return_fields` (5–10 identity fields), `_readonly_fields = set(READONLY_FIELDS)`.
   - Typed function wrappers only for commonly-used WAPI functions (see plan).

3. **Exports:**
   - `src/ibx_nios_sdk/dns/models/__init__.py` - add model to imports + `__all__`.
   - `src/ibx_nios_sdk/dns/__init__.py` - add resource to imports + `__all__`.

4. **Service wiring** - `src/ibx_nios_sdk/dns/_service.py`:
   - Add `@cached_property` with runtime-local import.
   - Add resource class to `TYPE_CHECKING` block.

5. **Tests** `tests/dns/test_<snake>.py` - minimum 6 scenarios:
   - `test_<obj>_list` - list with one representative filter.
   - `test_<obj>_get_by_ref` - get returns populated model.
   - `test_<obj>_find_one` - first match or None.
   - `test_<obj>_create` - POST body contains submitted fields.
   - `test_<obj>_update_strips_readonly` - PUT body excludes every `READONLY_FIELDS` member.
   - `test_<obj>_delete` - returns deleted ref.
   - For resources with extattrs: `test_<obj>_extattrs_round_trip` + `test_<obj>_set_extattrs`.
   - For resources with typed function wrappers: one `test_<obj>_<function_name>` test.

6. **Run full suite + tooling** after each batch, commit once per batch.

---

## Task 1: Remaining zone types (zone_forward, zone_delegated, zone_stub, zone_rp)

**Objects (4):** `ZoneForward`, `ZoneDelegated`, `ZoneStub`, `ZoneRp`

**Pattern precedent:** `dns/models/zone_auth.py` + `dns/_zone_auth.py`.

**Field counts (swagger):** ZoneForward=31, ZoneDelegated=30, ZoneStub=38, ZoneRp=53.

**Typed function wrappers:**
- All four zone types: none required.
- (ZoneAuth's `copy_zone_records` and `lock_unlock_zone` do NOT apply here - zones forward/delegated/stub/rp have their own less-common functions; rely on generic `call_function` for them.)

**Tests:** 6 scenarios per object × 4 objects = 24 tests. Use `zone_auth` tests as a template but swap field names appropriately.

**Commit:** `feat(dns): add ZoneForward, ZoneDelegated, ZoneStub, ZoneRp resources`

---

## Task 2: `record:host` + host address sub-resources

**Objects (3):** `RecordHost`, `RecordHostIpv4addr`, `RecordHostIpv6addr`

**Why batched:** `RecordHost` has nested lists of `ipv4addrs` and `ipv6addrs`. In WAPI, those nested addrs can ALSO be accessed as standalone resources (`record:host_ipv4addr`, `record:host_ipv6addr`) - they have their own `_ref`s and support GET/PUT.

**Field counts:** RecordHost=38, RecordHostIpv4addr=33, RecordHostIpv6addr=31.

**Special handling:**
- `RecordHost.ipv4addrs` is `list[RecordHostIpv4addr] | None`. The inline model referenced here is the SAME model used for the standalone resource - define `RecordHostIpv4addr` (and v6 equivalent) in their own model files and import from `record_host.py`.
- In `record_host.py`: `from ibx_nios_sdk.dns.models.record_host_ipv4addr import RecordHostIpv4addr`.

**Typed function wrappers:** none common enough to warrant them.

**Commit:** `feat(dns): add RecordHost and host address sub-resources`

---

## Task 3: Core record types batch (aaaa, cname, ptr, mx, txt, srv, ns)

**Objects (7):** `RecordAaaa`, `RecordCname`, `RecordPtr`, `RecordMx`, `RecordTxt`, `RecordSrv`, `RecordNs`

**Pattern precedent:** `dns/models/record_a.py` + `dns/_record_a.py`.

**Field counts:** Aaaa=25, Cname=24, Ptr=27, Mx=24, Txt=22, Srv=26, Ns=13.

**Key fields differ per record type:**
- `record:aaaa` - `name`, `ipv6addr`
- `record:cname` - `name`, `canonical`
- `record:ptr` - `ptrdname`, plus `ipv4addr`/`ipv6addr`/`name`
- `record:mx` - `name`, `mail_exchanger`, `preference`
- `record:txt` - `name`, `text`
- `record:srv` - `name`, `port`, `priority`, `target`, `weight`
- `record:ns` - `name`, `nameserver`, `addresses` (list of nested `RecordNsAddresses`)

**Default return fields:** always include the 2–3 key fields per above + `view` + `zone` + `comment` + `disable`.

**Nested inline types per object:**
- `RecordAaaa` - DiscoveredData, MsAdUserData, AwsRte53RecordInfo (same shapes as RecordA equivalents).
- `RecordCname`, `RecordMx`, `RecordPtr`, `RecordSrv`, `RecordTxt` - each has its own DiscoveredData/MsAdUserData/AwsRte53 (copy the pattern from RecordA; accept repetition for clarity).
- `RecordNs` - has a `RecordNsAddresses` nested list type (different shape).

**Tests:** 6 scenarios × 7 objects = 42 tests. Use `tests/dns/test_record_a.py` as template.

**Commit:** `feat(dns): add core record types (aaaa, cname, ptr, mx, txt, srv, ns)`

---

## Task 4: DNSSEC record types (dnskey, ds, nsec, nsec3, nsec3param, rrsig)

**Objects (6):** `RecordDnskey`, `RecordDs`, `RecordNsec`, `RecordNsec3`, `RecordNsec3param`, `RecordRrsig`

**Field counts:** 16, 17, 15, 18, 16, 22.

**Special:** these are almost entirely read-only - DNSSEC records are generated by the signer, not user-editable. Expect very few non-readonly fields. That's fine; the resource class is the same CRUD shape, users just rarely `create()` or `update()`.

**Tests:** 6 scenarios × 6 = 36 tests. The `update_strips_readonly` test is especially thorough here because almost every field is readonly.

**Commit:** `feat(dns): add DNSSEC record types (dnskey, ds, nsec, nsec3, nsec3param, rrsig)`

---

## Task 5: Other record types (alias, https, dname, naptr, tlsa, caa, dhcid, svcb, unknown)

**Objects (9):** `RecordAlias`, `RecordHttps`, `RecordDname`, `RecordNaptr`, `RecordTlsa`, `RecordCaa`, `RecordDhcid`, `RecordSvcb`, `RecordUnknown`

**Field counts:** 18, 22, 22, 26, 18, 22, 11, 22, 19.

**Key fields:**
- alias: `name`, `target_name`, `target_type`
- https: `name`, `priority`, `target_name`, `svc_parameters`
- dname: `name`, `target`
- naptr: `name`, `order`, `preference`, `flags`, `services`, `regexp`, `replacement`
- tlsa: `name`, `certificate_usage`, `selector`, `matching_type`, `certificate_data`
- caa: `name`, `flag`, `tag`, `ca_value`
- dhcid: `name`, `dhcid` (mostly read-only)
- svcb: `name`, `priority`, `target_name`, `svc_parameters`
- unknown: `name`, `record_type`, `subfield_values`

**Commit:** `feat(dns): add other record types (alias, https, dname, naptr, tlsa, caa, dhcid, svcb, unknown)`

---

## Task 6: NS groups (nsgroup family)

**Objects (6):** `Nsgroup`, `NsgroupDelegation`, `NsgroupForwardingmember`, `NsgroupForwardstubserver`, `NsgroupStubmember`, `Allnsgroup`

**Field counts:** 12, 6, 6, 6, 6, 4.

**WAPI types:**
- `nsgroup`, `nsgroup:delegation`, `nsgroup:forwardingmember`, `nsgroup:forwardstubserver`, `nsgroup:stubmember`, `allnsgroup` (read-only aggregate list).

**`Allnsgroup` is read-only** - subclass `WapiResource` but users only call `list`/`get`. No `create`/`update`/`delete` expected to succeed against it. The WapiResource base still exposes those methods; WAPI will 400 on attempts. No SDK-side enforcement needed.

**Commit:** `feat(dns): add nsgroup family (nsgroup + 4 sub-types + allnsgroup)`

---

## Task 7: Shared records (sharedrecord:a, aaaa, cname, mx, srv, txt, sharedrecordgroup)

**Objects (7):** `SharedrecordA`, `SharedrecordAaaa`, `SharedrecordCname`, `SharedrecordMx`, `SharedrecordSrv`, `SharedrecordTxt`, `Sharedrecordgroup`

**Field counts:** 11, 11, 12, 13, 15, 11, 8.

**Pattern:** nearly identical to their non-shared record counterparts but with a `shared_record_group` reference (required on create).

**Commit:** `feat(dns): add shared records (a, aaaa, cname, mx, srv, txt + sharedrecordgroup)`

---

## Task 8: Misc DNS objects

**Objects (7):** `Allrecords`, `Recordnamepolicy`, `Dns64group`, `DdnsPrincipalcluster`, `DdnsPrincipalclusterGroup`, `Orderedresponsepolicyzones`, `ZoneAuthDiscrepancy`

**Field counts:** 15, 6, 11, 6, 5, 4, 6.

**Notes:**
- `allrecords` and `zoneauthdiscrepancy` are read-only.
- `dns64group` has `enable` + IP range rules - standard.
- `orderedresponsepolicyzones` holds an ordered list of zone_rp refs.

**Commit:** `feat(dns): add misc DNS objects (allrecords, recordnamepolicy, dns64group, ddns clusters, orderedresponsepolicyzones, zone_auth_discrepancy)`

---

## Task 9: Final verification + summary example

**Files:**
- Create: `examples/03_dns_inventory.py` - lists all zones, all records (by type), and all views.

- [ ] **Run full suite, mypy, ruff - all clean.**
- [ ] **Verify every WAPI type in the DNS swagger tag list has a corresponding resource in `dns/__init__.py`.**
- [ ] **Verify every top-level schema in `components.schemas` whose name matches a tag has a corresponding model.**
- [ ] **Commit:** `feat(dns): Phase 2b complete - all 52 DNS object types covered`

---

## Verification Checklist

- [ ] `pytest -v` passes (≥98 + ~150 new = ~250 tests).
- [ ] `mypy`, `ruff check`, `ruff format --check` clean.
- [ ] `python -c "from ibx_nios_sdk.dns import *; print(__all__)"` lists every resource class.
- [ ] `DnsService` has a `@cached_property` for every resource class.
- [ ] Every resource in `dns/__init__.py` has a row in `dns/NOTES.md` (or `NOTES.md` covers the category).
