# DHCP

The `dhcp` domain covers **27 resources**: DHCP ranges and templates, fixed addresses, shared
networks, six filter types, option definitions/spaces, failover associations, leases, fingerprints,
MAC filter addresses, roaming hosts, and DHCP statistics.

Access via `client.dhcp`.

---

## DHCP Ranges

### List and filter ranges

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # All DHCP ranges in the default network view
        async for r in client.dhcp.range.list(network_view="default"):
            print(r.start_addr, "–", r.end_addr, r.comment)

        # Filter by network
        ranges = await client.dhcp.range.list(
            network="10.10.0.0/24",
            network_view="default",
        ).all()

asyncio.run(main())
```

### Create a range

```python
async with NiosClient() as client:
    r = await client.dhcp.range.create({
        "start_addr": "10.10.0.100",
        "end_addr": "10.10.0.200",
        "network_view": "default",
        "comment": "Dynamic pool",
    })
    print(r._ref)
```

### Next available IP in a range (typed wrapper)

```python
async with NiosClient() as client:
    ref = "range/ZG5z.../10.10.0.100/10.10.0.200/default"
    result = await client.dhcp.range.next_available_ip(ref, num=1)
    print(result["ips"])

    # IPv6 range
    ipv6_ref = "ipv6range/ZG5z.../..."
    result6 = await client.dhcp.ipv6range.next_available_ip(ipv6_ref, num=1)
```

---

## Fixed addresses

A fixed address (static DHCP reservation) maps a MAC address to a specific IP.

```python
async with NiosClient() as client:
    # Create a fixed address
    fa = await client.dhcp.fixedaddress.create({
        "ipv4addr": "10.10.0.50",
        "mac": "aa:bb:cc:dd:ee:ff",
        "network_view": "default",
        "comment": "Printer - floor 3",
    })
    print(fa._ref)

    # Find by MAC
    existing = await client.dhcp.fixedaddress.find_one(
        mac="aa:bb:cc:dd:ee:ff",
        network_view="default",
    )

    # IPv6 fixed address
    fa6 = await client.dhcp.ipv6fixedaddress.create({
        "ipv6addr": "2001:db8::50",
        "duid": "00:03:00:01:aa:bb:cc:dd:ee:ff",
        "network_view": "default",
    })
```

---

## Shared networks

```python
async with NiosClient() as client:
    sn = await client.dhcp.sharednetwork.create({
        "name": "office-shared",
        "network_view": "default",
        "comment": "Shared network for office VLANs",
    })

    ipv6_sn = await client.dhcp.ipv6sharednetwork.create({
        "name": "office-shared-v6",
        "network_view": "default",
    })
```

---

## DHCP filters

NIOS supports six filter types for conditional option delivery:

| Resource | Filter type | Description |
|---|---|---|
| `filtermac` | MAC address filter | Match by hardware address |
| `filteroption` | Option filter | Match by DHCP option value |
| `filternac` | NAC filter | Network access control filter |
| `filterrelayagent` | Relay agent filter | Match by relay agent circuit-id |
| `filterfingerprint` | Fingerprint filter | Match by OS fingerprint |
| `ipv6filteroption` | IPv6 option filter | IPv6 DHCP option filter |

```python
async with NiosClient() as client:
    # MAC filter
    mf = await client.dhcp.filtermac.create({
        "name": "allow-printers",
        "comment": "Only printer MACs",
    })

    # Option filter
    of = await client.dhcp.filteroption.create({
        "name": "windows-clients",
        "option_list": [{"num": 60, "value": "MSFT", "match_type": "substring_match"}],
    })
```

---

## DHCP options

```python
async with NiosClient() as client:
    # Custom option definition
    opt = await client.dhcp.dhcpoptiondefinition.create({
        "name": "my-custom-option",
        "code": 200,
        "type": "STRING",
        "space": "DHCP",
    })

    # List option spaces
    spaces = await client.dhcp.dhcpoptionspace.list().all()
```

---

## Failover associations

```python
async with NiosClient() as client:
    # List failover pairs
    failovers = await client.dhcp.dhcpfailover.list().all()
    for fo in failovers:
        print(fo.name, fo.primary, fo.secondary)

    # Update failover max-response-delay
    await client.dhcp.dhcpfailover.update(
        failovers[0]._ref,
        {"max_response_delay": 60},
    )
```

---

## Leases

Lease objects are read-only (they reflect the DHCP server's current lease table):

```python
async with NiosClient() as client:
    # Active leases in a subnet
    leases = await client.dhcp.lease.list(
        network="10.10.0.0/24",
        network_view="default",
        binding_state="ACTIVE",
    ).all()
    for lease in leases:
        print(lease.address, lease.hardware, lease.client_hostname)
```

---

## Device fingerprinting

```python
async with NiosClient() as client:
    # List fingerprint definitions
    fps = await client.dhcp.fingerprint.list().all()

    # Filter-fingerprint associations
    ffps = await client.dhcp.filterfingerprint.list().all()
```

---

## MAC filter addresses and roaming hosts

```python
async with NiosClient() as client:
    # Add a MAC to a filter
    mfa = await client.dhcp.macfilteraddress.create({
        "filter": "myfiltername",
        "mac": "de:ad:be:ef:00:01",
        "comment": "Test device",
    })

    # Roaming host (follows MAC across networks)
    rh = await client.dhcp.roaminghost.create({
        "mac": "de:ad:be:ef:00:01",
        "name": "laptop-001",
        "network_view": "default",
    })
```

---

## DHCP statistics

```python
async with NiosClient() as client:
    stats = await client.dhcp.dhcp_statistics.list(
        network="10.10.0.0/24",
    ).all()
    for s in stats:
        print(s.network, s.dynamic_hosts, s.static_hosts)
```
