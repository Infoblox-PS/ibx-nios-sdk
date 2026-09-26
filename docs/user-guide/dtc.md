# DTC - DNS Traffic Control

The `dtc` domain covers **22 resources**: the DTC core object, Load-Balanced Domain Names (LBDNs),
pools, servers, topology objects and rules, six monitor types, five DTC record types, certificates,
and all-records.

Access via `client.dtc`.

---

## Overview

DNS Traffic Control (DTC) provides intelligent DNS-based load balancing and failover. The
object hierarchy is:

```text
LBDN (Load-Balanced Domain Name)
  └── Pool (group of servers with a load-balancing method)
        └── Server (individual endpoint)
              └── Monitor (health check: HTTP, ICMP, TCP, SIP, SNMP, PDP)
```

---

## DTC core and topology

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # The `dtc` object itself is function-only: WAPI restricts read/create/
        # update/delete on it, so it is reached through call_function().
        state = await client.dtc.dtc.call_function(
            None, "dtc_get_object_grid_state", dtc_object="dtc:lbdn/ZG5z..."
        )
        print(state["enabled_on"], state["disabled_on"])

        # Topology objects (geographic / subnet-based routing)
        topologies = await client.dtc.topology.list().all()
        for topo in topologies:
            print(topo.name, topo.comment)

        # Topology labels and rules
        labels = await client.dtc.topology_label.list().all()
        rules = await client.dtc.topology_rule.list().all()

asyncio.run(main())
```

---

## Servers

DTC servers represent individual backend endpoints.

```python
async with NiosClient() as client:
    # Create a server
    server = await client.dtc.server.create({
        "name": "web-server-01",
        "host": "10.10.0.5",
        "comment": "Primary web server",
    })
    print(server._ref)

    # List servers
    servers = await client.dtc.server.list().all()
    for s in servers:
        print(s.name, s.host)
```

---

## Monitors

Monitors perform health checks on DTC servers. Six types are available:

| Resource | Protocol | Description |
|---|---|---|
| `dtc_monitor_http` | HTTP/HTTPS | HTTP GET/POST health check |
| `dtc_monitor_icmp` | ICMP | Ping-based availability check |
| `dtc_monitor_tcp` | TCP | Port reachability check |
| `dtc_monitor_sip` | SIP | VoIP endpoint health check |
| `dtc_monitor_snmp` | SNMP | SNMP OID value check |
| `dtc_monitor_pdp` | PDP | Policy Decision Point check |
| `dtc_monitor` | (base) | Generic monitor query |

```python
async with NiosClient() as client:
    # HTTP monitor
    http_mon = await client.dtc.monitor_http.create({
        "name": "http-check-80",
        "port": 80,
        "request": "GET / HTTP/1.1\r\nHost: example.com\r\n\r\n",
        "result": "STATUS_200",
        "comment": "Web server health check",
    })

    # ICMP monitor
    icmp_mon = await client.dtc.monitor_icmp.create({
        "name": "ping-check",
        "comment": "Basic ICMP ping",
    })

    # TCP monitor
    tcp_mon = await client.dtc.monitor_tcp.create({
        "name": "tcp-443",
        "port": 443,
        "comment": "HTTPS port reachability",
    })
```

---

## Pools

Pools group servers and define the load-balancing algorithm.

```python
async with NiosClient() as client:
    # Create a pool
    pool = await client.dtc.pool.create({
        "name": "web-pool",
        "lb_preferred_method": "ROUND_ROBIN",
        "servers": [
            {"server": server._ref, "ratio": 1},
        ],
        "monitors": [http_mon._ref],
        "comment": "Web server pool",
    })

    # List pools
    pools = await client.dtc.pool.list().all()
    for p in pools:
        print(p.name, p.lb_preferred_method)
```

---

## LBDNs (Load-Balanced Domain Names)

An LBDN is the DNS name that DTC manages. When a client queries the LBDN name, DTC selects
the best pool/server and returns an appropriate answer.

```python
async with NiosClient() as client:
    # Create an LBDN
    lbdn = await client.dtc.lbdn.create({
        "name": "www",
        "zone": "example.com",
        "lb_method": "TOPOLOGY",
        "topology": topology._ref,
        "pools": [{"pool": pool._ref, "ratio": 1}],
        "comment": "Website LBDN",
        "types": ["A"],
        "persistence": 0,
    })
    print(lbdn._ref)

    # List LBDNs
    lbdns = await client.dtc.lbdn.list().all()
```

---

## DTC records

DTC record objects represent the DNS responses that DTC returns:

| Resource | DNS type |
|---|---|
| `dtc_record_a` | A |
| `dtc_record_aaaa` | AAAA |
| `dtc_record_cname` | CNAME |
| `dtc_record_naptr` | NAPTR |
| `dtc_record_srv` | SRV |

```python
async with NiosClient() as client:
    # Query all DTC records
    all_dtc_recs = await client.dtc.allrecords.list().all()
    for rec in all_dtc_recs:
        print(rec.name, rec.type)
```

---

## DTC certificates

```python
async with NiosClient() as client:
    certs = await client.dtc.certificate.list().all()
    for cert in certs:
        print(cert.certificate, cert.comment)
```
