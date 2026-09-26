# ibx-nios-sdk Phase 3a: IPAM Domain Implementation Plan

> **For agentic workers:** Follow the pattern in `src/ibx_nios_sdk/dns/NOTES.md`, using the DNS domain as the concrete precedent.

**Goal:** Implement the IPAM domain - 20 object types covering IPv4/IPv6 networks, network containers, address objects, VLANs, bulk hosts, network discovery, and IPAM statistics.

**Precedent:** DNS domain is the canonical per-domain pattern. Reuse those file layouts, test structures, and conventions.

**Swagger:** `schemas/v2.14/ipam.json` (downloaded in Task 1).

**Tech Stack:** Python 3.11+, `httpx>=0.27`, `pydantic>=2`. Foundation from Phase 0+1 is stable; Phase 2 established the per-domain pattern.

---

## Domain object inventory (20 objects)

Grouped for batching:

**IPv4 networks/containers/addresses (5):** `Network`, `Networkcontainer`, `Networktemplate`, `Ipv4address`, `Networkview`

**IPv6 networks/containers (4):** `Ipv6network`, `Ipv6networkcontainer`, `Ipv6networktemplate`, `Ipv6address`

**VLANs (3):** `Vlan`, `Vlanview`, `Vlanrange`

**Bulk hosts (2):** `Bulkhost`, `Bulkhostnametemplate`

**Discovery (3):** `Discoverytask`, `NetworkDiscovery`, `Superhost` + `Superhostchild` (4 actually - split across 2 batches)

**Policy / statistics (2):** `Hostnamerewritepolicy`, `IpamStatistics`

---

## Task 1: Download swagger + scaffold ipam package

**Files:**
- Create: `schemas/v2.14/ipam.json`
- Create: `src/ibx_nios_sdk/ipam/__init__.py`
- Create: `src/ibx_nios_sdk/ipam/_service.py`
- Create: `src/ibx_nios_sdk/ipam/NOTES.md`
- Create: `src/ibx_nios_sdk/ipam/models/__init__.py`
- Create: `src/ibx_nios_sdk/ipam/models/_shared.py` (empty stub; grows per batch)
- Modify: `src/ibx_nios_sdk/client.py` - add `client.ipam` cached_property
- Modify: `src/ibx_nios_sdk/__init__.py` - export `IpamService`
- Create: `tests/ipam/__init__.py`, `tests/ipam/conftest.py`, `tests/ipam/test_service.py`

- [ ] **Step 1.1: Download swagger**

```bash
cd /Users/mjsmith/dev-projects/ibx-nios-sdk
curl -fsSL -o schemas/v2.14/ipam.json \
  https://infobloxopen.github.io/nios-swagger/swagger-ui/openspec/v2.14/ipam.json
python3 -c "import json; d=json.load(open('schemas/v2.14/ipam.json')); print(d['info']['version'], len(d['paths']), 'paths')"
```

Expected: `2.14 40 paths` (or similar).

- [ ] **Step 1.2: Scaffold ipam package** (follow DNS skeleton from Phase 2a Task 2):
  - `IpamService` class with initially-empty `@cached_property` list (filled in later tasks).
  - `ipam/__init__.py` exports `IpamService`.
  - `NOTES.md` copies the Phase 2a pattern guide, adjusted for IPAM.
  - `tests/ipam/conftest.py` mirrors `tests/dns/conftest.py`.
  - `tests/ipam/test_service.py` tests `client.ipam is client.ipam` and service class exists.

- [ ] **Step 1.3: Wire `ipam` into `NiosClient.client.py`** - add `@cached_property def ipam(self) -> IpamService: ...` with runtime-local import and TYPE_CHECKING guard.

- [ ] **Step 1.4: Export `IpamService` from top-level `__init__.py`**.

- [ ] **Step 1.5: Run tests + tooling, all clean.**

- [ ] **Step 1.6: Commit** - `feat(ipam): scaffold ipam package and wire IpamService into NiosClient`

---

## Task 2: Network view + IPv4 networks/containers/templates

