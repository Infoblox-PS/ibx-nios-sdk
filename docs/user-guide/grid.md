# Grid

The `grid` domain covers **45 resources**: the Grid core object, DNS/DHCP/Threat grid-wide
properties, Cloud API, service restart workflow, Member objects and per-member sub-properties
(DNS, DHCP, Threat Insight, Threat Protection, Parental Control, File Distribution, DFP,
Cloud sync), Mastergrid, licensing, upgrade/distribution scheduling, extensible attribute
definitions, NAT groups, captive portal, and X.509 certificates.

Access via `client.grid`.

---

## Grid core object

The Grid object is a singleton - there is exactly one per NIOS deployment.

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # The grid singleton
        grid_list = await client.grid.grid.list().all()
        grid = grid_list[0]
        print(grid.name, grid._ref)

        # Get grid DNS properties
        dns_props = await client.grid.grid_dns.list().all()

        # Grid-wide DHCP properties - see "Grid-wide and per-member DHCP properties" below
        dhcp_props = await client.grid.grid_dhcpproperties.list().all()

asyncio.run(main())
```

---

## Service restart

NIOS requires explicit service restarts after configuration changes to DNS or DHCP.

### Restart all grid services (typed wrapper)

```python
async with NiosClient() as client:
    grid_list = await client.grid.grid.list().all()
    grid_ref = grid_list[0]._ref

    result = await client.grid.grid.restart_services(
        grid_ref,
        service="ALL",
        mode="GROUPED",
    )
    print(result)
```

### Restart services on a specific member (typed wrapper)

```python
async with NiosClient() as client:
    member = await client.grid.member.find_one(host_name="ns1.example.com")
    if member:
        result = await client.grid.member.restart_services(
            member._ref,
            service="DNS",
            mode="SEQUENTIAL",
        )
```

### Restart via service restart group (typed wrapper)

```python
async with NiosClient() as client:
    groups = await client.grid.grid_servicerestart_group.list().all()
    for grp in groups:
        await client.grid.grid_servicerestart_group.restart_services(grp._ref)
```

---

## Members

Grid members represent individual NIOS appliances (physical or virtual).

```python
async with NiosClient() as client:
    # List all members
    async for member in client.grid.member.list():
        print(member.host_name, member.platform, member.node_info)

    # Get a member by hostname
    member = await client.grid.member.find_one(host_name="ns1.example.com")

    # Per-member DNS properties
    dns_cfg = await client.grid.member_dns.find_one(host_name="ns1.example.com")

    # Per-member DHCP properties
    dhcp_cfg = await client.grid.member_dhcpproperties.find_one(host_name="ns1.example.com")

    # Per-member Threat Insight config
    ti_cfg = await client.grid.member_threatinsight.find_one(host_name="ns1.example.com")

    # Per-member Threat Protection config
    tp_cfg = await client.grid.member_threatprotection.find_one(host_name="ns1.example.com")
```

---

## Grid-wide and per-member DHCP properties

`grid_dhcpproperties` is a singleton holding the DHCP configuration that applies to the
whole grid - global DHCP options, lease defaults, DDNS behaviour, and custom options.
`member_dhcpproperties` holds the same settings scoped to a single member, overriding the
grid-wide defaults where set.

```python
async with NiosClient() as client:
    # Grid-wide DHCP properties (singleton)
    grid_dhcp_list = await client.grid.grid_dhcpproperties.list().all()
    grid_dhcp = grid_dhcp_list[0]
    print(grid_dhcp.lease_scavenge_time, grid_dhcp.disable_all_nac_filters)

    # Update a grid-wide default (e.g. enable DDNS generation)
    await client.grid.grid_dhcpproperties.update(
        grid_dhcp._ref,
        {"enable_ddns": True, "ddns_generate_hostname": True},
    )

    # Per-member DHCP overrides
    member_dhcp = await client.grid.member_dhcpproperties.find_one(
        host_name="ns1.example.com"
    )
    if member_dhcp:
        # Override lease retention on this member only
        await client.grid.member_dhcpproperties.update(
            member_dhcp._ref,
            {"lease_scavenge_time": 86400},
        )

    # Similarly, member_dns holds per-member DNS overrides; pair the two when
    # provisioning a brand-new member to set its full service baseline.
```

!!! tip
    Changes to DHCP properties require a service restart on affected members. Pair property
    updates with `client.grid.member.restart_services(ref, service="DHCP")` or the
    equivalent grid-wide restart.

---

## Cloud API

```python
async with NiosClient() as client:
    # Cloud API tenants
    tenants = await client.grid.grid_cloudapi_tenant.list().all()
    for t in tenants:
        print(t.id, t.name)

    # Cloud VMs
    vms = await client.grid.grid_cloudapi_vm.list().all()

    # Cloud API statistics
    stats = await client.grid.grid_cloudapi_cloudstatistics.list().all()
```

---

## Extensible attribute definitions

EA definitions configure the custom metadata keys available on NIOS objects.

```python
async with NiosClient() as client:
    # List all EA definitions
    ea_defs = await client.grid.extensibleattributedef.list().all()
    for ea in ea_defs:
        print(ea.name, ea.type, ea.comment)

    # Create a new EA definition
    new_ea = await client.grid.extensibleattributedef.create({
        "name": "CostCenter",
        "type": "STRING",
        "comment": "Finance cost center code",
        "flags": "CR",
    })

    # Set EA values on a network (using set_extattrs helper)
    ref = "network/ZG5z.../10.0.0.0/24/default"
    await client.ipam.network.set_extattrs(ref, CostCenter="CC-1234")
```

---

## Licensing

```python
async with NiosClient() as client:
    # Grid-wide license summary
    pool = await client.grid.grid_license_pool.list().all()

    # All active licenses
    licenses = await client.grid.license_gridwide.list().all()
    for lic in licenses:
        print(lic.type, lic.expiration_status)

    # Per-member licenses
    member_lics = await client.grid.member_license.list().all()
```

---

## Upgrade and distribution

```python
async with NiosClient() as client:
    # Upgrade groups
    groups = await client.grid.upgradegroup.list().all()

    # Distribution schedules
    schedules = await client.grid.distributionschedule.list().all()

    # Upgrade status
    status = await client.grid.upgradestatus.list().all()
```

---

## NAT groups and captive portal

```python
async with NiosClient() as client:
    nat_groups = await client.grid.natgroup.list().all()
    captive = await client.grid.captiveportal.list().all()
```

---

## Mastergrid

```python
async with NiosClient() as client:
    mg = await client.grid.mastergrid.list().all()
    if mg:
        print(mg[0].address, mg[0].connection_timestamp)
```

---

## X.509 certificates

```python
async with NiosClient() as client:
    certs = await client.grid.grid_x509certificate.list().all()
    for cert in certs:
        print(cert.issuer, cert.valid_not_before, cert.valid_not_after)
```
