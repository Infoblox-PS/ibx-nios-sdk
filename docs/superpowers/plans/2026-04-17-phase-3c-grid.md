# ibx-nios-sdk Phase 3c: Grid Domain Implementation Plan

**Goal:** Implement the Grid domain - 44 object types covering Grid configuration, members, cloud API, DHCP/DNS/TP/TI/Captive portal services, certs, licenses, upgrades, distribution, and extensible attribute definitions.

**Swagger:** `schemas/v2.14/grid.json` (download in Task 1).

**Precedent:** IPAM and DHCP domains at `src/ibx_nios_sdk/{ipam,dhcp}/`. Same structure, same patterns.

---

## Object inventory (44, grouped into batches)

**Grid core (7):**
`Grid`, `GridDhcpproperties`, `GridDns`, `GridFiledistribution`, `GridThreatprotection`, `GridThreatinsight`, `GridDashboard`

**Grid Cloud API (6):**
`GridCloudapi`, `GridCloudapiCloudstatistics`, `GridCloudapiTenant`, `GridCloudapiVm`, `GridCloudapiVmaddress`, `GridMemberCloudapi`

**Grid service restart (5):**
`GridServicerestartGroup`, `GridServicerestartStatus`, `GridServicerestartRequest`, `GridServicerestartGroupOrder`, `GridServicerestartRequestChangedobject`

**Member (9):**
`Member`, `MemberDhcpproperties`, `MemberDns`, `MemberFiledistribution`, `MemberLicense`, `MemberThreatprotection`, `MemberParentalcontrol`, `MemberThreatinsight`, `Memberdfp`

**Member cloud/sync (2):** `Membercloudsync`, `Captiveportal`

**Mastergrid (1):** `Mastergrid`

**License (4):** `GridLicensePool`, `GridLicensePoolContainer`, `LicenseGridwide`, `GridX509certificate`

**Upgrade (3):** `Upgradegroup`, `Upgradeschedule`, `Upgradestatus`

**Distribution (3):** `Distributionschedule`, `Gmcgroup`, `Gmcschedule`

**Misc (4):** `GridMaxminddbinfo`, `Natgroup`, `Restartservicestatus`, `Extensibleattributedef`

---

## Task 1: Scaffold `grid` package

Same as prior Phase 3 scaffolds. Commit: `feat(grid): scaffold grid package and wire GridService into NiosClient`.

---

## Task 2: Grid core (7)

`Grid`, `GridDhcpproperties`, `GridDns`, `GridFiledistribution`, `GridThreatprotection`, `GridThreatinsight`, `GridDashboard`

**WAPI types use colons:** `grid`, `grid:dhcpproperties`, `grid:dns`, `grid:filedistribution`, `grid:threatprotection`, `grid:threatinsight`, `grid:dashboard`.

**Snake naming:** `grid`, `grid_dhcpproperties`, `grid_dns`, etc.

**Typed function wrapper** on `GridResource`:
```python
async def restart_services(
    self, ref: str, *, member_order: str = "SIMULTANEOUSLY",
    restart_option: str = "RESTART_IF_NEEDED",
    services: list[str] | None = None,
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"member_order": member_order, "restart_option": restart_option}
    if services is not None: kwargs["services"] = services
    return await self.call_function(ref, "restartservices", **kwargs)
```

**Default return fields:** each `["name", "comment"]` plus object-specific key fields (e.g., `Grid` uses `["name", "secret"]` where available).

`Grid`, `GridDhcpproperties`, `GridDns`, etc. are all singletons in practice - NIOS has one grid. Standard CRUD still exposed.

Commit: `feat(grid): add grid core resources (grid, dhcp/dns/filedist/tp/ti/dashboard properties)`.

---

## Task 3: Grid Cloud API (6)

`GridCloudapi`, `GridCloudapiCloudstatistics`, `GridCloudapiTenant`, `GridCloudapiVm`, `GridCloudapiVmaddress`, `GridMemberCloudapi`.

**WAPI types:** `grid:cloudapi`, `grid:cloudapi:cloudstatistics`, `grid:cloudapi:tenant`, `grid:cloudapi:vm`, `grid:cloudapi:vmaddress`, `grid:member:cloudapi`.

Snake names use double-underscore where helpful, but prefer colon→underscore flat: `grid_cloudapi`, `grid_cloudapi_cloudstatistics`, `grid_cloudapi_tenant`, `grid_cloudapi_vm`, `grid_cloudapi_vmaddress`, `grid_member_cloudapi`.

**Default return fields:** `["name", "comment"]` minimum; cloud VMs add `["vm_id", "name", "kernel_id", "network_interface_count", "first_available_ip_ipv4"]` type fields as swagger allows.

