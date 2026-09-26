# Other Domains

This page covers six smaller domains: Federated Realms, Microsoft Server, Smart Folder,
Notification, ACL, and Misc.

---

## Federated Realms (`client.federatedrealms`)

Federated IPAM realms allow NIOS to act as a federated IPAM authority, sharing IP space with
external IPAM systems (such as Infoblox Universal DDI).

**Resources:** `federatedrealms`, `fedipamop`

```python
import asyncio
from ibx_nios_sdk import NiosClient

async def main():
    async with NiosClient() as client:
        # List configured federated realms
        realms = await client.federatedrealms.federatedrealms.list().all()
        for r in realms:
            print(r.realm_name, r.comment)

        # Federated IPAM operations are function-only - WAPI restricts read on
        # `fedipamop`, so call the function instead of listing the object.
        ancestor = await client.federatedrealms.fedipamop.call_function(
            None,
            "get_ancestor_federated_realms",
            object_type="network",
            address="10.0.0.0",
            cidr=8,
            network_view="default",
        )
        print(ancestor["federated_realm_id"])

asyncio.run(main())
```

---

## Microsoft Server (`client.microsoftserver`)

The Microsoft Server domain manages NIOS's integration with Windows DHCP/DNS servers and
Active Directory Sites and Services.

**Resources:** `msserver`, `adsites_domain`, `adsites_site`, `dhcp`, `dns`,
`mssuperscope`

```python
async with NiosClient() as client:
    # List managed Microsoft servers
    ms_servers = await client.microsoftserver.msserver.list().all()
    for s in ms_servers:
        print(s.address, s.login_name, s.comment)

    # AD Sites and Services - domains
    domains = await client.microsoftserver.adsites_domain.list().all()

    # AD Sites
    sites = await client.microsoftserver.adsites_site.list().all()
    for site in sites:
        print(site.name, site.domain)

    # Microsoft DHCP configuration
    ms_dhcp = await client.microsoftserver.dhcp.list().all()

    # Microsoft DNS configuration
    ms_dns = await client.microsoftserver.dns.list().all()

    # Microsoft superscopes (aggregates of DHCP scopes)
    superscopes = await client.microsoftserver.mssuperscope.list().all()
```

---

## Smart Folder (`client.smartfolder`)

Smart Folders provide saved, filter-based views of NIOS objects - similar to saved searches.
Global smart folders are shared across all admins; personal smart folders are per-user.

**Resources:** `global_`, `personal`, `children`

```python
async with NiosClient() as client:
    # Global smart folders (shared)
    global_folders = await client.smartfolder.global_.list().all()
    for f in global_folders:
        print(f.name, f.comment)

    # Personal smart folders
    personal_folders = await client.smartfolder.personal.list().all()

    # Create a personal smart folder
    folder = await client.smartfolder.personal.create({
        "name": "My Networks",
        "query_items": [
            {"field": "type", "op_match": "=", "value": "network"},
            {"field": "comment", "op_match": "~=", "value": "prod"},
        ],
        "comment": "All production networks",
    })

    # List children of a smart folder
    children = await client.smartfolder.children.list(
        smartfolder=folder._ref
    ).all()
```

---

## Notification (`client.notification`)

The Notification domain configures REST webhook triggers that fire when NIOS objects are
created, modified, or deleted.

**Resources:** `rest_endpoint`, `rest_template`, `rule`

```python
async with NiosClient() as client:
    # Create a REST endpoint (webhook target)
    endpoint = await client.notification.rest_endpoint.create({
        "name": "my-webhook",
        "uri": "https://hooks.example.com/nios",
        "client_certificate_subject": "",
        "comment": "ITSM webhook",
    })

    # Templates cannot be created through WAPI (create is restricted on
    # notification:rest:template). Upload the template file, import it by
    # token, then look it up. Editing an imported template is allowed.
    session = await client.misc.fileop.upload_init(filename="ip-created-template.json")
    response = await client._http._client.put(
        session["url"],
        content=b'{"name": "ip-created-template", "content": "..."}',
        headers={"Content-Type": "application/octet-stream"},
    )
    response.raise_for_status()
    result = await client.misc.fileop.call(
        "restapi_template_import", token=session["token"], overwrite=True
    )
    print(result["overall_status"])
    template = await client.notification.rest_template.find_one(name="ip-created-template")

    # Create a notification rule
    rule = await client.notification.rule.create({
        "name": "on-fixedaddress-create",
        "notification_action": "create",
        "object_type": "fixedaddress",
        "endpoints": [endpoint._ref],
        "template": template._ref,
        "comment": "Fire webhook on fixed address creation",
    })
    print(rule._ref)
```