**Objects (5):** `Networkview`, `Network`, `Networkcontainer`, `Networktemplate`, `Ipv4address`

**WAPI types + default return fields:**

| Class | wapi_type | snake | default_return_fields |
|---|---|---|---|
| Networkview | networkview | networkview | `["name", "is_default", "comment"]` |
| Network | network | network | `["network", "network_view", "comment", "disable"]` |
| Networkcontainer | networkcontainer | networkcontainer | `["network", "network_view", "comment"]` |
| Networktemplate | networktemplate | networktemplate | `["name", "netmask", "comment"]` |
| Ipv4address | ipv4address | ipv4address | `["ip_address", "mac_address", "network", "network_view", "usage"]` |

**Special: Typed function wrapper for `next_available_ip`:**

The most commonly-used WAPI function in all of NIOS - must be typed. Add to `NetworkResource`:

```python
async def next_available_ip(
    self,
    ref: str,
    *,
    num: int = 1,
    exclude: list[str] | None = None,
) -> dict[str, Any]:
    """Return the next `num` available IPs in this network.

    Returns dict like ``{"ips": ["10.0.0.5", "10.0.0.6"]}``.
    """
    kwargs: dict[str, Any] = {"num": num}
    if exclude is not None:
        kwargs["exclude"] = exclude
    return await self.call_function(ref, "next_available_ip", **kwargs)
```

Also add to `NetworkcontainerResource`:

```python
async def next_available_network(
    self,
    ref: str,
    *,
    cidr: int,
    num: int = 1,
    exclude: list[str] | None = None,
) -> dict[str, Any]:
    """Carve out the next `num` networks of given `cidr` from this container."""
    kwargs: dict[str, Any] = {"cidr": cidr, "num": num}
    if exclude is not None:
        kwargs["exclude"] = exclude
    return await self.call_function(ref, "next_available_network", **kwargs)
```

**Tests:** 6 scenarios per object + 1 function-call test per typed wrapper = 32 tests (5×6 + 2).

**Commit:** `feat(ipam): add IPv4 networks, containers, templates, addresses, network view`

---

## Task 3: IPv6 networks/containers/templates/addresses

**Objects (4):** `Ipv6network`, `Ipv6networkcontainer`, `Ipv6networktemplate`, `Ipv6address`

Pattern identical to Task 2's IPv4 counterparts, but IPv6-specific fields (`network` is CIDR like `2001:db8::/64`, `auto_create_reversezone`, etc.).

**Typed function wrappers:**
- `Ipv6networkResource.next_available_ip` - same pattern as `NetworkResource`.
- `Ipv6networkcontainerResource.next_available_network` - same pattern.

**Default return fields:**

| Class | wapi_type | default_return_fields |
|---|---|---|
| Ipv6network | ipv6network | `["network", "network_view", "comment", "disable"]` |
| Ipv6networkcontainer | ipv6networkcontainer | `["network", "network_view", "comment"]` |
| Ipv6networktemplate | ipv6networktemplate | `["name", "cidr", "comment"]` |
| Ipv6address | ipv6address | `["ip_address", "duid", "network", "network_view", "usage"]` |

**Tests:** 6×4 + 2 = 26 tests.

**Commit:** `feat(ipam): add IPv6 networks, containers, templates, addresses`

---

## Task 4: VLANs (vlan, vlanview, vlanrange)

**Objects (3):** `Vlan`, `Vlanview`, `Vlanrange`

| Class | wapi_type | default_return_fields |
|---|---|---|
| Vlan | vlan | `["id", "name", "parent", "comment"]` |
| Vlanview | vlanview | `["name", "start_vlan_id", "end_vlan_id", "comment"]` |
| Vlanrange | vlanrange | `["name", "vlan_view", "start_vlan_id", "end_vlan_id"]` |

**Note:** `Vlan.id` collides with no Python keyword but shadowing `id()` builtin within the instance is fine. Keep as `id: int | None = None`.

**Typed function wrappers:** none.

**Tests:** 6×3 = 18 tests.