Commit: `feat(grid): add grid cloud API resources`.

---

## Task 4: Grid service-restart (5)

`GridServicerestartGroup`, `GridServicerestartStatus`, `GridServicerestartRequest`, `GridServicerestartGroupOrder`, `GridServicerestartRequestChangedobject`.

**WAPI types:** `grid:servicerestart:group`, `grid:servicerestart:status`, `grid:servicerestart:request`, `grid:servicerestart:group:order`, `grid:servicerestart:request:changedobject`.

**Typed function wrapper** on `GridServicerestartGroupResource`:
```python
async def restart_services(
    self, ref: str, *, services: list[str] | None = None,
    restart_option: str = "RESTART_IF_NEEDED",
) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"restart_option": restart_option}
    if services is not None: kwargs["services"] = services
    return await self.call_function(ref, "restart", **kwargs)
```

Commit: `feat(grid): add grid service-restart resources`.

---

## Task 5: Member + per-member properties (9)

`Member`, `MemberDhcpproperties`, `MemberDns`, `MemberFiledistribution`, `MemberLicense`, `MemberThreatprotection`, `MemberParentalcontrol`, `MemberThreatinsight`, `Memberdfp`.

**WAPI types:** `member`, `member:dhcpproperties`, `member:dns`, `member:filedistribution`, `member:license`, `member:threatprotection`, `member:parentalcontrol`, `member:threatinsight`, `member:dfp`.

**Default return fields for Member:** `["host_name", "config_addr_type", "platform", "service_type_configuration", "comment"]`.

**Typed function wrappers** on `MemberResource`:
```python
async def restart_services(
    self, ref: str, *, services: list[str] | None = None,
    restart_option: str = "RESTART_IF_NEEDED",
) -> dict[str, Any]: ...  # same shape as Grid's
```

Commit: `feat(grid): add member and per-member resources`.

---

## Task 6: Member cloud/sync + captive portal + mastergrid (3)

`Membercloudsync`, `Captiveportal`, `Mastergrid`.

**WAPI types:** `member:cloudsync`, `captiveportal`, `mastergrid`.

Commit: `feat(grid): add member-cloudsync, captive-portal, mastergrid resources`.

---

## Task 7: Licensing (4)

`GridLicensePool`, `GridLicensePoolContainer`, `LicenseGridwide`, `GridX509certificate`.

**WAPI types:** `grid:license_pool`, `grid:license_pool_container`, `license:gridwide`, `grid:x509certificate`.

Commit: `feat(grid): add licensing resources (pool, container, gridwide, x509cert)`.

---

## Task 8: Upgrade + distribution (6)

`Upgradegroup`, `Upgradeschedule`, `Upgradestatus`, `Distributionschedule`, `Gmcgroup`, `Gmcschedule`.

**WAPI types:** `upgradegroup`, `upgradeschedule`, `upgradestatus`, `distributionschedule`, `grid:gmcgroup`, `grid:gmcschedule`.

`Upgradestatus` is read-only.

Commit: `feat(grid): add upgrade and distribution resources`.

---

## Task 9: Misc (4)

`GridMaxminddbinfo`, `Natgroup`, `Restartservicestatus`, `Extensibleattributedef`.

**WAPI types:** `grid:maxminddbinfo`, `natgroup`, `restartservicestatus`, `extensibleattributedef`.

`Restartservicestatus` is read-only.
`Extensibleattributedef` is the CRUD for user-defined extensible attribute (EA) schemas - the thing that powers the `extattrs` field on every other object.

**Default return fields for Extensibleattributedef:** `["name", "type", "comment", "flags"]` (alias `type` → `type_`).

Commit: `feat(grid): add misc resources (maxminddbinfo, natgroup, restartservicestatus, extensibleattributedef)`.

---

## Task 10: Final verification + example

Create `examples/06_grid_member_inventory.py`:

```python
"""Dump grid and member info.

Env vars: NIOS_GRID_URL, NIOS_USERNAME, NIOS_PASSWORD
"""

from __future__ import annotations

import asyncio

from ibx_nios_sdk import NiosClient


async def main() -> None:
    async with NiosClient() as client:
        grids = await client.grid.grid.list().all()
        print(f"Grids: {len(grids)}")
        for g in grids:
            print(f"  {g.name}")

        members = await client.grid.member.list(
            return_fields_plus=["platform", "node_info"]
        ).all()
        print(f"Members: {len(members)}")
        for m in members:
            print(f"  {m.host_name:30}  {m.platform or '':15}  {m.service_type_configuration or ''}")


if __name__ == "__main__":
    asyncio.run(main())
```

Verify swagger tag count (44) == SDK resource count. Commit: `feat(grid): Phase 3c complete - all 44 Grid object types covered`.
