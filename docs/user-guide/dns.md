# DNS

The `dns` domain covers **52 resources**: authoritative/forward/delegated/stub/RPZ zones, all DNS record types,
DNS views, NS group families, shared records, DNSSEC records, and record name policies.

Access via `client.dns`.

---

## Zone management

### Authoritative zones (`zone_auth`)

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # List all forward zones in the default view
        async for zone in client.dns.zone_auth.list(view="default", zone_format="FORWARD"):
            print(zone.fqdn, zone.comment)

        # Find one zone
        zone = await client.dns.zone_auth.find_one(fqdn="example.com", view="default")

        # Create an authoritative zone
        new_zone = await client.dns.zone_auth.create({
            "fqdn": "new.example.com",
            "view": "default",
            "comment": "Created via SDK",
        })
        print(new_zone._ref)

        # Update a zone
        await client.dns.zone_auth.update(new_zone._ref, {"comment": "Updated"})

        # Delete a zone
        await client.dns.zone_auth.delete(new_zone._ref)

asyncio.run(main())
```

### Typed wrappers for `zone_auth`

**Copy records between zones:**

```python
async with NiosClient() as client:
    target_ref = "zone_auth/ZG5z.../new.example.com/default"
    result = await client.dns.zone_auth.copy_zone_records(
        target_ref,
        source_zone="example.com",
        view="default",
        copy_all_records=True,
    )
    print(result)
```

**Lock / unlock a zone for editing:**

```python
async with NiosClient() as client:
    ref = "zone_auth/ZG5z.../example.com/default"
    await client.dns.zone_auth.lock_unlock_zone(ref, lock=True)
    # ... make changes ...
    await client.dns.zone_auth.lock_unlock_zone(ref, lock=False)
```

### Forward, delegated, and stub zones

```python
async with NiosClient() as client:
    # Forward zone
    fwd = await client.dns.zone_forward.create({
        "fqdn": "forward.example.com",
        "view": "default",
        "forward_to": [{"address": "8.8.8.8", "name": "google"}],
    })

    # Delegated zone
    dlg = await client.dns.zone_delegated.create({
        "fqdn": "sub.example.com",
        "view": "default",
        "delegate_to": [{"address": "10.0.0.53", "name": "sub-ns"}],
    })
```

---

## DNS Records

### A records (`record_a`)

```python
async with NiosClient() as client:
    # Create
    rec = await client.dns.record_a.create({
        "name": "web01.example.com",
        "view": "default",
        "ipv4addr": "10.10.0.5",
        "ttl": 300,
        "comment": "Web server",
    })

    # List by name pattern
    records = await client.dns.record_a.list(name__like="web").all()

    # Update IP
    await client.dns.record_a.update(rec._ref, {"ipv4addr": "10.10.0.6"})

    # Delete
    await client.dns.record_a.delete(rec._ref)
```

### Host records (`record_host`)

Host records are unique to NIOS - they combine A/AAAA records with optional DHCP fixed-address
assignments in a single object.

```python
async with NiosClient() as client:
    host = await client.dns.record_host.create({
        "name": "server01.example.com",
        "view": "default",
        "ipv4addrs": [{"ipv4addr": "10.10.0.10"}],
        "comment": "Multi-purpose host record",
    })
    print(host._ref)
```

### Other record types

| Resource | `client.dns.<resource>` | WAPI type |
|---|---|---|
| AAAA record | `record_aaaa` | `record:aaaa` |
| CNAME record | `record_cname` | `record:cname` |
| MX record | `record_mx` | `record:mx` |
| TXT record | `record_txt` | `record:txt` |
| PTR record | `record_ptr` | `record:ptr` |
| NS record | `record_ns` | `record:ns` |
| SRV record | `record_srv` | `record:srv` |
| NAPTR record | `record_naptr` | `record:naptr` |
| CAA record | `record_caa` | `record:caa` |
| DNAME record | `record_dname` | `record:dname` |
| HTTPS record | `record_https` | `record:https` |
| SVCB record | `record_svcb` | `record:svcb` |
| TLSA record | `record_tlsa` | `record:tlsa` |
| DHCID record | `record_dhcid` | `record:dhcid` |
| Host IPv4 addr | `record_host_ipv4addr` | `record:host_ipv4addr` |
| Host IPv6 addr | `record_host_ipv6addr` | `record:host_ipv6addr` |
| Alias record | `record_alias` | `record:alias` |
| Unknown record | `record_unknown` | `record:unknown` |

---

## DNSSEC records

DNSSEC record types are read-only (managed by the Grid):

| Resource | WAPI type |
|---|---|
| `record_dnskey` | `record:dnskey` |
| `record_ds` | `record:ds` |
| `record_nsec` | `record:nsec` |
| `record_nsec3` | `record:nsec3` |
| `record_nsec3param` | `record:nsec3param` |
| `record_rrsig` | `record:rrsig` |

---

## DNS Views

```python
async with NiosClient() as client:
    # List all views
    views = await client.dns.view.list().all()

    # Create a split-horizon view
    ext_view = await client.dns.view.create({
        "name": "external",
        "comment": "External-facing DNS view",
    })

    # Return extra fields
    view = await client.dns.view.find_one(
        name="default",
        return_fields_plus=["match_clients", "match_destinations"],
    )
```

---

## NS groups

| Resource | Description |
|---|---|
| `nsgroup` | Primary NS group |
| `nsgroup_delegation` | Delegation NS group |
| `nsgroup_forwardingmember` | Forwarding member NS group |
| `nsgroup_forwardstubserver` | Forward/stub server NS group |
| `nsgroup_stubmember` | Stub member NS group |
| `allnsgroup` | Cross-type NS group query |

```python
async with NiosClient() as client:
    groups = await client.dns.nsgroup.list().all()
    for g in groups:
        print(g.name)
```

---

## Shared records

Shared record groups allow a single record to be shared across multiple views.

| Resource | WAPI type |
|---|---|
| `sharedrecordgroup` | `sharedrecordgroup` |
| `sharedrecord_a` | `sharedrecord:a` |
| `sharedrecord_aaaa` | `sharedrecord:aaaa` |
| `sharedrecord_cname` | `sharedrecord:cname` |
| `sharedrecord_mx` | `sharedrecord:mx` |
| `sharedrecord_srv` | `sharedrecord:srv` |
| `sharedrecord_txt` | `sharedrecord:txt` |

---

## Record name policies and all-records

```python
async with NiosClient() as client:
    # Query all record types in one call
    all_recs = await client.dns.allrecords.list(name__like="web").all()

    # Record name policies
    policies = await client.dns.recordnamepolicy.list().all()
```

---

## DDNS principal cluster groups

```python
async with NiosClient() as client:
    # DDNS principal cluster group
    groups = await client.dns.ddns_principalcluster_group.list().all()
```
