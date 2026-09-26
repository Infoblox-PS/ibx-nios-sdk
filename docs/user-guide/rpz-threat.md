# RPZ & Threat

This page covers three domains:

- **RPZ** (`client.rpz`) - 17 resources: Response Policy Zone zones and all RPZ record types
- **Threat Protection** (`client.threatprotection`) - 8 resources: profiles, rules, rulesets, templates, statistics
- **Threat Insight** (`client.threatinsight`) - 4 resources: allow-lists, cloud clients, module sets

---

## Response Policy Zones (RPZ)

RPZ zones are DNS firewall zones that intercept queries matching policy rules and return
overridden responses. All RPZ zones live under the `rpz` domain.

### Creating an RPZ zone

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # Create a new RPZ zone (NIOS uses zone_auth with rpz=True internally)
        zone = await client.dns.zone_rp.create({
            "fqdn": "rpz.block.example.com",
            "view": "default",
            "comment": "Malware blocking RPZ",
            "rpz_policy": "NXDOMAIN",
        })
        print(zone._ref)

asyncio.run(main())
```

### Querying RPZ zones and records

```python
async with NiosClient() as client:
    # All RPZ zones
    async for zone in client.dns.zone_rp.list(view="default"):
        print(zone.fqdn, zone.rpz_policy)

    # All RPZ records in one query
    all_rpz = await client.rpz.allrpzrecords.list().all()
    for rec in all_rpz:
        print(rec.name, rec.rpz_rule)
```

### RPZ record types

Each RPZ record type encodes a different interception policy:

| Resource | WAPI type | Policy |
|---|---|---|
| `record_rpz_a` | `record:rpz:a` | Return a specific A record |
| `record_rpz_aaaa` | `record:rpz:aaaa` | Return a specific AAAA record |
| `record_rpz_cname` | `record:rpz:cname` | PASSTHRU / NXDOMAIN / wildcard |
| `record_rpz_mx` | `record:rpz:mx` | Override with MX |
| `record_rpz_naptr` | `record:rpz:naptr` | Override with NAPTR |
| `record_rpz_ptr` | `record:rpz:ptr` | Override PTR queries |
| `record_rpz_srv` | `record:rpz:srv` | Override SRV |
| `record_rpz_txt` | `record:rpz:txt` | Override with TXT |
| `record_rpz_https` | `record:rpz:https` | Override HTTPS queries |
| `record_rpz_svcb` | `record:rpz:svcb` | Override SVCB queries |
| `record_rpz_a_ipaddress` | `record:rpz:a:ipaddress` | IP trigger → A response |
| `record_rpz_aaaa_ipaddress` | `record:rpz:aaaa:ipaddress` | IP trigger → AAAA response |
| `record_rpz_cname_ipaddress` | `record:rpz:cname:ipaddress` | IP trigger → CNAME |
| `record_rpz_cname_ipaddressdn` | `record:rpz:cname:ipaddressdn` | IP-domain trigger → CNAME |
| `record_rpz_cname_clientipaddress` | `record:rpz:cname:clientipaddress` | Client IP trigger |
| `record_rpz_cname_clientipaddressdn` | `record:rpz:cname:clientipaddressdn` | Client IP-domain trigger |

```python
async with NiosClient() as client:
    # Block a domain (NXDOMAIN via CNAME to '.')
    block = await client.rpz.record_rpz_cname.create({
        "name": "malware.example.com.rpz.block.example.com",
        "view": "default",
        "canonical": ".",
        "comment": "Block malware.example.com",
    })

    # Return a walled-garden A record for phishing domain
    walled = await client.rpz.record_rpz_a.create({
        "name": "phishing.example.com.rpz.block.example.com",
        "view": "default",
        "ipv4addr": "198.51.100.1",
        "comment": "Redirect to walled garden",
    })

    # IP-based trigger: block any response containing this IP
    ip_trigger = await client.rpz.record_rpz_a_ipaddress.create({
        "name": "198.51.100.200.rpz-ip.rpz.block.example.com",
        "view": "default",
        "ipv4addr": "198.51.100.200",
    })
```

---

## Threat Protection

Threat Protection (IPS-style) inspects DNS traffic and drops or logs queries matching threat rules.

### Profiles

A Threat Protection profile groups rules applied to one or more members.

```python
async with NiosClient() as client:
    # List profiles
    profiles = await client.threatprotection.profile.list().all()
    for p in profiles:
        print(p.name, p.comment)

    # Find a profile
    profile = await client.threatprotection.profile.find_one(name="default")
    print(profile._ref)
```

### Rules and rule sets

```python
async with NiosClient() as client:
    # List all available rules
    rules = await client.threatprotection.rule.list().all()

    # List rulesets (bundles of rules, e.g. a specific threat feed version)
    rulesets = await client.threatprotection.ruleset.list().all()
    for rs in rulesets:
        print(rs.version, rs.status)

    # Rule templates (read-only, provided by Infoblox)
    templates = await client.threatprotection.ruletemplate.list().all()

    # Per-profile rules (rule overrides within a profile)
    profile_rules = await client.threatprotection.profile_rule.list(
        profile="default"
    ).all()
```

### Statistics

```python
async with NiosClient() as client:
    # Grid-wide TP statistics
    stats = await client.threatprotection.statistics.list().all()
    for s in stats:
        print(s.member, s.type, s.stat_infos)

    # Also available: per-member grid_rule overrides
    grid_rules = await client.threatprotection.grid_rule.list().all()
```

---

## Threat Insight

Threat Insight provides behavioral detection of DNS-based threats (data exfiltration, DGA, etc.).

```python
async with NiosClient() as client:
    # Allow-list: domains/IPs excluded from Threat Insight analysis
    allowlist = await client.threatinsight.allowlist.list().all()
    for entry in allowlist:
        print(entry.address, entry.comment)

    # Add to allow-list
    new_entry = await client.threatinsight.allowlist.create({
        "address": "trusted-analytics.example.com",
        "comment": "Internal analytics - exclude from TI",
    })

    # Insight allow-list (separate from the main allow-list)
    insight_al = await client.threatinsight.insight_allowlist.list().all()

    # Cloud client configuration
    cloud_client = await client.threatinsight.cloudclient.list().all()
    if cloud_client:
        print(cloud_client[0].enable)

    # Module sets (TI detection modules and versions)
    modules = await client.threatinsight.moduleset.list().all()
    for m in modules:
        print(m.version, m.comment)
```
