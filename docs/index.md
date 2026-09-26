# Infoblox NIOS SDK

**ibx-nios-sdk** is a modern, fully async Python SDK for the [Infoblox NIOS WAPI](https://docs.infoblox.com/space/nios90/35430400/WAPI+Documentation).
It covers 17 WAPI domains and 280 resource types, giving you type-safe, paginated access to every major NIOS object - all over `async/await`.

---

## Quickstart

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient(
        grid_url="https://gm.example.com",
        username="admin",
        password="infoblox",
    ) as client:
        # List all authoritative DNS zones
        async for zone in client.dns.zone_auth.list(view="default"):
            print(zone.fqdn)

        # Allocate the next available IP from a network
        ref = "network/ZG5z:10.10.0.0/24/default"
        result = await client.ipam.network.next_available_ip(ref, num=1)
        print(result["ips"])

        # Create an A record
        rec = await client.dns.record_a.create({
            "name": "web01.example.com",
            "view": "default",
            "ipv4addr": "10.10.0.5",
        })
        print(rec._ref)

asyncio.run(main())
```

---

## Feature Highlights

| Feature | Detail |
|---|---|
| **Fully async** | Every network call is `async/await` via `httpx` |
| **Type-safe** | Pydantic v2 models for every resource |
| **Auto-pagination** | `list()` returns an `AsyncPageIterator`; call `.all()` or iterate |
| **Session auth** | Logs in at `__aenter__`, calls `/logout` at `__aexit__` |
| **TLS by default** | `verify=True`; override with `verify=False` or `ca_bundle=` |
| **Built-in retry** | Configurable exponential back-off (`max_retries=3`) |
| **WAPI filters** | `name__like`, `extattr_Site`, `__gte`, `__lte`, `__not` operators |
| **return_fields** | Fine-grained field selection via `return_fields` / `return_fields_plus` |
| **Typed wrappers** | `next_available_ip`, `next_available_network`, `restart_services`, … |
| **Restriction-aware** | Operations WAPI forbids per object type raise `UnsupportedOperationError` before the request |

---

## Domain Table

| Domain | `client.<domain>` | Description |
|---|---|---|
| DNS | `client.dns` | Zones, records (A/AAAA/CNAME/MX/PTR/TXT/HOST/…), views, NS groups, DNSSEC, shared records |
| IPAM | `client.ipam` | Network views, networks, containers, VLAN, addresses, bulk hosts |
| DHCP | `client.dhcp` | Ranges, fixed addresses, options, failover, leases, filters, fingerprints |
| Grid | `client.grid` | Grid config, members, service restart, licensing, upgrades, EA definitions |
| RPZ | `client.rpz` | Response Policy Zones and all RPZ record types |
| Security | `client.security` | Admin users/groups/roles, auth policies, RADIUS/LDAP/TACACS+/SAML, HSM |
| Threat Protection | `client.threatprotection` | TP profiles, rules, rulesets, rule templates, statistics |
| Threat Insight | `client.threatinsight` | Allow-lists, cloud clients, module sets |
| DTC | `client.dtc` | DNS Traffic Control: LBDNs, pools, servers, topology, monitors, records |
| Cloud | `client.cloud` | AWS/Azure/GCP DNS task groups and cloud users |
| Discovery | `client.discovery` | Device discovery, credentials, SDN networks, VRFs, vDiscovery |
| Federated Realms | `client.federatedrealms` | Federated IPAM realms and operations |
| MS Server | `client.microsoftserver` | Microsoft DNS/DHCP server management and AD Sites |
| Smart Folder | `client.smartfolder` | Global and personal smart folders |
| Notification | `client.notification` | REST notification endpoints, templates, and rules |
| ACL | `client.acl` | Named ACLs |
| Misc | `client.misc` | Search, file operations, scheduled tasks, TAXII, DXL, kerberos keys, … |

---

## License

Apache License 2.0 (`Apache-2.0`) - the full text ships as
[LICENSE](https://github.com/Infoblox-PS/ibx-nios-sdk/blob/main/LICENSE) and every
source file carries an SPDX identifier. The licence is permissive: you can build
this SDK into proprietary or differently licensed software, provided you keep the
notices and state any changes you made.

Runtime dependencies are permissive as well: httpx (BSD-3-Clause), pydantic (MIT),
python-dateutil (Apache-2.0/BSD-3-Clause); the `[cli]` extra adds click and
click-option-group (BSD-3-Clause).

## Trademarks

INFOBLOX is a trademark of Infoblox Inc. or its affiliated companies, registered in the
United States and other countries. Infoblox Grid is a trademark of Infoblox Inc. Other
Infoblox product names used here, such as NIOS, are used descriptively to identify the
products this SDK operates against and remain the property of their owner. "WAPI" is
used in its plain sense, as the name of the NIOS Web API.

This notice identifies the marks by jurisdiction rather than attaching a symbol to each
of the several thousand mentions throughout these docs, which the Infoblox trademark
guidelines expressly permit. That guidelines list is non-exhaustive, so absence from it
does not imply a name is unclaimed - but nor does this notice assert rights Infoblox has
not claimed. Usage questions go to <brand@infoblox.com>.

---

## Requirements

- Python 3.11 or later
- `httpx >= 0.27`
- `pydantic >= 2`
- `python-dateutil >= 2.8.2`
- NIOS 9.x grid with WAPI 2.12+ (defaults to `2.14`)

## Installation

```bash
pip install ibx-nios-sdk
```

## Next Steps

- [Getting Started](getting-started.md) - auth, first call, TLS
- [Configuration](configuration.md) - all constructor options and env vars
- [Common Patterns](common-patterns.md) - pagination, filters, error handling
- [User Guide](user-guide/dns.md) - per-domain reference
