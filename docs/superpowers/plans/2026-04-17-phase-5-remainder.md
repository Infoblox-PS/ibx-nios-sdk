# ibx-nios-sdk Phase 5: Remaining Sub-Domains Implementation Plan

**Goal:** Implement the final 8 sub-domains to complete all 17 WAPI swaggers.

Totals: **77 objects** across `dtc` (22), `cloud` (7), `discovery` (14), `federatedrealms` (2), `microsoftserver` (6), `smartfolder` (3), `notification` (3), `misc` (20 - incl. special `Fileop`).

**Precedent:** all prior domains. Follow the same per-domain file layout, `@cached_property` service, per-object model+resource+test, single HttpClient from Phase 0+1.

**Swaggers:** download each to `schemas/v2.14/<domain>.json` in each sub-domain's scaffold task.

Each sub-domain has its own batch of commits. Per-sub-domain structure:
1. Scaffold commit
2. One or more resource-batch commits
3. Optional final verification commit

---

## Sub-domain 1: `dtc` (22 objects)

Dynamic Traffic Control - load balancing / GSLB.

**Objects:** `Dtc`, `DtcServer`, `DtcPool`, `DtcTopology`, `DtcLbdn`, `DtcMonitor`, `DtcMonitorHttp`, `DtcMonitorIcmp`, `DtcMonitorPdp`, `DtcMonitorSip`, `DtcMonitorSnmp`, `DtcMonitorTcp`, `DtcRecordA`, `DtcRecordAaaa`, `DtcRecordCname`, `DtcRecordNaptr`, `DtcRecordSrv`, `DtcCertificate`, `DtcAllrecords`, `DtcObject`, `DtcTopologyRule`, `DtcTopologyLabel`

**Suggested batching (3 commits after scaffold):**
- Core + servers + pools: `Dtc`, `DtcServer`, `DtcPool`, `DtcLbdn`, `DtcTopology`, `DtcTopologyRule`, `DtcTopologyLabel`, `DtcCertificate`, `DtcObject`, `DtcAllrecords` (10)
- Monitors: `DtcMonitor`, `DtcMonitorHttp`, `DtcMonitorIcmp`, `DtcMonitorPdp`, `DtcMonitorSip`, `DtcMonitorSnmp`, `DtcMonitorTcp` (7)
- Records: `DtcRecordA`, `DtcRecordAaaa`, `DtcRecordCname`, `DtcRecordNaptr`, `DtcRecordSrv` (5)

---

## Sub-domain 2: `cloud` (7 objects)

**Objects:** `Awsrte53taskgroup`, `Awsuser`, `Azurednstaskgroup`, `Azureuser`, `Gcpdnstaskgroup`, `Gcpuser`, `Multiregions`

One commit for scaffold, one for the 7 resources.

---

## Sub-domain 3: `discovery` (14 objects)

**Objects:** `Discovery`, `DiscoveryCredentialgroup`, `DiscoveryDevice`, `DiscoveryDevicecomponent`, `DiscoveryDeviceinterface`, `DiscoveryDeviceneighbor`, `DiscoveryDevicesupportbundle`, `DiscoveryDiagnostictask`, `DiscoveryGridproperties`, `DiscoveryMemberproperties`, `DiscoverySdnnetwork`, `DiscoveryStatus`, `DiscoveryVrf`, `Vdiscoverytask`

Scaffold commit + 1-2 resource commits.

---

## Sub-domain 4: `federatedrealms` (2 objects)

**Objects:** `Federatedrealms`, `Fedipamop`

Single commit: scaffold + both resources.

---

## Sub-domain 5: `microsoftserver` (6 objects)

**Objects:** `Msserver`, `MsserverAdsitesDomain`, `MsserverAdsitesSite`, `MsserverDhcp`, `MsserverDns`, `Mssuperscope`

Scaffold commit + one resource commit.

---

## Sub-domain 6: `smartfolder` (3 objects)

**Objects:** `SmartfolderChildren`, `SmartfolderGlobal`, `SmartfolderPersonal`

Scaffold commit + one resource commit.

---

## Sub-domain 7: `notification` (3 objects)

**Objects:** `NotificationRestEndpoint`, `NotificationRestTemplate`, `NotificationRule`

Scaffold commit + one resource commit.

---

## Sub-domain 8: `misc` (20 objects, includes special `Fileop`)

**Objects:** `Allendpoints`, `Bfdtemplate`, `Csvimporttask`, `Datacollectioncluster`, `DbObjects`, `Dbsnapshot`, `DeletedObjects`, `DxlEndpoint`, `Fileop`, `Kerberoskey`, `Capacityreport`, `OutboundCloudclient`, `PxgridEndpoint`, `Ruleset`, `Scavengingtask`, `Scheduledtask`, `Search`, `SyslogEndpoint`, `Taxii`, `Tftpfiledir`

**Special handling for `Fileop`:**
- `Fileop` is NOT a CRUD object - it is a function-only endpoint at `/fileop?_function=<name>`. WAPI doesn't support GET/POST/PUT/DELETE for stored `fileop` records; everything is function calls (uploadinit, csv_import, csv_export, etc.).
- Implement as a plain class `FileopResource` with `__init__(self, client: HttpClient)` - do NOT subclass `WapiResource`. Expose typed methods: `upload_init()`, `upload_certificate()`, `csv_import()`, `csv_export()`, `csv_export_progress()`, `csv_snapshot_file()`, `download_complete()`, `downloadcertificate()`, and one generic `call(function_name, **kwargs)`.
- Resource wiring: `MiscService.fileop: FileopResource` (still `@cached_property`, but returns plain class).
- Tests: test the typed methods like other function wrappers (POST to `/fileop?_function=<name>` with body).

**Other misc objects are standard CRUD.** `Allendpoints` and `DeletedObjects` are read-only aggregates. `Search` is a function endpoint like `fileop` - treat similarly (plain class, POST-only). Verify each in swagger.

Suggested batching:
- Scaffold
- Standard objects (15 or so CRUD)
- Special function-only: `Fileop`, `Search` (2)
- Final verification

---

## Cross-cutting rules (carry through from prior phases)

- Every resource: model + resource + test + DomainService wiring.
- 6-scenario tests minimum per CRUD object; for function-only objects, test the typed methods.
- Python keyword collisions → `type_` alias.
- Deeply nested → `dict[str, Any] | None` with NOTES.md entries.
- Single HttpClient, single NiosClient entry point. Each sub-domain adds `client.<domain>` cached_property.
- pytest + mypy + ruff check + ruff format --check all clean before every commit.
- Commit message per-batch: `feat(<domain>): add <N> <category> resources` or `feat(<domain>): scaffold <domain> package and wire <Domain>Service into NiosClient`.

---

## Verification Checklist (end of Phase 5)

- [ ] All 8 sub-domains scaffolded.
- [ ] All 77 swagger tags have corresponding SDK resources (plus `Fileop`/`Search` as function-only plain classes).
- [ ] Full pytest suite passes.
- [ ] mypy strict, ruff check, ruff format --check all clean.
- [ ] Import smoke: `from ibx_nios_sdk import NiosClient, DtcService, CloudService, DiscoveryService, FederatedrealmsService, MicrosoftserverService, SmartfolderService, NotificationService, MiscService` works.
- [ ] 17 schemas committed under `schemas/v2.14/*.json` (one per swagger source).