**Commit:** `feat(ipam): add VLAN resources (vlan, vlanview, vlanrange)`

---

## Task 5: Bulk hosts

**Objects (2):** `Bulkhost`, `Bulkhostnametemplate`

| Class | wapi_type | default_return_fields |
|---|---|---|
| Bulkhost | bulkhost | `["prefix", "start_addr", "end_addr", "comment"]` |
| Bulkhostnametemplate | bulkhostnametemplate | `["template_name", "template_format"]` |

**Tests:** 6×2 = 12 tests.

**Commit:** `feat(ipam): add bulk host resources`

---

## Task 6: Discovery + superhosts

**Objects (4):** `Discoverytask`, `NetworkDiscovery`, `Superhost`, `Superhostchild`

| Class | wapi_type | default_return_fields |
|---|---|---|
| Discoverytask | discovery:discoverytask | discovery_discoverytask | `["status", "network_view", "member_name"]` |
| NetworkDiscovery | network_discovery | network_discovery | `["address", "network_view", "discovered_data"]` |
| Superhost | superhost | superhost | `["name", "comment", "dhcp_associated_objects"]` |
| Superhostchild | superhostchild | superhostchild | `["name", "record_parent", "parent"]` |

**Note:** WAPI type for `Discoverytask` contains a colon (`discovery:discoverytask`) - ensure `_wapi_type` string matches.

`NetworkDiscovery` is read-only in practice (discovery results, not user-created).

**Tests:** 6×4 = 24 tests.

**Commit:** `feat(ipam): add discovery and superhost resources`

---

## Task 7: Policy + statistics (Hostnamerewritepolicy, IpamStatistics)

**Objects (2):** `Hostnamerewritepolicy`, `IpamStatistics`

| Class | wapi_type | default_return_fields |
|---|---|---|
| Hostnamerewritepolicy | hostnamerewritepolicy | `["name", "comment", "pre_script", "post_script"]` |
| IpamStatistics | ipam:statistics | ipam_statistics | `["network", "network_view", "utilization"]` |

**Note:** `IpamStatistics` is read-only - aggregated stats per network.

**Tests:** 6×2 = 12 tests.

**Commit:** `feat(ipam): add hostname-rewrite-policy and ipam-statistics resources`

---

## Task 8: Final verification + IPAM example

**Files:**
- Create: `examples/04_ipam_next_ip.py` - demonstrates `next_available_ip`.

- [ ] Run full suite + verify every IPAM swagger tag has a resource.
- [ ] Commit: `feat(ipam): Phase 3a complete - all 20 IPAM object types covered`.

### Example script

```python
"""Allocate the next available IP in a network via next_available_ip function.

Env vars: NIOS_GRID_URL, NIOS_USERNAME, NIOS_PASSWORD

Usage: python examples/04_ipam_next_ip.py <cidr> <network_view>
"""

from __future__ import annotations

import asyncio
import sys

from ibx_nios_sdk import NiosClient


async def main(cidr: str, view: str = "default") -> None:
    async with NiosClient() as client:
        net = await client.ipam.network.find_one(network=cidr, network_view=view)
        if net is None:
            print(f"network {cidr} not found in view {view}")
            return
        result = await client.ipam.network.next_available_ip(net.ref, num=3)
        print(f"next 3 available IPs in {cidr}: {result.get('ips', [])}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <cidr> [network_view]")
        sys.exit(1)
    asyncio.run(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "default"))
```

---

## Verification Checklist

- [ ] All 20 IPAM swagger tags have a matching `WapiResource` subclass.
- [ ] `client.ipam.network.next_available_ip(ref, num=5)` is typed and callable.
- [ ] `client.ipam.networkcontainer.next_available_network(ref, cidr=26)` is typed.
- [ ] Full `pytest` green.
- [ ] `mypy`, `ruff check`, `ruff format --check` clean.
- [ ] `python -c "from ibx_nios_sdk.ipam import *; print(len(__all__))"` ≥ 21 (20 resources + IpamService).