---

## ACL (`client.acl`)

Named ACLs define reusable access control lists referenced by DNS views, zones, and TSIG keys.

**Resources:** `namedacl`

```python
async with NiosClient() as client:
    # List named ACLs
    acls = await client.acl.namedacl.list().all()
    for a in acls:
        print(a.name, a.comment)

    # Create a named ACL for internal resolvers
    acl = await client.acl.namedacl.create({
        "name": "internal-resolvers",
        "access_list": [
            {"address": "10.0.0.0/8", "permission": "ALLOW"},
            {"address": "172.16.0.0/12", "permission": "ALLOW"},
            {"address": "any", "permission": "DENY"},
        ],
        "comment": "Internal network ACL",
    })
    print(acl._ref)
```

---

## Misc (`client.misc`)

The Misc domain is a grab-bag of utility and infrastructure resources. Two classes - `Fileop`
and `Search` - are **plain classes** (not `WapiResource` subclasses) and only expose
function-based operations, not standard CRUD.

**Resources (WapiResource):** `allendpoints`, `bfdtemplate`, `capacityreport`, `csvimporttask`,
`datacollectioncluster`, `db_objects`, `dbsnapshot`, `deleted_objects`, `dxl_endpoint`,
`kerberoskey`, `outbound_cloudclient`, `pxgrid_endpoint`, `ruleset`, `scavengingtask`,
`scheduledtask`, `syslog_endpoint`, `taxii`, `tftpfiledir`

**Function-only classes (no CRUD):** `Fileop`, `Search`

### Search

```python
async with NiosClient() as client:
    # Global search across all NIOS object types
    results = await client.misc.search.search(search_string="web01.example.com")
    for r in results:
        print(r.get("_ref"), r.get("name", ""))
```

### File operations (Fileop)

```python
async with NiosClient() as client:
    # 1. Open an upload session
    session = await client.misc.fileop.upload_init()
    token, upload_url = session["token"], session["url"]

    # 2. PUT the file content to the returned URL
    response = await client._http._client.put(
        upload_url,
        content=b"fqdn,view\nexample.com,default",
        headers={"Content-Type": "application/octet-stream"},
    )
    response.raise_for_status()

    # 3. Start the import with the session token
    job = await client.misc.fileop.csv_import(
        token=token, action="START", on_error="STOP", operation="INSERT"
    )
    print(job["import_id"])
```

### Scheduled tasks

```python
async with NiosClient() as client:
    # List pending scheduled tasks
    tasks = await client.misc.scheduledtask.list().all()
    for t in tasks:
        print(t.submit_time, t.execution_status)

    # Capacity report
    caps = await client.misc.capacityreport.list().all()
```

### CSV import tasks

```python
async with NiosClient() as client:
    # Monitor CSV import progress
    import_tasks = await client.misc.csvimporttask.list().all()
    for task in import_tasks:
        print(task.action, task.status, task.lines_processed)
```

### Database snapshots

```python
async with NiosClient() as client:
    snapshots = await client.misc.dbsnapshot.list().all()
    for s in snapshots:
        print(s.comment, s.timestamp)
```

### Kerberos keys

```python
async with NiosClient() as client:
    kkeys = await client.misc.kerberoskey.list().all()
```

### TAXII and threat intelligence endpoints

```python
async with NiosClient() as client:
    taxii = await client.misc.taxii.list().all()
    dxl = await client.misc.dxl_endpoint.list().all()
    pxgrid = await client.misc.pxgrid_endpoint.list().all()
```
