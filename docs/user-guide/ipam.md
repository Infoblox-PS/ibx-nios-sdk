# IPAM

The `ipam` domain covers **20 resources**: network views, IPv4/IPv6 networks and containers,
templates, address objects, VLAN infrastructure, bulk hosts, discovery tasks, super hosts,
and IPAM statistics.

Access via `client.ipam`.

---

## Network views

A network view is the top-level container for all networks. Most NIOS grids have a single
`default` view, but multi-tenancy deployments use many views.

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # List all network views
        views = await client.ipam.networkview.list().all()
        for v in views:
            print(v.name, v.comment)

        # Create a new network view
        tenant_view = await client.ipam.networkview.create({
            "name": "tenant-a",
            "comment": "Tenant A network view",
        })
        print(tenant_view._ref)

asyncio.run(main())
```

---

## Networks

### List and filter networks

```python
async with NiosClient() as client:
    # All networks in the default view
    async for net in client.ipam.network.list(network_view="default"):
        print(net.network, net.comment)

    # Filter by EA
    london_nets = await client.ipam.network.list(
        network_view="default",
        extattr_Site="London",
    ).all()
```

### Create and update

```python
async with NiosClient() as client:
    net = await client.ipam.network.create({
        "network": "10.20.0.0/24",
        "network_view": "default",
        "comment": "Prod subnet",
        "extattrs": {"Site": {"value": "London"}},
    })
    await client.ipam.network.update(net._ref, {"comment": "Production subnet - London"})
```

### Next available IP (typed wrapper)

```python
async with NiosClient() as client:
    ref = "network/ZG5z.../10.20.0.0/24/default"
    # Request 3 consecutive IPs
    result = await client.ipam.network.next_available_ip(ref, num=3)
    print(result["ips"])  # ["10.20.0.2", "10.20.0.3", "10.20.0.4"]

    # Exclude specific IPs from allocation
    result = await client.ipam.network.next_available_ip(
        ref,
        num=1,
        exclude=["10.20.0.2", "10.20.0.3"],
    )
```

---

## Network containers

### Next available network (typed wrapper)

```python
async with NiosClient() as client:
    container_ref = "networkcontainer/ZG5z.../10.0.0.0/8/default"

    # Allocate a /24 from the container
    result = await client.ipam.networkcontainer.next_available_network(
        container_ref,
        cidr=24,
        num=1,
    )
    print(result["networks"])  # ["10.0.1.0/24"]
```

---

## IPv6 networks

```python
async with NiosClient() as client:
    # Create an IPv6 network
    net6 = await client.ipam.ipv6network.create({
        "network": "2001:db8::/48",
        "network_view": "default",
        "comment": "IPv6 prod",
    })

    # Next available IPv6 address
    result = await client.ipam.ipv6network.next_available_ip(net6._ref, num=1)
    print(result["ips"])

    # Next available IPv6 network from a container
    container6_ref = "ipv6networkcontainer/ZG5z.../2001:db8::/32/default"
    result = await client.ipam.ipv6networkcontainer.next_available_network(
        container6_ref,
        cidr=64,
    )
```

---

## IP address objects

IP address objects (ipv4address / ipv6address) are read-only views of allocated addresses.
They reflect what NIOS knows about each IP (hostname, MAC, lease status, usage type).

```python
async with NiosClient() as client:
    # Find all addresses in a subnet
    addrs = await client.ipam.ipv4address.list(
        network="10.20.0.0/24",
        network_view="default",
        status="USED",
    ).all()
    for a in addrs:
        print(a.ip_address, a.names, a.types)

    # Look up a specific IP
    addr = await client.ipam.ipv4address.find_one(
        ip_address="10.20.0.5",
        network_view="default",
    )
```

---

## VLAN infrastructure

| Resource | Description |
|---|---|
| `vlanview` | Top-level VLAN view (container for ranges) |
| `vlanrange` | VLAN ID range within a view |
| `vlan` | Individual VLAN object |

```python
async with NiosClient() as client:
    # List all VLANs
    vlans = await client.ipam.vlan.list().all()
    for v in vlans:
        print(v.id, v.name)

    # Create a VLAN view and range
    vview = await client.ipam.vlanview.create({
        "name": "corp-vlans",
        "start_vlan_id": 100,
        "end_vlan_id": 999,
    })
```

---

## Network templates

```python
async with NiosClient() as client:
    templates = await client.ipam.networktemplate.list().all()
    ipv6_templates = await client.ipam.ipv6networktemplate.list().all()
```

---

## Bulk hosts and super hosts

```python
async with NiosClient() as client:
    # Bulk host name template
    templates = await client.ipam.bulkhostnametemplate.list().all()

    # Bulk host object
    bh = await client.ipam.bulkhost.create({
        "name_template": "host-{n}",
        "start_addr": "10.0.0.100",
        "num_hosts": 10,
        "network_view": "default",
    })
```

---

## IPAM statistics

```python
async with NiosClient() as client:
    stats = await client.ipam.ipam_statistics.list(network="10.20.0.0/24").all()
    for s in stats:
        print(s.network, s.utilization)
```
