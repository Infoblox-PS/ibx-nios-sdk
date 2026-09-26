# Cloud & Discovery

This page covers two domains:

- **Cloud** (`client.cloud`) - 7 resources: AWS/Azure/GCP DNS task groups and cloud users
- **Discovery** (`client.discovery`) - 14 resources: device discovery, credential groups, SDN networks, VRFs, vDiscovery

---

## Cloud

The Cloud domain manages cloud provider DNS zone synchronization. NIOS can mirror hosted DNS zones
from AWS Route 53, Azure DNS, and Google Cloud DNS into the NIOS Grid (and optionally push NIOS
records back to the cloud providers).

### Task groups

Each cloud provider has its own task-group resource type:

| Resource | Provider |
|---|---|
| `awsrte53taskgroup` | Amazon Route 53 |
| `azurednstaskgroup` | Microsoft Azure DNS |
| `gcpdnstaskgroup` | Google Cloud DNS |

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # List all AWS Route 53 sync tasks
        async for task in client.cloud.awsrte53taskgroup.list():
            print(task.name, task.comment)

        # Create an Azure DNS task group
        az_task = await client.cloud.azurednstaskgroup.create({
            "name": "prod-azure-dns",
            "tenant_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "client_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "comment": "Azure DNS sync for production subscription",
        })
        print(az_task._ref)

        # GCP DNS task group
        gcp_tasks = await client.cloud.gcpdnstaskgroup.list().all()

asyncio.run(main())
```

### Cloud users

Cloud users hold the authentication credentials for cloud provider APIs:

| Resource | Provider |
|---|---|
| `awsuser` | AWS IAM credentials |
| `azureuser` | Azure service principal |
| `gcpuser` | GCP service account |

```python
async with NiosClient() as client:
    aws_users = await client.cloud.awsuser.list().all()
    az_users = await client.cloud.azureuser.list().all()
    gcp_users = await client.cloud.gcpuser.list().all()
```

### Multi-region support

```python
async with NiosClient() as client:
    # AWS multi-region task configuration
    regions = await client.cloud.multiregions.list().all()
    for r in regions:
        print(r.regions)
```

---

## Discovery

The Discovery domain manages NIOS's network device discovery (using Cisco Discovery Protocol,
LLDP, SNMP, and active scanning), plus vDiscovery (VMware/cloud inventory sync).

### Grid and member discovery properties

```python
async with NiosClient() as client:
    # Grid-wide discovery settings
    grid_disc = await client.discovery.gridproperties.list().all()

    # Per-member discovery settings
    member_disc = await client.discovery.memberproperties.list().all()
    for m in member_disc:
        print(m.member, m.discovery_member)
```

### Device discovery

Discovered devices are represented as read-only objects:

```python
async with NiosClient() as client:
    # All discovered devices
    async for device in client.discovery.device.list():
        print(device.ip_address, device.os_version, device.vendor)

    # Filter by network
    devices = await client.discovery.device.list(
        network="10.10.0.0/24",
    ).all()

    # Device components (interfaces, modules)
    components = await client.discovery.devicecomponent.list().all()

    # Device interfaces
    ifaces = await client.discovery.deviceinterface.list().all()

    # Device neighbors (CDP/LLDP topology)
    neighbors = await client.discovery.deviceneighbor.list().all()

    # Support bundles (device-specific diagnostic data)
    bundles = await client.discovery.devicesupportbundle.list().all()
```

### Credential groups

Credential groups store SNMP/SSH credentials used during device discovery:

```python
async with NiosClient() as client:
    creds = await client.discovery.credentialgroup.list().all()
    for c in creds:
        print(c.name, c.comment)

    # Create a credential group
    cg = await client.discovery.credentialgroup.create({
        "name": "snmpv3-prod",
        "comment": "SNMPv3 credentials for production network",
    })
```

### Discovery status and diagnostics

```python
async with NiosClient() as client:
    # Current discovery status
    status = await client.discovery.status.list().all()

    # Diagnostic tasks (on-demand discovery runs)
    diag = await client.discovery.diagnostictask.list().all()

    # SDN networks (OpenDaylight, ACI integration)
    sdn_nets = await client.discovery.sdnnetwork.list().all()

    # VRF objects
    vrfs = await client.discovery.vrf.list().all()
    for vrf in vrfs:
        print(vrf.name, vrf.device)
```

### vDiscovery

vDiscovery syncs VMware vCenter / cloud inventory into NIOS:

```python
async with NiosClient() as client:
    # vDiscovery task
    vtasks = await client.discovery.vdiscoverytask.list().all()
    for vt in vtasks:
        print(vt.name, vt.state)

    # Create a vDiscovery task for vCenter
    vt = await client.discovery.vdiscoverytask.create({
        "name": "vcenter-prod",
        "fqdn_or_ip": "vcenter.corp.example.com",
        "comment": "Production vCenter inventory sync",
    })

    # The `discovery` object is function-only - WAPI restricts read on it, so
    # call its functions rather than listing it.
    found = await client.discovery.discovery.call_function(
        None, "get_job_devices", task="discoverytask/ZG5z..."
    )
    print(found["devices"])
```
