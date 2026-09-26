# ibx-nios-sdk Phase 3b: DHCP Domain Implementation Plan

**Goal:** Implement the DHCP domain - 27 object types covering DHCP ranges, fixed addresses, shared networks, filters, options, failover, leases, and DHCP statistics.

**Swagger:** `schemas/v2.14/dhcp.json` (downloaded in Task 1).

**Precedent:** IPAM domain at `src/ibx_nios_sdk/ipam/` - same structure, same patterns.

---

## Object inventory (27)

- **Ranges (5):** `Range`, `Rangetemplate`, `Ipv6range`, `Ipv6rangetemplate`, `Orderedranges`
- **Fixed addresses (4):** `Fixedaddress`, `Fixedaddresstemplate`, `Ipv6fixedaddress`, `Ipv6fixedaddresstemplate`
- **Shared networks (2):** `Sharednetwork`, `Ipv6sharednetwork`
- **Filters (6):** `Filterfingerprint`, `Filtermac`, `Filternac`, `Filteroption`, `Filterrelayagent`, `Ipv6filteroption`
- **Options (4):** `Dhcpoptiondefinition`, `Dhcpoptionspace`, `Ipv6dhcpoptiondefinition`, `Ipv6dhcpoptionspace`
- **Other (6):** `Dhcpfailover`, `Fingerprint`, `Lease`, `Macfilteraddress`, `Roaminghost`, `DhcpStatistics`

---

## Task 1: Scaffold `dhcp` package

Same as Phase 3a Task 1 but for `dhcp/`. Commit: `feat(dhcp): scaffold dhcp package and wire DhcpService into NiosClient`.

---

## Task 2: Ranges (5)

`Range`, `Rangetemplate`, `Ipv6range`, `Ipv6rangetemplate`, `Orderedranges`.

**Typed wrapper** on `RangeResource` and `Ipv6rangeResource`:
```python
async def next_available_ip(self, ref: str, *, num: int = 1, exclude: list[str] | None = None) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"num": num}
    if exclude is not None: kwargs["exclude"] = exclude
    return await self.call_function(ref, "next_available_ip", **kwargs)
```

`Orderedranges` is a read-only ordering aggregate over DHCP ranges in a network.

**Default return fields:**
- Range: `["start_addr", "end_addr", "network", "network_view", "comment", "disable"]`
- Rangetemplate: `["name", "number_of_addresses", "offset", "comment"]`
- Ipv6range: `["start_addr", "end_addr", "network", "network_view", "comment", "disable"]`
- Ipv6rangetemplate: `["name", "number_of_addresses", "offset", "comment"]`
- Orderedranges: `["network", "network_view", "ranges"]`

Commit: `feat(dhcp): add DHCP range resources`.

---

## Task 3: Fixed addresses (4)

`Fixedaddress`, `Fixedaddresstemplate`, `Ipv6fixedaddress`, `Ipv6fixedaddresstemplate`.

**Default return fields:**
- Fixedaddress: `["ipv4addr", "mac", "name", "network", "network_view", "comment"]`
- Fixedaddresstemplate: `["name", "number_of_addresses", "offset", "comment"]`
- Ipv6fixedaddress: `["ipv6addr", "duid", "name", "network", "network_view", "comment"]`
- Ipv6fixedaddresstemplate: `["name", "number_of_addresses", "offset", "comment"]`

Commit: `feat(dhcp): add DHCP fixed address resources`.

---

## Task 4: Shared networks (2)

`Sharednetwork`, `Ipv6sharednetwork`.

**Default return fields:** both `["name", "network_view", "networks", "comment", "disable"]`.

Commit: `feat(dhcp): add DHCP shared network resources`.

---

## Task 5: Filters (6)

`Filterfingerprint`, `Filtermac`, `Filternac`, `Filteroption`, `Filterrelayagent`, `Ipv6filteroption`.

All small objects, follow the View pattern.

**Default return fields (each):** `["name", "comment"]` minimum, plus filter-specific key fields (e.g., `Filtermac` adds `leasetime`).

Commit: `feat(dhcp): add DHCP filter resources`.

---

## Task 6: Option definitions + spaces (4)

`Dhcpoptiondefinition`, `Dhcpoptionspace`, `Ipv6dhcpoptiondefinition`, `Ipv6dhcpoptionspace`.

**Default return fields:**
- Dhcpoptiondefinition: `["name", "code", "space", "type", "comment"]`
- Dhcpoptionspace: `["name", "comment"]`
- Same for IPv6 equivalents (`name`, `code`, `space`, `type`, `comment`).

`type` field is a Python builtin name - alias to `type_`: `type_: str | None = Field(default=None, alias="type")`. Use `"type_"` in `READONLY_FIELDS`.

Commit: `feat(dhcp): add DHCP option definition and space resources`.

---

## Task 7: Other (6)

`Dhcpfailover`, `Fingerprint`, `Lease`, `Macfilteraddress`, `Roaminghost`, `DhcpStatistics`.

**Default return fields:**
- Dhcpfailover: `["name", "primary", "secondary", "comment"]`
- Fingerprint: `["name", "comment", "type", "device_class"]` (alias `type` → `type_`)
- Lease: `["address", "hardware", "client_hostname", "binding_state"]` (READONLY in practice)
- Macfilteraddress: `["mac", "filter", "comment"]`
- Roaminghost: `["name", "mac", "network_view", "address_type", "comment"]`
- DhcpStatistics: `["dhcp_utilization", "network", "network_view"]` (READONLY)

Commit: `feat(dhcp): add DHCP failover, fingerprint, lease, mac filter, roaming host, statistics resources`.

`Lease` and `DhcpStatistics` are read-only aggregates.

---

## Task 8: Final verification + example

Create `examples/05_dhcp_lease_report.py`:

```python
"""List all DHCP leases with their binding states.

Env vars: NIOS_GRID_URL, NIOS_USERNAME, NIOS_PASSWORD
"""

from __future__ import annotations

import asyncio

from ibx_nios_sdk import NiosClient


async def main() -> None:
    async with NiosClient() as client:
        leases = await client.dhcp.lease.list(
            return_fields_plus=["hardware", "client_hostname", "starts", "ends"]
        ).all()
        print(f"Total leases: {len(leases)}")
        for l in leases[:50]:
            print(f"  {l.address!s:20}  {l.binding_state!s:12}  {l.client_hostname or '<no hostname>'}")


if __name__ == "__main__":
    asyncio.run(main())
```

Verify swagger tag count matches resource count, commit: `feat(dhcp): Phase 3b complete - all 27 DHCP object types covered`.
